document.addEventListener("DOMContentLoaded", () => {
    const togglePasswordBtn = document.getElementById("toggle-password");
    const passwordInput = document.getElementById("password");
    const togglePasswordIcon = document.getElementById("toggle-password-icon");

    if (togglePasswordBtn && passwordInput && togglePasswordIcon) {
        togglePasswordBtn.addEventListener("click", () => {
            const isPassword = passwordInput.getAttribute("type") === "password";
            passwordInput.setAttribute("type", isPassword ? "text" : "password");
            togglePasswordIcon.className = isPassword ? "fas fa-eye-slash" : "fas fa-eye";
            togglePasswordBtn.setAttribute("aria-label", isPassword ? "Hide password" : "Show password");
        });
    }
});

document.getElementById("login-form").addEventListener("submit", (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Send the login request to the backend
    fetch("/admin/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username: username,
            password: password,
        }),
    })
    .then((response) => {
        if (response.ok) {
            // Redirect to the admin dashboard if login is successful
            window.location.href = "/admin/dashboard/";
        } else {
            const errorMessage = document.getElementById("error-message");
            errorMessage.style.display = "block"; // Show error message
        }
    });
});
