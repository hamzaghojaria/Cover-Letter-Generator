import yaml 
from fpdf import FPDF
# Function to load job titles from YAML



def load_job_titles():
    with open("job_titles.yaml", "r") as f:
        data = yaml.safe_load(f)
    return data.get("job_titles", [])

def load_companies():
    with open("companies.yaml", "r") as f:
        data = yaml.safe_load(f)
    return data.get("companies", [])

def load_templates():
    with open("templates.yaml", "r",encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("templates", {})



def generate_pdf(content: str, filename: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, content)
    pdf.output(filename)