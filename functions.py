import yaml 
from fpdf import FPDF
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.enums import TA_JUSTIFY




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
