const predefinedSkills = ["Python","Java",".Net","JavaScript", "SQL", "Machine Learning", "Data Science", "Power BI", "Deep Learning","Generative AI", "TensorFlow", "React.js", "Node.js", "Vue.js"];
const skillInput = document.getElementById("skillInput");

function loadSkillsList() {
    const skillsList = document.getElementById("skillsList");
    skillsList.innerHTML = ""; // Clear existing items

    predefinedSkills.forEach(skill => {
        const skillDiv = document.createElement("div");
        skillDiv.classList.add("skill-item");
        skillDiv.textContent = skill;
        skillDiv.onclick = function () {
            addSkillTag(skill);
            skillInput.focus(); // 🔥 Keep input field active after clicking
        };
        skillsList.appendChild(skillDiv);
    });
}

// Allow typing and pressing Enter/Space to add skills
skillInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter" ) {
        event.preventDefault();
        const skill = this.value.trim();
        if (skill) {
            addSkillTag(skill);
            this.value = ""; // Clear input after adding
        }
    }
});

// Ensure input remains active
skillInput.addEventListener("focus", function () {
    this.setAttribute("placeholder", "Type and press Enter or select from the suggestions... eg: Python, PowerBI, SQL ...");
});

// Add a skill to the list
function addSkillTag(skill) {
    if (skill === "" || skills.includes(skill)) return;
    if (skills.length >= 5) {
        alert("You can only add up to 5 skills.");
        return;
    }
    skills.push(skill);
    updateSkillTags();
}

// Update the selected skill tags UI
function updateSkillTags() {
    const tagContainer = document.getElementById("tagContainer");
    tagContainer.innerHTML = ""; // Clear only the tag elements

    skills.forEach(skill => {
        const tag = document.createElement("div");
        tag.classList.add("tag");
        tag.textContent = skill;

        const removeButton = document.createElement("span");
        removeButton.classList.add("remove");
        removeButton.textContent = "×";
        removeButton.onclick = function () {
            skills = skills.filter(s => s !== skill);
            updateSkillTags();
            document.querySelectorAll(".skill-item").forEach(item => {
                if (item.textContent === skill) {
                    item.classList.remove("selected");
                }
            });
        };

        tag.appendChild(removeButton);
        tagContainer.appendChild(tag);
    });

    skillInput.focus(); // Ensure typing works even after clicking a skill
}

document.addEventListener("DOMContentLoaded", function () {
    loadSkillsList();
});


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
        body: JSON.stringify({ feedback,email})
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
       // document.getElementById("editToggleBtn").disabled = false;
    } else {
        alert("Failed to load template preview.");
    }
});

/*
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
*/

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

    // Templates that require an email
    const mandatoryEmailTemplates = ["startup", "executive", "technical"];

    data.templates.forEach(template => {
        let option = document.createElement("option");

        // Capitalize the first letter of each template name
        let formattedTemplate = template.charAt(0).toUpperCase() + template.slice(1);

        option.value = template;

        // Add a star if the template requires an email
        if (mandatoryEmailTemplates.includes(template.toLowerCase())) {
            option.textContent = `${formattedTemplate} ✨`;
            //option.style.fontWeight = "bold";
            option.setAttribute("data-bs-toggle", "tooltip");
            option.setAttribute("title", "⚠️ This template requires an email to proceed.");
        } else {
            option.textContent = formattedTemplate;
        }

        templateSelect.appendChild(option);
    });

    // Enable Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
}

// Clear email when switching to a non-premium template
document.getElementById("template").addEventListener("change", function () {
    const selectedTemplate = this.value.toLowerCase();
    const mandatoryEmailTemplates = ["startup", "executive", "technical"];
    const templateNote = document.getElementById("templateNote");
    const emailInput = document.getElementById("userEmail");

    if (mandatoryEmailTemplates.includes(selectedTemplate)) {
        templateNote.innerHTML = "⚠️ Email ID required! We promise no spam… just pure awesomeness! 😎💌";
        templateNote.style.color = "red";
    } else {
        templateNote.innerHTML = "✨ Premium templates Eg. Startup, Technical, and Executive need a little something in return—your Email ID. Just a small price for big style! 😉";
        templateNote.style.color = "gray";

        // Clear email input when switching to a non-premium template
        if (emailInput) {
            emailInput.value = "";
        }
    }
});




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
    if (event.key === "Enter") {
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
    const emailInput = document.getElementById('userEmail');
    const emailModal = new bootstrap.Modal(document.getElementById('emailCaptureModal'));

    // Templates that require mandatory email
    const mandatoryEmailTemplates = ["startup", "executive", "technical"];

    // Show the email popup for all templates
    emailModal.show();

    const confirmEmailBtn = document.getElementById('confirmEmailBtn');
    confirmEmailBtn.disabled = false; // Enable "Skip" by default

    emailInput.addEventListener("input", function() {
        if (mandatoryEmailTemplates.includes(template.toLowerCase())) {
            confirmEmailBtn.disabled = !isValidEmail(emailInput.value);
        }
    });

    confirmEmailBtn.onclick = async function() {
        const email = emailInput.value.trim();

        // If selected template requires an email and it's missing, prevent submission
        if (mandatoryEmailTemplates.includes(template.toLowerCase()) && !isValidEmail(email)) {
            alert("Try again to unlock this template with a valid email! 😊");
            emailInput.focus();
            return;
        }

        // Save email only if entered
        if (isValidEmail(email)) {
            await fetch('http://127.0.0.1:8000/capture_email/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            });
        }

        bootstrap.Modal.getInstance(document.getElementById('emailCaptureModal')).hide();
        processCoverLetter(name, jobTitle, company, template);
    };
});

function isValidEmail(email) {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(email);
}

async function fetchTotalGenerated() {
    try {
        const response = await fetch("http://127.0.0.1:8000/total_generated/");
        const data = await response.json();
        document.getElementById("totalCoverLetters").textContent = `📄 Total Cover Letters Generated: ${data.total}`;
    } catch (error) {
        console.error("Error fetching total count:", error);
    }
}


function triggerCelebration() {
    const confettiContainer = document.createElement("div");
    confettiContainer.classList.add("confetti-container");
    document.body.appendChild(confettiContainer);

    for (let i = 0; i < 100; i++) { // Increased number of confetti
        let confetti = document.createElement("div");
        confetti.classList.add("confetti");
        confetti.style.left = Math.random() * 100 + "vw";
        confetti.style.animationDuration = Math.random() * 4 + 2 + "s"; // Increased range for better effect
        confetti.style.width = Math.random() * 10 + 5 + "px"; // Varying size
        confetti.style.height = confetti.style.width;
        confetti.style.opacity = Math.random(); // Random opacity
        confetti.style.backgroundColor = `hsl(${Math.random() * 360}, 100%, 50%)`;
        confettiContainer.appendChild(confetti);
    }

    setTimeout(() => {
        confettiContainer.remove();
    }, 6000); // Confetti disappears after 6 seconds

    alert("🎉 Congratulations! Your cover letter is ready for download! 🚀");
}

async function processCoverLetter(name, jobTitle, company, template) {
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
        document.getElementById('downloadLink').style.display = 'block';

        // Trigger celebration when download is ready
        triggerCelebration();
        fetchTotalGenerated(); // 🔄 Update total count

    } else {
        alert('Failed to generate cover letter');
    }
};

window.onload = async function() {
    await logUserVisit();
    await loadJobTitlesAndCompanies();
    loadTemplates();
    showSuggestions("job_title", "job_suggestions", jobTitles);
    showSuggestions("company", "company_suggestions", companies);
    fetchTotalGenerated();  // Fetch and display total count
};
