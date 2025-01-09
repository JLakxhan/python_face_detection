const SearchUserButton = document.getElementById("search-user-btn");

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