
const createLeave = document.getElementById('apply-leave-btn');

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
        // JavaScript to handle form submission
createLeave.addEventListener('click', (event) => {
    event.preventDefault(); // Prevent form reload
    const formData = new FormData();
    formData.append('leave_type', document.getElementById('leave-type').value);
    formData.append('start_date', document.getElementById('start-date').value);
    formData.append('end_date', document.getElementById('end-date').value);

    fetch("/users/create/leave/", {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.code === 1) {
            showToast(data.data);
            document.getElementById('apply-leave-form').reset(); // Reset the form
        } else {
            showToast(data.data, "error");
            showToast("Connection error. Please check backend.", "error");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        showToast("Connection error. Please check backend.", "error");
    });
});