from django.http import JsonResponse
from keras.models import model_from_json
import numpy as np
import cv2
import os
from django.conf import settings
import traceback
from .models import Shift, Prediction
from django.shortcuts import render,redirect
from django.utils.timezone import now

def start_shift(request):
    if request.user.is_authenticated:
        # Check if the user already has an active shift
        active_shift = Shift.objects.filter(user=request.user, end_time__isnull=True).first()
        
        if active_shift:
            # If an active shift exists, return its ID
            return JsonResponse({
                'code': 1, 
                'message': "Active shift already exists.", 
                "shift_id": active_shift.id
            })
        else:
            # If no active shift, create a new one
            shift = Shift(user=request.user)
            shift.save()
            return JsonResponse({
                'code': 1, 
                'message': "Shift started successfully.", 
                "shift_id": shift.id
            })
    else:
        return redirect('login')

    
def end_shift(request):
    if request.user.is_authenticated: 
        shift = Shift.objects.get(id=request.POST['id'])
        shift.end_time = now()
        shift.save()

        return JsonResponse({'code': 1, 'message':"Shift completed successfully."})
    else:
        return redirect('login')
    
def analyze_emotion_and_stress(request):
    try:
        if request.method != "POST":
            return JsonResponse({"code": 0, "error": "Invalid request method"}, status=400)

        emotion_classes = ["Angry", "Disgust", "Fearful", "Happy", "Neutral", "Sad", "Surprised"]
        stress_classes = ["Notstress", "Stress"]

        # Load emotion detection model
        with open(os.path.join(settings.BASE_DIR, 'prediction', 'emotion_detection_output_final_v2.json'), 'r') as json_file:
            emotional_loaded_model_json = json_file.read()
        emotion_model = model_from_json(emotional_loaded_model_json)
        emotion_model.load_weights(os.path.join(settings.BASE_DIR, 'prediction', 'emotion_detection_output_final_v2_1.weights.h5'))

        # Load stress detection model
        with open(os.path.join(settings.BASE_DIR, 'prediction', 'stress_detection_output_final_v2.json'), 'r') as json_file:
            stress_loaded_model_json = json_file.read()
        stress_model = model_from_json(stress_loaded_model_json)
        stress_model.load_weights(os.path.join(settings.BASE_DIR, 'prediction', 'stress_detection_output_final_v2_1.weights.h5'))

        # Get the image frame from the request
        file = request.FILES.get("frame")
        if not file:
            return JsonResponse({"code": 0, "error": "No frame received"}, status=400)

        # Read the image from the request
        file_bytes = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Convert to grayscale for face detection
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Load the Haar Cascade classifier
        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        # Detect faces
        faces = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=1)
        if len(faces) == 0:
            return JsonResponse({"code": 0, "error": "No face detected"}, status=200)

        # Find the largest face
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        x, y, w, h = largest_face

        # Crop the largest face
        cropped_face = gray_image[y:y + h, x:x + w]

        # Resize the cropped face to 48x48
        resized_face = cv2.resize(cropped_face, (48, 48), interpolation=cv2.INTER_AREA)

        # Normalize the resized face for the model
        resized_face = resized_face.astype("float32") / 255.0
        resized_face = np.expand_dims(resized_face, axis=0)  # Add batch dimension

        # Predict emotion
        emotion_predictions = emotion_model.predict(resized_face)
        emotion = emotion_classes[np.argmax(emotion_predictions)]
        emotion_confidence = round(100 * float(np.max(emotion_predictions)), 2)

        # Predict stress
        stress_predictions = stress_model.predict(resized_face)
        stress = stress_classes[np.argmax(stress_predictions)]
        stress_confidence = round(100 * float(np.max(stress_predictions)), 2)

        shift = Shift.objects.get(id=request.POST['shift'])
        prediction = Prediction(
            shift=shift,
            suprise=round(100 * float(emotion_predictions[0][6]), 2),
            sad=round(100 * float(emotion_predictions[0][5]), 2),
            netural=round(100 * float(emotion_predictions[0][4]), 2),
            happy=round(100 * float(emotion_predictions[0][3]), 2),
            fearful=round(100 * float(emotion_predictions[0][2]), 2),
            disgusted=round(100 * float(emotion_predictions[0][1]), 2),
            angry=round(100 * float(emotion_predictions[0][0]), 2),
            stress=round(100 * float(stress_predictions[0][1]), 2),
        )
        prediction.save()

        # Return the prediction results
        return JsonResponse({
            "code": 1,
            # "emotion_predictions" : stress_predictions[0][1]
            # "emotion": emotion,
            # "emotion_confidence": emotion_confidence,
            # "stress": stress,
            # "stress_confidence": stress_confidence
        })

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"code": 0, "error": str(e)}, status=500)
