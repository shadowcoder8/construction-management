document.getElementById("toggle-password").addEventListener("click", function() {
    const passwordInput = document.getElementById("password");
    const icon = document.getElementById("toggle-password-icon");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
        this.setAttribute("aria-label", "Hide password");
    } else {
        passwordInput.type = "password";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
        this.setAttribute("aria-label", "Show password");
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
