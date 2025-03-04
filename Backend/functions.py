import yaml 
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.enums import TA_JUSTIFY

####################################################### Main Work - Start ###########################################################
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_pdf(content: str, filename: str):
    try:
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
    except Exception as e:
        return { "An Error has occurred in generate_pdf ": str(e)}

def load_job_titles():
    try:
        file_name="job_titles.yaml"
        yaml_path = os.path.join(BASE_DIR, "Services", file_name)
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)
            #print("data",data)
        return data.get("job_titles", [])
    except Exception as e:
        return { "An Error has occurred in load_job_titles ": str(e)}

def load_companies():
    try:
        file_name="companies.yaml"
        yaml_path = os.path.join(BASE_DIR, "Services", file_name)
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)
        return data.get("companies", [])
    except Exception as e:
        return { "An Error has occurred in load_companies ": str(e)}

def load_templates():
    try:
        file_name="templates.yaml"
        yaml_path = os.path.join(BASE_DIR, "Services", file_name)
        with open(yaml_path, "r",encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data.get("templates", {})
    except Exception as e:
        return { "An Error has occurred in load_templates ": str(e)}

def save_email_to_yaml(email,yaml_path):
    try:
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
    except Exception as e:
        return { "An Error has occurred in save_email_to_yaml ": str(e)}


def save_feedback_to_yaml(feedback,email,yaml_path):
    try:    
        """Save feedback to a YAML file."""
        data = []
        
        # If file exists, load existing emails
        if os.path.exists(yaml_path):
            with open(yaml_path, "r") as f:
                try:
                    data = yaml.safe_load(f) or []
                except yaml.YAMLError:
                    data = []  # If YAML is corrupted, reset it

        # Append new email
        data.append({"feedback": feedback,"email": email})

        # Write back to YAML file
        with open(yaml_path, "w") as f:
            yaml.safe_dump(data, f, default_flow_style=False)
    except Exception as e:
            return { "An Error has occurred in save_feedback_to_yaml ": str(e)}

####################################################### Main Work - End ###########################################################