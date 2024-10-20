const laborForm = document.getElementById("labor-form");
const laborList = document.querySelector("#labor-list tbody");
const attendanceModal = document.getElementById("attendance-modal");
const attendanceList = document.querySelector("#attendance-list tbody");
const searchInput = document.getElementById("search-bar");
const searchAttendanceInput = document.getElementById("search-bar-labor");


let editingLaborId = null;
let currentLaborPage = 1;
let currentAttendancePage = 1;
const itemsPerPage = 10;

// Logout Functionality
document.getElementById("logout-button").addEventListener("click", () => {
    fetch("/admin/logout/", {
        method: "POST",
    }).then(() => {
        window.location.href = "/"; // Redirect to login page after logout
    });
});

// Add/Edit Laborer
laborForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const name = document.getElementById("labor-name").value;
    const age = document.getElementById("labor-age").value;
    const gender = document.getElementById("labor-gender").value;
    const wage = document.getElementById("labor-wage").value;
    const date = document.getElementById("labor-date").value;

    const laborerData = { name, age, gender, daily_wage: wage, date_of_joining: date };
    
    if (editingLaborId) {
        await updateLaborer(editingLaborId, laborerData);
    } else {
        await addLaborer(laborerData);
    }

    laborForm.reset();
    editingLaborId = null;
    document.getElementById("save-laborer-btn").innerText = "Add Laborer";
});

// Close Laborer Modal
document.getElementById("close-labor-modal").addEventListener("click", () => {
    laborForm.reset();
    editingLaborId = null;
    document.getElementById("save-laborer-btn").innerText = "Add Laborer"; 
});

// Add Laborer Function
async function addLaborer(laborer) {
    const response = await fetch("/labours/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(laborer),
    });

    if (response.ok) {
        alert("Laborer added successfully!");
        loadLaborers(currentLaborPage);
    } else {
        alert("Failed to add laborer.");
    }
}

// Update Laborer Function
async function updateLaborer(id, laborer) {
    const response = await fetch(`/labours/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(laborer),
    });

    if (response.ok) {
        alert("Laborer updated successfully!");
        loadLaborers(currentLaborPage);
    } else {
        alert("Failed to update laborer.");
    }
}

// Delete Laborer Function
async function deleteLaborer(id) {
    const confirmed = confirm("Are you sure you want to delete this laborer?");
    if (confirmed) {
        const response = await fetch(`/labours/${id}`, { method: "DELETE" });

        if (response.ok) {
            alert("Laborer deleted successfully!");
            loadLaborers(currentLaborPage);
            loadAttendanceHistory(currentAttendancePage); // Refresh the attendance history
        } else {
            alert("Failed to delete laborer.");
        }
    }
}

// Load Laborers with Pagination
async function loadLaborers(page) {
    document.getElementById("loading").style.display = "block"; // Show loading indicator
    
    const skip = (page - 1) * itemsPerPage; // Calculate skip for pagination
    const response = await fetch(`/labours/?skip=${skip}&limit=${itemsPerPage}`);
    
    if (response.ok) {
        const data = await response.json();
        laborList.innerHTML = ""; // Clear existing labor list

        if (data.length > 0) {
            data.forEach((laborer) => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${laborer.name}</td>
                    <td>${laborer.age}</td>
                    <td>${laborer.gender}</td>
                    <td>${laborer.daily_wage}</td>
                    <td>
                        <button onclick="editLaborer(${laborer.id})">Edit</button>
                        <button onclick="deleteLaborer(${laborer.id})">Delete</button>
                        <button onclick="openAttendanceModal(${laborer.id})">Record Attendance</button>
                    </td>
                `;
                laborList.appendChild(row);
            });
        } else {
            const row = document.createElement("tr");
            row.innerHTML = `<td colspan="5">No laborers found.</td>`;
            laborList.appendChild(row);
        }

        // Update pagination info and buttons
        document.getElementById("page-info").textContent = `Page ${page}`;
        document.getElementById("prev-button").disabled = page === 1;
        document.getElementById("next-button").disabled = data.length < itemsPerPage; // Disable next if fewer results
    } else {
        console.error("Failed to load laborers.");
        alert("Failed to load laborers.");
    }

    document.getElementById("loading").style.display = "none"; // Hide loading indicator
}

// Edit Laborer
async function editLaborer(id) {
    const response = await fetch(`/labours/${id}`);
    if (response.ok) {
        const laborer = await response.json();

        document.getElementById("labor-name").value = laborer.name;
        document.getElementById("labor-age").value = laborer.age;
        document.getElementById("labor-gender").value = laborer.gender;
        document.getElementById("labor-wage").value = laborer.daily_wage;
        document.getElementById("labor-date").value = laborer.date_of_joining;

        editingLaborId = id;
        document.getElementById("save-laborer-btn").innerText = "Update Laborer"; 
    } else {
        alert("Failed to load laborer details.");
    }
}

// Search Laborers
let debounceTimer;
searchInput.addEventListener("input", () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        const searchTerm = searchInput.value.toLowerCase();
        const rows = laborList.getElementsByTagName("tr");
        for (const row of rows) {
            const name = row.cells[0].textContent.toLowerCase();
            row.style.display = name.includes(searchTerm) ? "" : "none";
        }
    }, 300);
});


// Pagination Controls for Laborers
document.getElementById("prev-button").addEventListener("click", () => {
    if (currentLaborPage > 1) {
        currentLaborPage--;
        loadLaborers(currentLaborPage);
    }
});

document.getElementById("next-button").addEventListener("click", () => {
    currentLaborPage++;
    loadLaborers(currentLaborPage);
});

// Update pagination controls for attendance
document.getElementById("prev-attendance-button").addEventListener("click", () => {
    if (currentAttendancePage > 1) {
        currentAttendancePage--;
        loadAttendanceHistory(currentAttendancePage);
    }
});

document.getElementById("next-attendance-button").addEventListener("click", () => {
    currentAttendancePage++;
    loadAttendanceHistory(currentAttendancePage);
});

// Open Attendance Modal for both new and edit
function openAttendanceModal(laborerId, attendanceId = null) {
    document.getElementById("attendance-labor-id").value = laborerId;

    if (attendanceId) {
        // Edit existing attendance
        editAttendance(attendanceId);
    } else {
        // Add new attendance
        resetAttendanceForm();
    }

    attendanceModal.style.display = "block"; // Show modal
}

// Close Attendance Modal
document.getElementById("close-attendance-modal").addEventListener("click", () => {
    attendanceModal.style.display = "none"; // Hide modal
});

// Reset attendance form for new record
function resetAttendanceForm() {
    document.getElementById("attendance-form").reset();  // Clear form fields
    document.getElementById("attendance-form").onsubmit = async function (e) {
        e.preventDefault();
        await addAttendance();  // Use the POST method to create a new record
    };
}

// Add Attendance
async function addAttendance() {
    const laborId = document.getElementById("attendance-labor-id").value;
    const date = document.getElementById("attendance-date").value;
    const status = document.getElementById("attendance-status").value;
    const hoursWorked = document.getElementById("hours-worked").value;
    const site = document.getElementById("attendance-site-name").value;

    const attendanceData = { labor_id: laborId, date: date, status: status, hours_worked: hoursWorked , site_name:site};

    const response = await fetch(`/labours/${laborId}/attendance/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            laborer_id: attendanceData.labor_id,
            date: attendanceData.date,
            present: attendanceData.status,
            hours_worked: attendanceData.hours_worked,
            site_name: attendanceData.site_name,
        }),
    });

    if (response.ok) {
        alert("Attendance recorded successfully!");
        loadAttendanceHistory(currentAttendancePage);
        attendanceModal.style.display = "none"; // Hide modal after submission
    } else {
        alert("Failed to record attendance.");
    }
}

// Edit Attendance
async function editAttendance(id) {
    const response = await fetch(`/attendance/${id}`); // Fetch attendance by ID
    if (response.ok) {
        const attendance = await response.json();

        document.getElementById("attendance-labor-id").value = attendance.laborer_id;
        document.getElementById("attendance-date").value = attendance.date;
        document.getElementById("attendance-status").value = attendance.present ? "Present" : "Absent";
        document.getElementById("hours-worked").value = attendance.hours_worked;
        document.getElementById("attendance-site-name").value = attendance.site_name;

        document.getElementById("attendance-form").onsubmit = async function (e) {
            e.preventDefault();
            await updateAttendance(id);  // Use the PUT method to update the record
        };

    } else {
        alert("Failed to load attendance record.");
    }
}

// Update Attendance (PUT method)
async function updateAttendance(id) {
    const laborId = document.getElementById("attendance-labor-id").value;
    const date = document.getElementById("attendance-date").value;
    const status = document.getElementById("attendance-status").value;
    const hoursWorked = document.getElementById("hours-worked").value;
    const site = document.getElementById("attendance-site-name").value;

    const attendanceData = {
        laborer_id: laborId,
        date: date,
        present: status,
        hours_worked: hoursWorked,
        site_name: site
    };

    const response = await fetch(`/attendance/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(attendanceData),
    });

    if (response.ok) {
        alert("Attendance updated successfully!");
        loadAttendanceHistory(currentAttendancePage);
        attendanceModal.style.display = "none"; // Hide modal after updating
    } else {
        alert("Failed to update attendance.");
    }
}

// Delete Attendance
async function deleteAttendance(id) {
    const confirmed = confirm("Are you sure you want to delete this attendance record?");
    if (confirmed) {
        const response = await fetch(`/attendance/${id}`, { method: "DELETE" });

        if (response.ok) {
            alert("Attendance deleted successfully!");
            loadAttendanceHistory(currentAttendancePage);
        } else {
            alert("Failed to delete attendance.");
        }
    }
}

// Load Attendance History with Pagination
async function loadAttendanceHistory(page) {
    const response = await fetch(`/attendance/?skip=${(page - 1) * itemsPerPage}&limit=${itemsPerPage}`);
    
    if (response.ok) {
        const data = await response.json();
        attendanceList.innerHTML = "";

        if (data.results && data.results.length > 0) {
            data.results.forEach((attendance) => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${attendance.laborer_name}</td>
                    <td>${attendance.date}</td>
                    <td>${attendance.present}</td>
                    <td>${attendance.hours_worked}</td>
                    <td>${attendance.site_name}</td>
                    <td>
                        <button class="edit-attendance-btn" data-id="${attendance.id}">Edit</button>
                        <button class="delete-attendance-btn" data-id="${attendance.id}">Delete</button>
                    </td>
                `;
                attendanceList.appendChild(row);
            });

            // Attach event listeners to dynamically created buttons
            attachAttendanceEventListeners();
        } else {
            const row = document.createElement("tr");
            row.innerHTML = `<td colspan="5">No attendance records found.</td>`;
            attendanceList.appendChild(row);
        }

        // Update pagination info and buttons
        document.getElementById("attendance-page-info").textContent = `Page ${page}`;
        document.getElementById("prev-attendance-button").disabled = data.prev === null;
        document.getElementById("next-attendance-button").disabled = data.next === null;
    } else {
        alert("Failed to load attendance history.");
    }
}


// Search Attendance For laborers based on both name and site name
let debounceTimers;
searchAttendanceInput.addEventListener("input", () => {
    clearTimeout(debounceTimers);
    debounceTimers = setTimeout(() => {
        const searchTerms = searchAttendanceInput.value.toLowerCase();  // Get the search term

        const rows = attendanceList.getElementsByTagName("tr");  // Get all table rows
        for (const row of rows) {
            const nameCell = row.cells[0];  // Assuming the laborer name is in the first cell
            const siteCell = row.cells[4];  // Assuming the site name is in the fifth cell
            if (nameCell && siteCell) {
                const name = nameCell.textContent.toLowerCase();  // Get the laborer name
                const siteName = siteCell.textContent.toLowerCase();  // Get the site name

                // Show or hide the row if either the name or site name contains the search term
                if (name.includes(searchTerms) || siteName.includes(searchTerms)) {
                    row.style.display = "";  // Show row
                } else {
                    row.style.display = "none";  // Hide row
                }
            }
        }
    }, 300);
});



// Attach event listeners for edit and delete attendance buttons
function attachAttendanceEventListeners() {
    const editButtons = document.querySelectorAll(".edit-attendance-btn");
    const deleteButtons = document.querySelectorAll(".delete-attendance-btn");

    editButtons.forEach(button => {
        button.addEventListener("click", () => {
            const attendanceId = button.dataset.id;
            openAttendanceModal(null, attendanceId);
        });
    });

    deleteButtons.forEach(button => {
        button.addEventListener("click", () => {
            const attendanceId = button.dataset.id;
            deleteAttendance(attendanceId);
        });
    });
}

// Load Initial Data
document.addEventListener("DOMContentLoaded", () => {
    loadLaborers(currentLaborPage);
    loadAttendanceHistory(currentAttendancePage);
});
