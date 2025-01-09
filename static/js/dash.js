const shiftStatusText = document.getElementById("shift-status");
const SearchShiftButton = document.getElementById("search-btn");
const LogoutButton = document.getElementById("logot-btn");

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

LogoutButton.addEventListener("click", () => {
    window.location.href = "/login";  
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


