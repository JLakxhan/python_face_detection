const video = document.getElementById("video");
const emotionText = document.getElementById("emotion-text");
const startButton = document.getElementById("start-btn");
const endShiftButton = document.getElementById("end-btn");

let isDetecting = false; // Flag to track if emotion detection is started
let shiftId;
let letTimeout;

const showToast = (message, type = "success") => {
    Toastify({
        text: message,
        duration: 6000,
        close: true,
        gravity: "top", // `top` or `bottom`
        position: "right", // `left`, `center` or `right`
        backgroundColor: type === "success" ? "green" : "red",
        stopOnFocus: true,
    }).showToast();
};

startButton.addEventListener("click", () => {
    fetch("/shift/start/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken
        },
        body: {},
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.code == 1) {
                shiftId = data.shift_id;
                isDetecting = true;
                emotionText.textContent = "Detecting...";
                showToast(data.message, "success");

                navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
                    video.srcObject = stream;
                }).catch((error) => {
                    console.error("Camera Error:", error);
                    showToast("Unable to access the camera. Please check permissions.", "error");
                });

                letTimeout = setInterval(() => {
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
                            let gray = 0.3 * pixels[i] + 0.59 * pixels[i + 1] + 0.11 * pixels[i + 2];
                            pixels[i] = pixels[i + 1] = pixels[i + 2] = gray;
                        }
                        context.putImageData(imgData, 0, 0);

                        // Resize the canvas to 48x48 before sending to the backend
                        const resizedCanvas = document.createElement("canvas");
                        const resizedContext = resizedCanvas.getContext("2d");
                        resizedCanvas.width = 48;
                        resizedCanvas.height = 48;
                        resizedContext.drawImage(canvas, 0, 0, 48, 48);

                        resizedCanvas.toBlob((blob) => {
                            const formData = new FormData();
                            formData.append("frame", blob);
                            formData.append("shift", shiftId);

                            fetch("/analyze/", {
                                method: "POST",
                                headers: {
                                    "X-CSRFToken": csrfToken
                                },
                                body: formData,
                            })
                                .then((response) => response.json())
                                .then((data) => {
                                    if (data.error) {
                                        emotionText.textContent = "Error: Unable to detect.";
                                        console.error("Backend Error:", data.error);
                                        showToast("Error detecting emotion.", "error");
                                    } else {
                                        emotionText.textContent = `${data.emotion} (${data.emotion_confidence}%)`;
                                    }
                                })
                                .catch((error) => {
                                    emotionText.textContent = "Connection error. Please check your backend.";
                                    console.error("Fetch Error:", error);
                                    showToast("Connection error. Please check your backend.", "error");
                                });
                        });
                    }
                }, 10000); // Capture a frame every 10 seconds
            } else {
                showToast(data.message, "error");
            }
        })
        .catch((error) => {
            emotionText.textContent = "Connection error. Please check your backend.";
            console.error("Fetch Error:", error);
            showToast("Connection error. Please check your backend.", "error");
        });
});

endShiftButton.addEventListener("click", () => {
    clearInterval(letTimeout);
    isDetecting = false;
    emotionText.textContent = "N/A";

    // Stop the video stream
    const stream = video.srcObject;
    if (stream) {
        const tracks = stream.getTracks();
        tracks.forEach((track) => track.stop());
        video.srcObject = null;
    }
    const formData = new FormData();
    formData.append("id", shiftId);

    fetch("/shift/end/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken
        },
        body: formData
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.code == 1) {
                shiftId = null;
                isDetecting = false;
                showToast(data.message, "success");
            } else {
                showToast(data.message, "error");
            }
        })
        .catch((error) => {
            emotionText.textContent = "Connection error. Please check your backend.";
            console.error("Fetch Error:", error);
            showToast("Connection error. Please check your backend.", "error");
        });
});
