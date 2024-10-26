// DOM elements
const materialForm = document.getElementById('material-form');
const siteForm = document.getElementById('site-form');

const materialList = document.querySelector("#material-list tbody");
const siteList = document.querySelector("#site-list tbody");

const searchMaterialInput = document.getElementById('search-material');
const searchSiteInput = document.getElementById('search-site');

const materialPagination = document.getElementById("material-pagination");
const sitePagination = document.getElementById("site-pagination");

const searchSites = document.getElementById("search-site");
const searchMaterials = document.getElementById("search-material");



let editingMaterialId = null;
let editingSiteId = null;

let currentMaterialPage = 1;
let currentSitePage = 1;
const itemsPerPage = 10;


// Logout Functionality
document.getElementById("logout-button").addEventListener("click", () => {
    fetch("/admin/logout/", {
        method: "POST",
    }).then(() => {
        window.location.href = "/"; // Redirect to login page after logout
    });
});

// Function to fetch and load materials
async function loadMaterials(page = 1) {
    try {
        const skip = (page - 1) * itemsPerPage;
        const response = await fetch(`/materials/?skip=${skip}&limit=${itemsPerPage}`);
        if (!response.ok) throw new Error('Failed to load materials');
        const data = await response.json();
        renderMaterials(data); // Adjusted to use the correct data structure
        updatePagination(materialPagination, page, data.length, loadMaterials);
    } catch (error) {
        console.error(error);
        alert('Error loading materials');
    }
}

// Render materials
function renderMaterials(materials) {
    materialList.innerHTML = '';
    materials.forEach(material => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${material.name}</td>
            <td>${material.quantity}</td>
            <td>${material.unit}</td>
            <td>${material.site_name}</td>
            <td>${material.arrival_date}</td>
            <td>${material.transport_type}</td>
            <td>
                <button onclick="editMaterial(${material.id})">Edit</button>
                <button onclick="deleteMaterial(${material.id})">Delete</button>
            </td>
        `;
        materialList.appendChild(row);
    });
}

// Add or Update material
materialForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const materialData = {
        name: document.getElementById('material-name').value,
        quantity: parseFloat(document.getElementById('material-quantity').value),
        unit: document.getElementById('material-unit').value,
        site_id: parseInt(document.getElementById('material-site').value),
        arrival_date: document.getElementById('arrival-date').value, // Ensure this field is included
        transport_type: document.getElementById('transport-type').value 
    };
    try {
        if (editingMaterialId) {
            await updateMaterial(editingMaterialId, materialData);
        } else {
            await addMaterial(materialData);
        }
        materialForm.reset();
        editingMaterialId = null;
        loadMaterials(currentMaterialPage);
    } catch (error) {
        console.error(error);
        alert('Failed to save material');
    }
});

// Add material
async function addMaterial(material) {
    const response = await fetch('/materials/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(material)
    });
    if (!response.ok) throw new Error('Failed to add material');
    alert('Material added successfully');
}

// Update material
async function updateMaterial(id, material) {
    const response = await fetch(`/materials/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(material)
    });
    if (!response.ok) throw new Error('Failed to update material');
    alert('Material updated successfully');
}

// Delete material
async function deleteMaterial(id) {
    if (!confirm('Are you sure you want to delete this material?')) return;
    const response = await fetch(`/materials/${id}`, { method: 'DELETE' });
    if (!response.ok) throw new Error('Failed to delete material');
    alert('Material deleted successfully');
    loadMaterials(currentMaterialPage);
}

// Edit material
async function editMaterial(id) {
    try {
        const response = await fetch(`/materials/${id}`);
        if (!response.ok) throw new Error('Failed to fetch material');
        const material = await response.json();
        document.getElementById('material-name').value = material.name;
        document.getElementById('material-quantity').value = material.quantity;
        document.getElementById('material-unit').value = material.unit;
        document.getElementById('material-site').value = material.site_id;
        document.getElementById('arrival-date').value = material.arrival_date;
        document.getElementById('transport-type').value = material.transport_type;
        editingMaterialId = id;
    } catch (error) {
        console.error(error);
        alert('Failed to load material for editing');
    }
}

// Search Materials names based on both name and site name
let debounceTimers;
searchMaterials.addEventListener("input", () => {
    clearTimeout(debounceTimers);
    debounceTimers = setTimeout(() => {
        const searchTerms = searchMaterials.value.toLowerCase();  // Get the search term

        const rows = materialList.getElementsByTagName("tr");  // Get all table rows
        for (const row of rows) {
            const nameCell = row.cells[0];  // Assuming the laborer name is in the first cell
            const siteCell = row.cells[3];  // Assuming the site name is in the fifth cell
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


// Function to fetch and load sites
async function loadSites(page = 1) {
    try {
        const skip = (page - 1) * itemsPerPage;
        const response = await fetch(`/sites/?skip=${skip}&limit=${itemsPerPage}`);
        
        if (!response.ok) throw new Error('Failed to load sites');

        const data = await response.json();

        // Assuming data is directly an array of sites, adjust if your response structure is different
        renderSites(data); // Adjusted to use the correct data structure

        // Update pagination
        const totalSitesResponse = await fetch('/sites/'); // Fetch the total count of sites for pagination
        const totalSitesData = await totalSitesResponse.json();
        updatePagination(sitePagination, page, totalSitesData.length, loadSites);

    } catch (error) {
        console.error(error);
        alert('Error loading sites');
    }
}

// Function to fetch and load sites into the dropdown
async function loadSitesIntoDropdown() {
    try {
        const response = await fetch('/sites/'); // Call your API endpoint
        if (!response.ok) throw new Error('Failed to load sites');
        const sites = await response.json();

        const materialSiteSelect = document.getElementById('material-site');
        materialSiteSelect.innerHTML = ''; // Clear existing options

        sites.forEach(site => {
            const option = document.createElement('option');
            option.value = site.id; // Assuming the site has an 'id' property
            option.textContent = site.name; // Assuming the site has a 'name' property
            materialSiteSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading sites for materials:', error);
        alert('Error loading sites');
    }
}



// Render sites
function renderSites(sites) {
    siteList.innerHTML = '';
    sites.forEach(site => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${site.name}</td>
            <td>${site.location}</td>
            <td>
                <button onclick="editSite(${site.id})">Edit</button>
                <button onclick="deleteSite(${site.id})">Delete</button>
            </td>
        `;
        siteList.appendChild(row);
    });
}

// Add or Update site
siteForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const siteData = {
        name: document.getElementById('site-name').value,
        location: document.getElementById('site-location').value,
    };
    try {
        if (editingSiteId) {
            await updateSite(editingSiteId, siteData);
        } else {
            await addSite(siteData);
        }
        siteForm.reset();
        editingSiteId = null;
        loadSites(currentSitePage);
    } catch (error) {
        console.error(error);
        alert('Failed to save site');
    }
});

// Add site
async function addSite(site) {
    const response = await fetch('/sites/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(site)
    });
    if (!response.ok) throw new Error('Failed to add site');
    alert('Site added successfully');
}

// Update site
async function updateSite(id, site) {
    const response = await fetch(`/sites/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(site)
    });
    if (!response.ok) throw new Error('Failed to update site');
    alert('Site updated successfully');
}

// Delete site
async function deleteSite(id) {
    if (!confirm('Are you sure you want to delete this site?')) return;
    const response = await fetch(`/sites/${id}`, { method: 'DELETE' });
    if (!response.ok) throw new Error('Failed to delete site');
    alert('Site deleted successfully');
    loadSites(currentSitePage);
}

// Edit site
async function editSite(id) {
    try {
        const response = await fetch(`/sites/${id}`);
        if (!response.ok) throw new Error('Failed to fetch site');
        const site = await response.json();
        document.getElementById('site-name').value = site.name;
        document.getElementById('site-location').value = site.location;
        editingSiteId = id;
    } catch (error) {
        console.error(error);
        alert('Failed to load site for editing');
    }
}

// Search Sites
let debounceTimer;
searchSites.addEventListener("input", () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        const searchTerm = searchSites.value.toLowerCase();
        const rows = siteList.getElementsByTagName("tr");
        for (const row of rows) {
            const name = row.cells[0].textContent.toLowerCase();
            row.style.display = name.includes(searchTerm) ? "" : "none";
        }
    }, 300);
});

// Function to update pagination
function updatePagination(paginationElement, currentPage, totalItems, loadFunction) {
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    paginationElement.innerHTML = '';

    const prevButton = document.createElement('button');
    prevButton.innerText = 'Previous';
    prevButton.disabled = currentPage === 1;
    prevButton.onclick = () => loadFunction(currentPage - 1);
    paginationElement.appendChild(prevButton);

    const pageInfo = document.createElement('span');
    pageInfo.innerText = `Page ${currentPage} of ${totalPages}`;
    paginationElement.appendChild(pageInfo);

    const nextButton = document.createElement('button');
    nextButton.innerText = 'Next';
    nextButton.disabled = currentPage === totalPages;
    nextButton.onclick = () => loadFunction(currentPage + 1);
    paginationElement.appendChild(nextButton);
}

// Load initial materials and sites
loadMaterials(currentMaterialPage);
loadSites(currentSitePage);
loadSitesIntoDropdown();
