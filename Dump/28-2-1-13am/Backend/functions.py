import yaml 
import os
#from fpdf import FPDF
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.enums import TA_JUSTIFY


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_job_titles():
    file_name="job_titles.yaml"
    yaml_path = os.path.join(BASE_DIR, "Services", file_name)
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
        #print("data",data)
    return data.get("job_titles", [])

def load_companies():
    file_name="companies.yaml"
    yaml_path = os.path.join(BASE_DIR, "Services", file_name)
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    return data.get("companies", [])

def load_templates():
    file_name="templates.yaml"
    yaml_path = os.path.join(BASE_DIR, "Services", file_name)
    with open(yaml_path, "r",encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("templates", {})


# def generate_pdf(content: str, filename: str):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     pdf.multi_cell(0, 8, content)
#     pdf.output(filename)



def generate_pdf(content: str, filename: str):
    # Define the PDF file
    doc = SimpleDocTemplate(filename, pagesize=A4)
    
    # Define styles
    styles = getSampleStyleSheet()
    custom_style = ParagraphStyle(
        'CustomStyle',
        parent=styles['Normal'],
        fontSize=12,
        leading=18,  # Line spacing
        spaceAfter=12,  # Space between paragraphs
        alignment=TA_JUSTIFY  # Justify text
    )
    
    # Create a paragraph with formatting
    formatted_content = Paragraph(content.replace("\n", "<br/>"), custom_style)

    # Build the PDF
    doc.build([formatted_content])

    return filename


def save_email_to_yaml(email,yaml_path):
    """Save email to a YAML file."""
    data = []
    
    # If file exists, load existing emails
    if os.path.exists(yaml_path):
        with open(yaml_path, "r") as f:
            try:
                data = yaml.safe_load(f) or []
            except yaml.YAMLError:
                data = []  # If YAML is corrupted, reset it

    # Append new email
    data.append({"email": email})

    # Write back to YAML file
    with open(yaml_path, "w") as f:
        yaml.safe_dump(data, f, default_flow_style=False)