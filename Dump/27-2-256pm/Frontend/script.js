document.getElementById("feedbackToggle").addEventListener("click", function() {
    const form = document.getElementById("feedbackFormContainer");
    form.style.display = form.style.display === "block" ? "none" : "block";
});

document.getElementById("feedbackForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    const email = document.getElementById("feedbackEmail").value;
    const feedback = document.getElementById("feedbackText").value;

    const response = await fetch("http://127.0.0.1:8000/submit_feedback/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, feedback })
    });

    if (response.ok) {
        document.getElementById("feedbackMessage").textContent = "Thank you for your feedback!";
        document.getElementById("feedbackForm").reset();
        setTimeout(() => {
            document.getElementById("feedbackFormContainer").style.display = "none";
        }, 2000);
    } else {
        document.getElementById("feedbackMessage").textContent = "Error submitting feedback.";
    }
});


document.getElementById("previewBtn").addEventListener("click", async function() {
    const template = document.getElementById("template").value;

    if (!template) {
        alert("Please select a template.");
        return;
    }

    const response = await fetch(`http://127.0.0.1:8000/template_preview/?template=${template}`);
    if (response.ok) {
        const data = await response.json();
        document.getElementById("previewContent").innerHTML = data.preview;
        document.getElementById("templatePreview").style.display = "block";
        document.getElementById("editToggleBtn").disabled = false;
    } else {
        alert("Failed to load template preview.");
    }
});

document.getElementById("editToggleBtn").addEventListener("click", function() {
    const editArea = document.getElementById("editContent");
    const previewText = document.getElementById("previewContent").innerHTML;

    if (editArea.style.display === "none") {
        editArea.value = previewText;
        editArea.style.display = "block";
        this.textContent = "✅ Save Edits";
    } else {
        document.getElementById("previewContent").innerHTML = editArea.value;
        editArea.style.display = "none";
        this.textContent = "✏️ Enable Editing";
    }
});

document.addEventListener("DOMContentLoaded", function() {
    const themeToggle = document.getElementById("themeToggle");
    const root = document.documentElement;
    const form = document.getElementById("coverLetterForm");
    const currentTheme = localStorage.getItem("theme") || "light";

    root.setAttribute("data-bs-theme", currentTheme);
    updateButton(currentTheme);

    themeToggle.addEventListener("click", function(event) {
        event.preventDefault(); // Prevent form validation triggering
        const newTheme = root.getAttribute("data-bs-theme") === "light" ? "dark" : "light";
        root.setAttribute("data-bs-theme", newTheme);
        localStorage.setItem("theme", newTheme);
        updateButton(newTheme);
    });

    function updateButton(theme) {
        if (theme === "dark") {
            themeToggle.innerHTML = '<i class="bi bi-sun"></i> Light Mode';
        } else {
            themeToggle.innerHTML = '<i class="bi bi-moon"></i> Dark Mode';
        }
    }
});


async function logUserVisit() {
    try {
        await fetch("http://127.0.0.1:8000/log_visit/");
        console.log("User visit logged successfully.");
    } catch (error) {
        console.error("Error logging user visit:", error);
    }
}

// Enable Bootstrap Tooltip
document.addEventListener("DOMContentLoaded", function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

const userCountElement = document.getElementById("user-count");
const ws = new WebSocket("ws://127.0.0.1:8000/ws/live_users");

ws.onmessage = function(event) {
    userCountElement.textContent = event.data.replace("Live Users: ", "");
};

ws.onerror = function() {
    userCountElement.textContent = "Error!";
};

ws.onclose = function() {
    userCountElement.textContent = "Disconnected";
};


let jobTitles = [];
let companies = [];
let skills = [];

async function loadJobTitlesAndCompanies() {
    const jobTitleResponse = await fetch("http://127.0.0.1:8000/job_titles/");
    const companyResponse = await fetch("http://127.0.0.1:8000/companies/");

    jobTitles = (await jobTitleResponse.json()).job_titles;
    companies = (await companyResponse.json()).companies;
}

function showSuggestions(inputId, suggestionsId, dataList) {
    const input = document.getElementById(inputId);
    const suggestionsDiv = document.getElementById(suggestionsId);

    input.addEventListener("input", function() {
        const searchText = this.value.toLowerCase();
        suggestionsDiv.innerHTML = "";

        if (searchText.length === 0) {
            return;
        }

        const filteredList = dataList.filter(item => item.toLowerCase().includes(searchText)).slice(0, 5);

        filteredList.forEach(item => {
            let div = document.createElement("div");
            div.classList.add("suggestion-item");
            div.textContent = item;
            div.onclick = function() {
                input.value = item;
                suggestionsDiv.innerHTML = "";
            };
            suggestionsDiv.appendChild(div);
        });
    });

    input.addEventListener("blur", function() {
        setTimeout(() => {
            suggestionsDiv.innerHTML = "";
        }, 200);
    });
}

async function loadTemplates() {
    const response = await fetch("http://127.0.0.1:8000/templates/");
    const data = await response.json();
    const templateSelect = document.getElementById("template");
    templateSelect.innerHTML = "";

    data.templates.forEach(template => {
        let option = document.createElement("option");
        option.value = template;
        option.textContent = template.charAt(0).toUpperCase() + template.slice(1);
        templateSelect.appendChild(option);
    });
}

function addSkillTag(skill) {
    if (skill.trim() === "" || skills.includes(skill)) return;
    if (skills.length >= 5) {
        alert("You can only add up to 5 skills.");
        return;
    }
    skills.push(skill);

    const tagContainer = document.getElementById("tagContainer");
    const tag = document.createElement("div");
    tag.classList.add("tag");
    tag.textContent = skill;

    const removeButton = document.createElement("span");
    removeButton.classList.add("remove");
    removeButton.textContent = "×";
    removeButton.onclick = function() {
        tagContainer.removeChild(tag);
        skills = skills.filter(s => s !== skill);
    };

    tag.appendChild(removeButton);
    tagContainer.insertBefore(tag, document.getElementById("skillInput"));
    document.getElementById("skillInput").value = "";
}

document.getElementById("skillInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        addSkillTag(this.value);
    }
});



document.getElementById('coverLetterForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    document.getElementById('loader').style.display = 'block';
    document.getElementById('downloadLink').style.display = 'none';

    const name = document.getElementById('name').value;
    const jobTitle = document.getElementById('job_title').value;
    const company = document.getElementById('company').value;
    const template = document.getElementById('template').value;

    const response = await fetch('http://127.0.0.1:8000/generate_cover_letter/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name,
            job_title: jobTitle,
            company,
            skills: skills.join(", "),
            template
        })
    });

    document.getElementById('loader').style.display = 'none';

    if (response.ok) {
        const blob = await response.blob();
        const link = document.getElementById('pdfLink');
        link.href = URL.createObjectURL(blob);
        link.download = `${name}_cover_letter.pdf`;
        
        // Show email capture modal before revealing download link
        const emailModal = new bootstrap.Modal(document.getElementById('emailCaptureModal'));
        emailModal.show();

        document.getElementById('confirmEmailBtn').replaceWith(document.getElementById('confirmEmailBtn').cloneNode(true));
        document.getElementById('confirmEmailBtn').addEventListener('click', async function() {
            const emailInput = document.getElementById('userEmail');
            const email = emailInput.value.trim();
    
            // Email validation
            const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    
            if (email && !emailRegex.test(email)) {
                alert("❌ Please enter a valid email address.");
                emailInput.focus();
                return;
            }
    
            if (email) {
                await fetch('http://127.0.0.1:8000/capture_email/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email })
                });
            }
    
            bootstrap.Modal.getInstance(document.getElementById('emailCaptureModal')).hide();
            document.getElementById('downloadLink').style.display = 'block';
        });
    } else {
        alert('Failed to generate cover letter');
    }
});

window.onload = async function() {
    await logUserVisit();
    await loadJobTitlesAndCompanies();
    loadTemplates();
    showSuggestions("job_title", "job_suggestions", jobTitles);
    showSuggestions("company", "company_suggestions", companies);
};