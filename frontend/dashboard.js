document.getElementById("logout-button").addEventListener("click", () => {
    fetch("/admin/logout/", {
        method: "POST",
    }).then(() => {
        window.location.href = "/"; // Redirect to login page after logout
    });
});

document.getElementById("presence-form").addEventListener("submit", (e) => {
    e.preventDefault();

    const laborerId = document.getElementById("laborer-id").value;
    const present = document.getElementById("present").value === "true";

    fetch("/admin/presence/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ laborer_id: laborerId, present }),
    }).then(response => response.json()).then(data => {
        alert(data.message); // Display success message
        document.getElementById("presence-form").reset(); // Reset the form
    });
});
