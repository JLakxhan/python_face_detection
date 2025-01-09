const video = document.getElementById("video");
const emotionText = document.getElementById("emotion-text");
const shiftStatusText = document.getElementById("shift-status");
const startButton = document.getElementById("start-btn");
const endShiftButton = document.getElementById("end-btn");
const SearchShiftButton = document.getElementById("search-btn");


let isDetecting = false; // Flag to track if emotion detection is started
let shiftId;
let letTimeoutAlert;
let letTimeout;
let predictionBuffer = []; // To store emotion and stress predictions
let avgTimeout; // Interval for sending average predictions

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
        headers: { "X-CSRFToken": csrfToken },
        body: {},
    })
    .then((response) => response.json())
        .then((data) => {
            if (data.code === 1) {
                shiftId = data.shift_id;
                isDetecting = true;
                shiftStatusText.textContent = `Shift started at ${data.start_time}`;
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

                        canvas.toBlob((blob) => {
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

                                        // Add predictions to buffer
                                        predictionBuffer.push({
                                            emotionConfidence: data.emotion_confidence,
                                            stressConfidence: data.stress_confidence,
                                        });
                                    }
                                })
                                .catch((error) => {
                                    emotionText.textContent = "Connection error. Please check your backend.";
                                    console.error("Fetch Error:", error);
                                    showToast("Connection error. Please check your backend.", "error");
                                });
                        });
                    }
                }, 10000);

                avgTimeout = setInterval(sendAveragePredictions, 25000)

            } else {
                showToast(data.message, "error");
            }
        })
        .catch((error) => {
            shiftStatusText.textContent = "Connection error. Please check your backend.";
            console.error("Fetch Error:", error);
            showToast("Connection error. Please check your backend.", "error");
        });
});

endShiftButton.addEventListener("click", () => {
    if (!shiftId) {
        showToast("No active shift to end.", "error");
        return;
    }

    clearInterval(letTimeout);
    clearInterval(avgTimeout);
    isDetecting = false;

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
        headers: { "X-CSRFToken": csrfToken },
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.code === 1) {
                shiftId = null;
                isDetecting = false;
                shiftStatusText.textContent = "Click the button below to start detecting emotions in real-time.";
                showToast(data.message, "success");
            } else {
                showToast(data.message, "error");
            }
        })
        .catch((error) => {
            shiftStatusText.textContent = "Connection error. Please check your backend.";
            console.error("Fetch Error:", error);
            showToast("Connection error. Please check your backend.", "error");
        });
});

SearchShiftButton.addEventListener("click",()=>{
    const formData = new FormData();
    formData.append("date",  document.getElementById("search-date").value);

    fetch("/shift/search/", {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
        body: formData,
    })
    .then((response) => response.json())
        .then((data) => {
            if (data.code == 1) {
                let rows = '';  // Initialize rows before the loop

                data.data.forEach(addRow);
                
                function addRow(item) { 
                    rows += "<tr>";
                    rows += "<td>" + item.id + "</td>";
                    rows += "<td>" +addTimeAndFormat(item.start_time) + "</td>";
                    rows += "<td>" + (item.end_time != null ? addTimeAndFormat(item.end_time) : '') + "</td>";
                    rows += "</tr>";
                }
                document.getElementById('table-body').innerHTML = rows;
					// $('#tableData').DataTable();
            } else {
                showToast(data.message, "error");
            }
        })
        .catch((error) => {
            console.error("Fetch Error:", error);
            showToast("Connection error. Please check backend.", "error");
        });
});

const sendAveragePredictions = () => {
    const formData = new FormData();
    formData.append("shift_id", shiftId);

    fetch("/shift/avg/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
        },
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.code === 1) {
                showToast(data.message, "success");

                        // Check if the browser supports notifications
                if (Notification.permission === "granted") {
                    // Create and show the notification
                    new Notification("Work Management System", {
                        body: data.message,
                        icon: "/path-to-your-icon.png"  // Optional: icon for the notification
                    });
                } else if (Notification.permission !== "denied") {
                    // Request permission from the user if not granted yet
                    Notification.requestPermission().then(permission => {
                        if (permission === "granted") {
                            // Create and show the notification
                            new Notification("Work Management System", {
                                body: data.message,
                                icon: "/path-to-your-icon.png"  // Optional: icon for the notification
                            });
                        }
                    });
                }
            } else {
                showToast("Error saving average predictions: " + data.message, "error");
            }
        })
        .catch((error) => {
            console.error("Error saving average predictions:", error);
            showToast("Connection error while saving average predictions.", "error");
        });

};

// document.addEventListener("DOMContentLoaded", () => {
//     fetch("/shift/status/", {
//         method: "GET",
//         headers: { "X-CSRFToken": csrfToken },
//     })
//         .then((response) => response.json())
//         .then((data) => {
//             if (data.active) {
//                 shiftId = data.shift_id;
//                 shiftStatusText.textContent = `Shift started at ${data.start_time}`;
//             } else {
//                 shiftStatusText.textContent = "Click the button below to start detecting emotions in real-time.";
//             }
//         })
//         .catch((error) => {
//             console.error("Error checking shift status:", error);
//             shiftStatusText.textContent = "Error fetching shift status. Please try again.";
//         });
// });



function addTimeAndFormat(utcDateStr) {
    if (!utcDateStr) return ''; // Handle null or empty times
    
    const utcDate = new Date(utcDateStr); // Parse the UTC date
    // Check if the input is a valid date
    if (isNaN(utcDate.getTime())) {
        return ''; // Return empty if the date is invalid
    }
    
    // Add 5 hours and 30 minutes to the date
    utcDate.setHours(utcDate.getHours() + 5); // Add 5 hours
    utcDate.setMinutes(utcDate.getMinutes() + 30); // Add 30 minutes
    
    // Format the date to 'Y-m-d H:i:s' in the local timezone (Asia/Colombo)
    const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false, // Use 24-hour format
    };

    // Use toLocaleString with the Asia/Colombo timezone
    const localTime = utcDate.toLocaleString('en-GB', {
        ...options,
        timeZone: 'Asia/Colombo', // Force timezone to Asia/Colombo
    });

    // Format the result to 'Y-m-d H:i:s'
    const [datePart, timePart] = localTime.split(', ');

    // Change '/' to '-' and reformat to 'Y-m-d' (ISO format)
    const formattedDate = datePart.split('/').reverse().join('-');  // Reverse and join with '-'

    // Join date and time parts with a space
    return `${formattedDate} ${timePart}`;
}


