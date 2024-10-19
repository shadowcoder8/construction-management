document.addEventListener("DOMContentLoaded", () => {
    loadLabours();

    // Handle form submission to add a new labour
    document.getElementById("labour-form").addEventListener("submit", (e) => {
        e.preventDefault();
        
        // Get input values from the form
        const name = document.getElementById("name").value;
        const age = document.getElementById("age").value;
        const gender = document.getElementById("gender").value;
        const dailyWage = document.getElementById("daily-wage").value;

        // Send the POST request to the FastAPI backend to create labour
        fetch("http://localhost:8000/labours/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name: name,
                age: age,
                gender: gender,
                daily_wage: dailyWage,
            }),
        })
        .then((response) => response.json())
        .then(() => {
            loadLabours(); // Reload labour list after adding a new one
            document.getElementById("labour-form").reset(); // Reset the form after submission
        });
    });
});

// Function to load and display labours
function loadLabours() {
    fetch("http://localhost:8000/labours/")
    .then((response) => response.json())
    .then((data) => {
        const labourList = document.getElementById("labour-list");
        labourList.innerHTML = ""; // Clear current list
        data.forEach((labour) => {
            labourList.innerHTML += `
                <tr>
                    <td>${labour.name}</td>
                    <td>${labour.age}</td>
                    <td>${labour.gender === "M" ? "Male" : "Female"}</td>
                    <td>${labour.daily_wage}</td>
                </tr>`;
        });
    });
}
