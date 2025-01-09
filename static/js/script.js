const container = document.querySelector('.container');
const registerBtn = document.querySelector('.register-btn');
const loginBtn = document.querySelector('.login-btn');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const homePage = document.querySelector('.home');  // Assuming you have a home element for the home page

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
    container.classList.remove('active'); 
    
});



