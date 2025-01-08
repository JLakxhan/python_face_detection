from flask import Flask, request, jsonify
from flask_cors import CORS
from keras.models import model_from_json
import numpy as np
import cv2
import datetime
import traceback

app = Flask(__name__)
CORS(app)


emotion_classes = ["Angry", "Disgust", "Fearful", "Happy", "Netural", "Sad", "Suprised"]
stress_classes = ["Notstress", "Stress"]

with open('emotion_detection_output_final_v2.json', 'r') as json_file:
    emotional_loaded_model_json = json_file.read()

emotion_model = model_from_json(emotional_loaded_model_json)
 
emotion_model.load_weights("emotion_detection_output_final_v2_1.weights.h5")

with open('stress_detection_output_final_v2.json', 'r') as json_file:
    stress_loaded_model_json = json_file.read()

stress_model = model_from_json(stress_loaded_model_json)
 
stress_model.load_weights("stress_detection_output_final_v2_1.weights.h5")
    
@app.route("/analyze/", methods=["POST"])
def analyze_emotion_and_stress():
    # try:
        # Get the image frame from the request
    file = request.files.get("frame")
    if not file:
        return jsonify({"error": "No frame received"}), 400

    # Read the image from the request
    file_bytes = np.frombuffer(file.read(), np.uint8)  # Read the file content # Read the file content
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)  # Decode to an OpenCV image

        # Convert to grayscale for face detection
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Load the Haar Cascade classifier
    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    # Detect faces
    faces = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=1)
    if len(faces) == 0:
        return jsonify({"error": "No face detected"}), 400

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

    # Return the prediction results
    return jsonify({
        "emotion": emotion,
        "emotion_confidence": emotion_confidence,
        # "stress": stress,
        # "stress_confidence": stress_confidence
    })

# except Exception as e:
#     traceback.print_exc()
# return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
