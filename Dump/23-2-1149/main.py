from fastapi import FastAPI
from pydantic import BaseModel
from fpdf import FPDF
from fastapi.responses import FileResponse
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Job Titles and Companies List
JOB_TITLES = [
    "Software Engineer", "Data Scientist", "Product Manager", "DevOps Engineer", "UX Designer",
    # Add 95 more job titles...
]

COMPANIES = [
    "Google", "Microsoft", "Amazon", "Facebook", "Tesla",
    # Add 95 more company names...
]

# Cover Letter Templates
TEMPLATES = {
    "default": """
Dear Hiring Manager,

I am writing to express my interest in the {job_title} position at {company}. With my expertise in {skills}, I have successfully contributed to projects that required innovation, problem-solving, and collaboration. I am confident that my experience and dedication will make me a valuable addition to your team.

I take pride in my ability to adapt to new challenges and drive meaningful results. My past work demonstrates my capability to handle complex problems with efficiency. I would love the opportunity to further discuss how my skills align with your company goals.

Sincerely,
{name}
""",
    "formal": """
Dear {company} Hiring Team,

I am eager to apply for the {job_title} role at {company}, as advertised. With a strong background in {skills}, I have developed a proven ability to drive success in my field.

I am particularly impressed by {company}'s commitment to excellence and innovation. I am excited about the possibility of bringing my skills to your esteemed organization and would appreciate the opportunity to discuss my qualifications in more detail.

Best regards,
{name}
""",
    "casual": """
Hey {company} Team,

I saw the {job_title} opening and immediately felt it was the perfect fit. With my background in {skills}, I thrive in dynamic and collaborative environments.

Let's set up a time to chat—I would love to discuss how I can contribute to {company}.

Cheers,  
{name}
"""
}

class CoverLetterInput(BaseModel):
    name: str
    job_title: str
    company: str
    skills: str
    template: str

def generate_pdf(content: str, filename: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, content)
    pdf.output(filename)

@app.post("/generate_cover_letter/")
def generate_cover_letter(data: CoverLetterInput):
    if data.template not in TEMPLATES:
        return {"error": "Invalid template selection"}

    cover_letter = TEMPLATES[data.template].format(
        name=data.name, job_title=data.job_title, company=data.company, skills=data.skills
    )
    filename = f"{data.name}_cover_letter.pdf"
    generate_pdf(cover_letter, filename)
    return FileResponse(filename, media_type="application/pdf", filename=filename)

@app.get("/job_titles/")
def get_job_titles():
    return {"job_titles": JOB_TITLES}

@app.get("/companies/")
def get_companies():
    return {"companies": COMPANIES}

@app.get("/templates/")
def get_templates():
    return {"templates": list(TEMPLATES.keys())}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
