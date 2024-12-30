const video = document.getElementById("video");
const emotionText = document.getElementById("emotion-text");
const startButton = document.getElementById("start-btn");
const endShiftButton = document.getElementById("end-btn");

let isDetecting = false; // Flag to track if emotion detection is started

startButton.addEventListener("click", () => {
    isDetecting = true; // Set to true when emotion detection is started
    emotionText.textContent = "Detecting..."; // Set text while detecting
    alert("Emotion detection started!");
});

endShiftButton.addEventListener("click", () => {
    isDetecting = false; // Stop detecting when shift ends
    emotionText.textContent = "N/A"; // Reset emotion text
    alert("Camera is turned off!");
});

// Start webcam
navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
    video.srcObject = stream;
});

// Periodically capture frames and send to the backend if detecting
setInterval(() => {
    if (isDetecting) {
        const canvas = document.createElement("canvas");
        const context = canvas.getContext("2d");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0);

        // Convert the captured image to grayscale before sending to backend
        const imgData = context.getImageData(0, 0, canvas.width, canvas.height);
        const pixels = imgData.data;
        for (let i = 0; i < pixels.length; i += 4) {
            // Convert to grayscale using the formula: gray = 0.3 * R + 0.59 * G + 0.11 * B
            let gray = 0.3 * pixels[i] + 0.59 * pixels[i + 1] + 0.11 * pixels[i + 2];
            pixels[i] = pixels[i + 1] = pixels[i + 2] = gray; // Set RGB channels to the gray value
        }
        context.putImageData(imgData, 0, 0); // Update canvas with grayscale image

        // Resize the canvas to 48x48 before sending to the backend
        const resizedCanvas = document.createElement("canvas");
        const resizedContext = resizedCanvas.getContext("2d");
        resizedCanvas.width = 48;
        resizedCanvas.height = 48;
        resizedContext.drawImage(canvas, 0, 0, 48, 48); // Resize the image

        resizedCanvas.toBlob((blob) => {
            const formData = new FormData();
            formData.append("frame", blob);

            fetch("http://127.0.0.1:5000/analyze/", {
                method: "POST",
                body: formData,
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.error) {
                        emotionText.textContent = "Error: Not detecting.";
                        console.error("Backend Error:", data.error);
                    } else {
                        emotionText.textContent = `${data.emotion} (${data.confidence}%)`;
                    }
                })
                .catch((error) => {
                    emotionText.textContent = "Error: Not detecting.";
                    console.error("Fetch Error:", error);
                });
        });
    }
}, 10000); // Capture a frame every 10 seconds
