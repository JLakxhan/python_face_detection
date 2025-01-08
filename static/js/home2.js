const startButton = document.getElementById("start-btn");
const endShiftButton = document.getElementById("end-btn");
const tableBody = document.getElementById("table-body");

let isDetecting = false; // Track if detection is active
let startTime; // Track shift start time

startButton.addEventListener("click", () => {
    isDetecting = true;
    startTime = new Date();
    alert("Shift started. Detecting emotions...");
});

endShiftButton.addEventListener("click", () => {
    isDetecting = false;
    const endTime = new Date();

    fetch("/save-shift-data/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken, // Add CSRF token for Django protection
        },
        body: JSON.stringify({
            start_time: startTime.toISOString(),
            end_time: endTime.toISOString(),
            average_emotion: "happy", // Replace with dynamic emotion if available
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert("Shift ended and data saved!");
            } else {
                alert("Error saving data: " + data.error);
            }
        })
        .catch((error) => console.error("Error:", error));
});

// Send periodic frames to backend if detecting
setInterval(() => {
    if (isDetecting) {
        // Capture frame and send to backend (skipping video details)
        fetch("http://127.0.0.1:5000/analyze/", {
            method: "POST",
            body: JSON.stringify({ image_data: "frame_placeholder" }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.error) {
                    console.error("Backend Error:", data.error);
                } else {
                    if (data.emotion === "stress") {
                        alert("Stress detected!");
                    }
                }
            })
            .catch((error) => console.error("Fetch Error:", error));
    }
}, 10000);

document.addEventListener("DOMContentLoaded", () => {
    fetch("/fetch-shift-data/")
        .then((response) => response.json())
        .then((data) => {
            if (data.shifts) {
                data.shifts.forEach((shift) => {
                    const row = `
                        <tr>
                            <td>${shift.username}</td>
                            <td>${shift.shift_start_time}</td>
                            <td>${shift.shift_end_time}</td>
                            <td>${shift.average_emotion}</td>
                        </tr>
                    `;
                    tableBody.innerHTML += row;
                });
            }
        })
        .catch((error) => console.error("Error fetching shifts:", error));
});
