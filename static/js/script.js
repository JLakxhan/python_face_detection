const container = document.querySelector('.container');
const registerBtn = document.querySelector('.register-btn');
const loginBtn = document.querySelector('.login-btn');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const homePage = document.querySelector('.home');  // Assuming you have a home element for the home page

// Show login form on page load
window.addEventListener('load', () => {
    container.classList.remove('active'); // Ensure the login form is shown on load
    homePage.style.display = 'none'; // Hide the home page initially
});

// Toggle between login and register forms
registerBtn.addEventListener('click', () => {
    container.classList.add('active'); // Show register form
});

loginBtn.addEventListener('click', () => {
    container.classList.remove('active'); // Show login form
});

// Handle login form submission
// loginForm.addEventListener('submit', (e) => {
//     e.preventDefault(); // Prevent default form submission

//     const email = loginForm.querySelector('[name="email"]').value;
//     const password = loginForm.querySelector('[name="password"]').value;

//     // Make a request to Django to authenticate the user
//     fetch('/login/', {
//         method: 'POST',
//         body: new URLSearchParams({
//             'email': email,
//             'password': password,
//         }),
//         headers: {
//             'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
//         },
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.success) {
//             // If login is successful, redirect to home page
//             window.location.href = '/home/';
//         } else {
//             alert('Invalid credentials. Please try again.');
//         }
//     })
//     .catch(error => {
//         console.error('Error:', error);
//         alert('An error occurred during login. Please try again.');
//     });
// });
