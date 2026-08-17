const API_URL = "/api/application";

async function loadApplications() {
    try {
        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error("Failed to fetch applications");
        }

        const applications = await response.json();

        console.log("Applications received:", applications);

        displayApplications(applications);

    } catch (error) {
        console.error("Error loading applications:", error);
    }
}


function displayApplications(applications) {

    const table = document.getElementById("applicationsTable");

    table.innerHTML = "";

    if (applications.length === 0) {
        table.innerHTML = `
            <tr>
                <td colspan="6" style="text-align: center;">
                    No applications found.
                </td>
            </tr>
        `;

        return;
    }

    applications.forEach(application => {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${application.company}</td>

            <td>${application.role}</td>

            <td>${application.date_applied}</td>

            <td>${application.status}</td>

            <td>
                ${
                    application.job_link
                    ? `<a href="${application.job_link}" target="_blank">View Job</a>`
                    : "N/A"
                }
            </td>

            <td>
                <button class="action-btn edit-btn">
                    Edit
                </button>

                <button class="action-btn delete-btn">
                    Delete
                </button>
            </td>
        `;

        table.appendChild(row);
    });
}


loadApplications();

const applicationForm = document.getElementById("applicationForm");

applicationForm.addEventListener("submit", async function(event) {

    event.preventDefault();

    const company = document.getElementById("company").value;
    const role = document.getElementById("role").value;
    const dateApplied = document.getElementById("dateApplied").value;
    const status = document.getElementById("status").value;
    const jobLink = document.getElementById("jobLink").value;
    const notes = document.getElementById("notes").value;

    const applicationData = {
        company: company,
        role: role,
        date_applied: dateApplied,
        status: status,
        job_link: jobLink,
        notes: notes
    };

    try {

        const response = await fetch(API_URL, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(applicationData)
        });

        if (!response.ok) {
            throw new Error("Failed to add application");
        }

        const result = await response.json();

        console.log("Application added:", result);

        applicationForm.reset();

        loadApplications();

    } catch (error) {

        console.error("Error adding application:", error);

    }

});