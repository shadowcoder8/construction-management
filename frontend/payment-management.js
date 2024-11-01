document.addEventListener("DOMContentLoaded", function () {
    loadLaborers();
    loadSites();
    loadMaterials();
    loadPayments();

    document.getElementById('payment-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const paymentData = {
            amount: parseFloat(document.getElementById('payment-amount').value),
            date: document.getElementById('payment-date').value,
            labor_id: document.getElementById('labor-select').value,
            site_id: document.getElementById('site-select').value,
            material_name: document.getElementById('material-name').value,
            description: document.getElementById('payment-description').value
        };
        await addPayment(paymentData);
        document.getElementById('payment-form').reset();  // Clear form after submission
        await loadPayments();  // Reload payments to reflect new entry
    });

    document.getElementById('close-payment-form').addEventListener('click', () => {
        document.getElementById('payment-form').reset();  // Clear the form
    });

    document.getElementById('search-payment').addEventListener('input', (e) => {
        filterPayments(e.target.value);
    });
});

// Logout Functionality
document.getElementById("logout-button").addEventListener("click", () => {
    fetch("/admin/logout/", {
        method: "POST",
    }).then(() => {
        window.location.href = "/"; // Redirect to login page after logout
    });
});

// Load laborers into dropdown
async function loadLaborers() {
    const response = await fetch('/labours/');
    const laborers = await response.json();
    const laborSelect = document.getElementById('labor-select');
    laborers.forEach(laborer => {
        const option = document.createElement('option');
        option.value = laborer.id;
        option.textContent = laborer.name;
        laborSelect.appendChild(option);
    });
}

// Load sites into dropdown
async function loadSites() {
    const response = await fetch('/sites/');
    const sites = await response.json();
    const siteSelect = document.getElementById('site-select');
    sites.forEach(site => {
        const option = document.createElement('option');
        option.value = site.id;
        option.textContent = site.name;
        siteSelect.appendChild(option);
    });
}

// Load materials into dropdown
async function loadMaterials() {
    const response = await fetch('/materials/');
    const materials = await response.json();
    const materialSelect = document.getElementById('material-select');
    materials.forEach(material => {
        const option = document.createElement('option');
        option.value = material.name;  // Assuming material.name is what you want to show
        option.textContent = material.name;
        materialSelect.appendChild(option);
    });
}

// Load payments with pagination
async function loadPayments(page = 1) {
    const response = await fetch(`/payments/?page=${page}`);
    const payments = await response.json();
    const paymentList = document.getElementById('payment-list').getElementsByTagName('tbody')[0];
    paymentList.innerHTML = ''; // Clear previous data

    payments.results.forEach(payment => {
        const row = paymentList.insertRow();
        row.insertCell(0).textContent = payment.amount;
        row.insertCell(1).textContent = payment.date;
        row.insertCell(2).textContent = payment.labor_name;  // Assuming you have labor_name in the response
        row.insertCell(3).textContent = payment.site_name;    // Assuming you have site_name in the response
        row.insertCell(4).textContent = payment.material_name ? payment.material_name : 'N/A';  // Optional material
        row.insertCell(5).textContent = payment.description || 'N/A';  // Optional description
        const actionsCell = row.insertCell(6);
        
        // Edit button
        const editButton = document.createElement('button');
        editButton.textContent = 'Edit';
        editButton.className = 'btn btn-primary';
        editButton.onclick = () => editPayment(payment.id);
        actionsCell.appendChild(editButton);
        
        // Delete button
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.className = 'btn btn-danger';
        deleteButton.onclick = () => deletePayment(payment.id);
        actionsCell.appendChild(deleteButton);
    });

    // Pagination
    updatePagination(payments);
}

// Update pagination controls
function updatePagination(payments) {
    const pagination = document.getElementById('payment-pagination');
    pagination.innerHTML = ''; // Clear existing pagination

    if (payments.prev) {
        const prevButton = document.createElement('button');
        prevButton.textContent = 'Previous';
        prevButton.onclick = () => loadPayments(payments.prev);
        pagination.appendChild(prevButton);
    }

    const pageInfo = document.createElement('span');
    pageInfo.textContent = `Page ${payments.current} of ${payments.totalPages}`;
    pagination.appendChild(pageInfo);

    if (payments.next) {
        const nextButton = document.createElement('button');
        nextButton.textContent = 'Next';
        nextButton.onclick = () => loadPayments(payments.next);
        pagination.appendChild(nextButton);
    }
}

// Add a new payment
async function addPayment(paymentData) {
    const response = await fetch('/payments/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(paymentData)
    });

    if (response.ok) {
        await loadPayments(); // Refresh payments after adding
    } else {
        console.error('Failed to add payment:', await response.json());
    }
}

// Delete a payment
async function deletePayment(paymentId) {
    const response = await fetch(`/payments/${paymentId}`, {
        method: 'DELETE'
    });

    if (response.ok) {
        await loadPayments(); // Refresh payments after deleting
    } else {
        console.error('Failed to delete payment:', await response.json());
    }
}

// Edit a payment
async function editPayment(paymentId) {
    const response = await fetch(`/payments/${paymentId}`);
    const payment = await response.json();
    
    document.getElementById('payment-amount').value = payment.amount;
    document.getElementById('payment-date').value = payment.date;
    document.getElementById('labor-select').value = payment.labor_id;
    document.getElementById('site-select').value = payment.site_id;
    document.getElementById('material-select').value = payment.material_name || ''; // If there's no material, set to empty
    document.getElementById('payment-description').value = payment.description || '';

    // Handle form submission for updating payment
    document.getElementById('payment-form').onsubmit = async (e) => {
        e.preventDefault();
        const updatedPaymentData = {
            amount: parseFloat(document.getElementById('payment-amount').value),
            date: document.getElementById('payment-date').value,
            labor_id: document.getElementById('labor-select').value,
            site_id: document.getElementById('site-select').value,
            material_name: document.getElementById('material-select').value,
            description: document.getElementById('payment-description').value
        };
        await updatePayment(paymentId, updatedPaymentData);
        document.getElementById('payment-form').reset();
        await loadPayments();
    };
}

// Update a payment
async function updatePayment(paymentId, paymentData) {
    const response = await fetch(`/payments/${paymentId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(paymentData)
    });

    if (response.ok) {
        await loadPayments(); // Refresh payments after updating
    } else {
        console.error('Failed to update payment:', await response.json());
    }
}

// Filter payments
function filterPayments(searchTerm) {
    const rows = document.querySelectorAll('#payment-list tbody tr');
    rows.forEach(row => {
        const cells = row.getElementsByTagName('td');
        const text = Array.from(cells).map(cell => cell.textContent.toLowerCase()).join(' ');
        row.style.display = text.includes(searchTerm.toLowerCase()) ? '' : 'none';
    });
}
