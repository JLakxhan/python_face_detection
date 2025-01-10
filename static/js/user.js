const SearchUserButton = document.getElementById("search-user-btn");
const LogoutButton = document.getElementById("logot-btn");
const CreateButton = document.getElementById("");


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

// Function to open a modal
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

// Function to close a modal
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Set data in Edit Modal
function setEditModel(id, username, email, first_name, last_name, is_superuser) {
    document.getElementById('editUserId').value = id;
    document.getElementById('editEmail').value = email;
    document.getElementById('editFname').value = first_name;
    document.getElementById('editLname').value = last_name;
    document.getElementById('editRole').value = is_superuser;
    openModal('editModal');
}

// Set data in Reset Modal
function setPasswordModel(id, username) {
    document.getElementById('resetUserId').value = id;
    openModal('resetModal');
}

// Submit edited user data
function submitEditUser() {
    const formData = new FormData();
    formData.append('id', document.getElementById('editUserId').value);
    formData.append('email', document.getElementById('editEmail').value);
    formData.append('fname', document.getElementById('editFname').value);
    formData.append('lname', document.getElementById('editLname').value);
    formData.append('role', document.getElementById('editRole').value);

    fetch("/user/edit/", {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.code === 1) {
            showToast(data.data);
            closeModal('editModal');
            // Refresh the table data
            // document.getElementById('search-user-btn').click();
        } else {
            showToast(data.data, "error");
            showToast("Conection Error in the backend", "error");
        }
    });
}

// Submit reset password data
function submitResetPassword() {
    const formData = new FormData();
    formData.append('id', document.getElementById('resetUserId').value);
    formData.append('password', document.getElementById('newPassword').value);

    fetch("/user/reset/", {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.code === 1) {
            showToast(data.data);
            closeModal('resetModal');
        } else {
            showToast(data.data, "error");
            showToast("Conection Error in the backend", "error");
        }
    });
}

// Submit create user data
function submitCreateUser() {
    const formData = new FormData();
    formData.append('username', document.getElementById('createUsername').value);
    formData.append('email', document.getElementById('createEmail').value);
    formData.append('password', document.getElementById('createPassword').value);
    formData.append('role', document.getElementById('createRole').value);

    fetch("/users/create/", {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.code === 1) {
            showToast(data.data);
            closeModal('createUserModal');
            // Refresh the table data
            // document.getElementById('search-user-btn').click();
        } else {
            showToast(data.data, "error");
            showToast("Connection error. Please check backend.", "error");
        }
    })
    .catch(error => {
        console.error("Fetch Error:", error);
        showToast("Connection error. Please check backend.", "error");
    });
}


SearchUserButton.addEventListener("click",()=>{
    const formData = new FormData();
    formData.append("role",  document.getElementById("roleFilter").value);

    fetch("/user/search/", {
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
                    rows += "<td>" + item.username + "</td>";
                    rows += "<td>" + item.email + "</td>";
                    rows += "<td>" + item.first_name + " " + item.last_name +  "</td>";
                    rows += "<td>" + (item.is_superuser == 1 ? 'Admin' : 'User') + "</td>";
                    rows += "<td class='ignore'>"; 
                            rows += "<button type='button' onclick='setEditModel(`"+item.id+"`,`"+item.username+"`,`"+item.email+"`,`"+item.first_name+"`,`"+item.last_name+"`,`"+item.is_superuser+"`)' class='btn btn-warning btn-sm' data-bs-toggle='modal' data-bs-target='#editModel'> Edit </button> ";
                            rows += "<button type='button' onclick='setPasswordModel(`"+item.id+"`,`"+item.username+"`)' class='btn btn-danger btn-sm' data-bs-toggle='modal' data-bs-target='#passwordModel'> Reset Password </button> ";
                        rows +="</td>";
                    rows += "</tr>";
                }
                document.getElementById('table-user-body').innerHTML = rows;
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

