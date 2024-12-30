from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import datetime
import traceback

app = Flask(__name__)
CORS(app)

# Load the trained model
model = load_model("emotion_detection_output_final_v2_1.h5")
classes = ["surprise", "neutral", "happy", "fear", "disgust", "angry", "sad"]

@app.route("/analyze/", methods=["POST"])
def analyze_emotion():
    try:
        # Get the image frame from the request
        file = request.files.get("frame")
        if not file:
            return jsonify({"error": "No frame received"}), 400

        # Convert the image to a numpy array
        nparr = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)  # Convert to grayscale

        # Resize the image to 48x48 as per the model's input size
        resized = cv2.resize(img, (48, 48)) / 255.0  # Normalize to [0, 1]
        resized = np.expand_dims(resized, axis=0)  # Add batch dimension
        resized = np.expand_dims(resized, axis=-1)  # Add channel dimension

        # Predict emotion
        predictions = model.predict(resized)
        emotion = classes[np.argmax(predictions)]
        confidence = round(100 * float(np.max(predictions)), 2)

        # Return the prediction result
        return jsonify({"emotion": emotion, "confidence": confidence})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
