from django.http import JsonResponse
from keras.models import model_from_json
import numpy as np
import cv2
import os
from django.conf import settings
import traceback
from .models import Shift, Prediction,PredictionResult
from django.shortcuts import render,redirect
from django.utils.timezone import now,timedelta
from django.utils import timezone
from django.db.models import Avg
from django.views.decorators.csrf import csrf_exempt
import traceback
from bson.decimal128 import Decimal128
from datetime import datetime

def start_shift(request):
    if request.user.is_authenticated:
        # Check if the user already has an active shift
        active_shift = Shift.objects.filter(user=request.user, end_time__isnull=True).first()

        if active_shift:
            # If an active shift exists, return its details
            return JsonResponse({
                'code': 1,
                'message': "Active shift already exists.",
                "shift_id": active_shift.id,
                "start_time": active_shift.start_time.strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            # If no active shift, create a new one
            shift = Shift(user=request.user)
            shift.save()
            return JsonResponse({
                'code': 1,
                'message': "Shift started successfully.",
                "shift_id": shift.id,
                "start_time": shift.start_time.strftime('%Y-%m-%d %H:%M:%S')
            })
    else:
        return redirect('login')


def end_shift(request):
    if request.user.is_authenticated:
        shift_id = request.POST.get('id')
        if not shift_id:
            return JsonResponse({'code': 0, 'message': "Shift ID is missing or invalid."})

        try:
            shift = Shift.objects.get(id=shift_id, user=request.user)
        except Shift.DoesNotExist:
            return JsonResponse({'code': 0, 'message': "Shift not found or already ended."})

        # End the shift
        shift.end_time = timezone.now()
        shift.save()

        return JsonResponse({'code': 1, 'message': "Shift completed successfully for the day."})
    else:
        return JsonResponse({'code': 0, 'message': "User is not authenticated."})


def shift_status(request):
    if request.user.is_authenticated:
        active_shift = Shift.objects.filter(user=request.user, end_time__isnull=True).first()
        if active_shift:
            return JsonResponse({
                'active': True,
                'shift_id': active_shift.id,
                'start_time': active_shift.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            })
        else:
            return JsonResponse({'active': False, 'message': "No active shift."})
    else:
        return JsonResponse({'active': False, 'message': "User not authenticated."})

@csrf_exempt
def analyze_notification(request):
    try:
        if request.method != "POST":
            return JsonResponse({"code": 0, "error": "Invalid request method"}, status=400)

        # Extract the emotion averages from the request
        emotion_averages = request.POST.dict()

        # Define messages for each emotion
        emotion_messages = {
            "Angry": "The user seems to be angry. Consider taking a break!",
            "Disgust": "The user shows signs of disgust. Please ensure they are comfortable.",
            "Fearful": "Fear detected. Check in with the user for reassurance.",
            "Happy": "Great! The user is happy. Keep up the positive atmosphere.",
            "Neutral": "Neutral emotion detected. Everything seems steady.",
            "Sad": "Sadness detected. Offer support if necessary.",
            "Surprised": "Surprise detected. Ensure the user is in a safe environment.",
            "Stress": "High stress levels detected! Consider stress-relieving measures."
        }

        # Check if any emotion average is above 50%
        notifications = []
        for emotion, avg in emotion_averages.items():
            avg_value = float(avg)
            if avg_value > 50 and emotion in emotion_messages:
                notifications.append({"emotion": emotion, "message": emotion_messages[emotion]})

        if notifications:
            return JsonResponse({"code": 1, "notifications": notifications}, status=200)
        else:
            return JsonResponse({"code": 1, "message": "No significant emotions detected."}, status=200)

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"code": 0, "error": str(e)}, status=500)



def analyze_avg_emotion(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"code": 0, "message": "User is not authenticated."}, status=403)

        # Get shift ID from the request
        shift_id = request.POST.get("shift_id")
        if not shift_id:
            return JsonResponse({"code": 0, "message": "Shift ID is missing or invalid."})

        try:
            # Get the shift
            shift = Shift.objects.get(id=shift_id, user=request.user)
        except Shift.DoesNotExist:
            return JsonResponse({"code": 0, "message": "Shift not found."}, status=404)

        # Define the 10-minute time window
        # end_time = now()
        # start_time = end_time - timedelta(minutes=2)

        one_hour_ago = now() - timedelta(hours=1)
        # Fetch predictions within the time window
        predictions = Prediction.objects.filter(
            shift=shift,
            created_at__gte=(one_hour_ago)
        )

        if not predictions.exists():
            return JsonResponse({"code": 0, "message": "No predictions found in the last 10 minutes."})

        # averages = predictions.aggregate(
        #     avg_suprise=Avg("suprise"),
        #     avg_sad=Avg("sad"),
        #     avg_netural=Avg("netural"),
        #     avg_happy=Avg("happy"),
        #     avg_fearful=Avg("fearful"),
        #     avg_disgusted=Avg("disgusted"),
        #     avg_angry=Avg("angry"),
        #     avg_stress=Avg("stress"),
        # )

        sum_suprise = 0.0
        sum_sad = 0.0
        sum_netural = 0.0
        sum_happy = 0.0
        sum_fearful = 0.0
        sum_disgusted = 0.0
        sum_angry = 0.0
        sum_stress = 0.0

        count = predictions.count()

        # Sum up the values for each emotion
        for prediction in predictions:
            sum_suprise += convert_decimal(prediction.suprise)
            sum_sad += convert_decimal(prediction.sad)
            sum_netural += convert_decimal(prediction.netural)
            sum_happy += convert_decimal(prediction.happy)
            sum_fearful += convert_decimal(prediction.fearful)
            sum_disgusted += convert_decimal(prediction.disgusted)
            sum_angry += convert_decimal(prediction.angry)
            sum_stress += convert_decimal(prediction.stress)

        # Calculate averages
        averages = {
            "avg_suprise": round(sum_suprise / count, 2) if count else 0.0,
            "avg_sad": round(sum_sad / count, 2) if count else 0.0,
            "avg_netural": round(sum_netural / count, 2) if count else 0.0,
            "avg_happy": round(sum_happy / count, 2) if count else 0.0,
            "avg_fearful": round(sum_fearful / count, 2) if count else 0.0,
            "avg_disgusted": round(sum_disgusted / count, 2) if count else 0.0,
            "avg_angry": round(sum_angry / count, 2) if count else 0.0,
            "avg_stress": round(sum_stress / count, 2) if count else 0.0,
        }
        # return JsonResponse({"mes":"dcdcd"})  
        # averages = {key: convert_decimal(value) for key, value in averages.items()}
        # return JsonResponse({"averages": averages})

        
        # Save the averages to the PredictionResult model
        result = PredictionResult.objects.create(
            shift=shift,
            avg_prediction_suprise=averages["avg_suprise"],
            avg_prediction_sad=averages["avg_sad"],
            avg_prediction_netural=averages["avg_netural"],
            avg_prediction_happy=averages["avg_happy"],
            avg_prediction_fearful=averages["avg_fearful"],
            avg_prediction_disgusted=averages["avg_disgusted"],
            avg_prediction_angry=averages["avg_angry"],
            avg_prediction_stress=averages["avg_stress"],
        )

        averages_dict = {
            "suprise": averages["avg_suprise"],
            "sad": averages["avg_sad"],
            "netural": averages["avg_netural"],
            "happy": averages["avg_happy"],
            "fearful": averages["avg_fearful"],
            "disgusted": averages["avg_disgusted"],
            "angry": averages["avg_angry"],
            "stress": averages["avg_stress"],
        }

        highest_emotion = max(averages_dict, key=averages_dict.get)  # Emotion with the highest average
        highest_value = averages_dict[highest_emotion]  # Highest average value

        # Check if the highest average is greater than 50
        if highest_value > 10:
            if highest_emotion == 'suprise':
                 return JsonResponse({"code": 1, 'message': "Surprise detected. Ensure the user is in a safe environment."})
            elif highest_emotion == 'sad':
                 return JsonResponse({"code": 1, 'message': "Sadness detected. Offer support if necessary."})
            elif highest_emotion == 'netural':
                 return JsonResponse({"code": 1, 'message': "Neutral emotion detected. Everything seems steady."})
            elif highest_emotion == 'happy':
                 return JsonResponse({"code": 1, 'message': "Great! The user is happy. Keep up the positive atmosphere."})
            elif highest_emotion == 'fearful':
                 return JsonResponse({"code": 1, 'message': "Fear detected. Check in with the user for reassurance."})
            elif highest_emotion == 'disgusted':
                 return JsonResponse({"code": 1, 'message': "The user shows signs of disgust. Please ensure they are comfortable."})
            elif highest_emotion == 'angry':
                 return JsonResponse({"code": 1, 'message': "The user seems to be angry. Consider taking a break! "})
            elif highest_emotion == 'stress':
                 return JsonResponse({"code": 1, 'message': "High stress levels detected! Consider stress-relieving measures"})
        else:
            return JsonResponse({"code": 0})

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"code": 0, "error": str(e)}, status=500)

def convert_decimal(value):
    if isinstance(value, Decimal128):
        return round(float(value.to_decimal()), 2)
    elif value is not None:
        return round(float(value), 2)
    return 0.0

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

def search_shift(request):
    # Get the date from the request
    date_str = request.POST.get('date')  
    if not date_str:
        return JsonResponse({"code": 0, "message": "Date is required."}, status=400)

    try:
        # Parse the date
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({"code": 0, "message": "Invalid date format. Use YYYY-MM-DD."}, status=400)

    # Get the start and end of the day for the target date
    start_of_day = datetime.combine(target_date, datetime.min.time())
    end_of_day = start_of_day + timedelta(days=1)

    # Filter shifts by the start time being within the specific date range
    shifts = Shift.objects.filter(start_time__gte=start_of_day, start_time__lt=end_of_day).values('id', 'start_time', 'end_time')

    # Return the shifts as a JSON response
    return JsonResponse({'code': 1, 'data': list(shifts)})


