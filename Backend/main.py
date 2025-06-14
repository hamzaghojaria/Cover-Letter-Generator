from fastapi import FastAPI
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from pydantic import BaseModel
from fastapi.responses import FileResponse,HTMLResponse
import uvicorn
import os, requests
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import yaml 
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from Backend import functions as coverletter_proc
#import functions as coverletter_proc

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from the "Frontend" directory
app.mount("/static", StaticFiles(directory="Frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("Frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()

######################## Job Title Add & Delete - Start ###############################
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class JobTitleInput(BaseModel):
    title: str

@app.post("/add_job_title/")
def add_job_title(data: JobTitleInput):
    try:
        file_name="job_titles.yaml"
        yaml_path = os.path.join(BASE_DIR, "Services", file_name)
        job_titles = coverletter_proc.load_job_titles()
        if data.title in job_titles:
            return {"error": "Job title already exists"}

        job_titles.append(data.title)
        with open(yaml_path, "w") as f:
            yaml.safe_dump({"job_titles": job_titles}, f)

        return {"message": f"Job title '{data.title}' added successfully"}
    except Exception as e:
        return { "An Error has occurred in add_job_title ": str(e)}

@app.delete("/delete_job_title/")
def delete_job_title(data: JobTitleInput):
    try:
        job_titles = coverletter_proc.load_job_titles()
        file_name="job_titles.yaml"
        yaml_path = os.path.join(BASE_DIR, "Services", file_name)
        if data.title not in job_titles:
            return {"error": "Job title not found"}

        job_titles.remove(data.title)

        with open(yaml_path, "w") as f:
            yaml.safe_dump({"job_titles": job_titles}, f)

        return {"message": f"Job title '{data.title}' deleted successfully"}
    except Exception as e:
        return { "An Error has occurred in delete_job_title ": str(e)}
############################ Job Title Add & Delete - End  ###########################


######################## Companies Add & Delete - Start ###############################
class CompaniesInput(BaseModel):
    title: str

@app.post("/add_companies/")
def add_companies(data: CompaniesInput):
    try:
        file_name="companies.yaml"
        yaml_path = os.path.join(BASE_DIR, "Services", file_name)
        companies = coverletter_proc.load_companies()
        if data.title in companies:
            return {"error": "Companies already exists"}

        companies.append(data.title)

        with open(yaml_path, "w") as f:
            yaml.safe_dump({"companies": companies}, f)

        return {"message": f"companies '{data.title}' added successfully"}
    except Exception as e:
        return { "An Error has occurred in add_companies ": str(e)}

@app.delete("/delete_companies/")
def delete_companies(data: CompaniesInput):
    try:
        companies = coverletter_proc.load_companies()
        file_name="companies.yaml"
        yaml_path = os.path.join(BASE_DIR, "Services", file_name)
        if data.title not in companies:
            return {"error": "Job title not found"}

        companies.remove(data.title)

        with open(yaml_path, "w") as f:
            yaml.safe_dump({"companies": companies}, f)

        return {"message": f"Companies '{data.title}' deleted successfully"}
    except Exception as e:
        return { "An Error has occurred in delete_companies ": str(e)}

############################ Companies Title Add & Delete - End  ###########################

############################ Live Users - Start  ###########################
# Set to track active WebSocket connections
active_connections = set()

async def broadcast_user_count():
    user_count = len(active_connections)
    for connection in active_connections:
        await connection.send_text(f"Live Users: {user_count}")

@app.websocket("/ws/live_users")
async def websocket_endpoint(websocket: WebSocket):
    try:    
        await websocket.accept()
        active_connections.add(websocket)
        await broadcast_user_count()

        try:
            while True:
                await websocket.receive_text()  # Keep connection alive
        except WebSocketDisconnect:
            active_connections.remove(websocket)
            await broadcast_user_count()
    except Exception as e:
        return { "An Error has occurred in websocket_endpoint ": str(e)}


############################ Live Users - End  ###########################


############################ Daily Users - Start  ###########################

# Load user data from a YAML file
def load_user_data():
    try:
        file_name="daily_users.yaml"
        yaml_path = os.path.join(BASE_DIR, "Services", file_name)
        if os.path.exists(yaml_path):
            with open(yaml_path, "r") as f:
                return yaml.safe_load(f) or {}
        return {}
    except Exception as e:
        return { "An Error has occurred in load_user_data ": str(e)}


# Save user data to a YAML file
def save_user_data(user_data):
    try:
        file_name="daily_users.yaml"
        yaml_path = os.path.join(BASE_DIR, "Services", file_name)
        with open(yaml_path, "w") as f:
            yaml.safe_dump(user_data, f, default_flow_style=False)
    except Exception as e:
        return { "An Error has occurred in save_user_data ": str(e)}

# Function to get geolocation & network info
def get_geolocation(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")  # Using ipinfo.io
        if response.status_code == 200:
            data = response.json()
            return {
                "country": data.get("country", "Unknown"),
                "region": data.get("region", "Unknown"),
                "city": data.get("city", "Unknown"),
                "isp": data.get("org", "Unknown"),  # Organization (ISP)
            }
    except Exception as e:
        print(f"Error fetching geolocation in get_geolocation: {e}")  # Debugging
    return {"country": "Unknown", "region": "Unknown", "city": "Unknown", "isp": "Unknown"}

# Function to log user data
def log_user(request: Request):
    try:
        user_data = load_user_data()
        day = datetime.now().strftime("%Y-%m-%d")

        ip = request.client.host or "Unknown"
        user_agent = request.headers.get("user-agent", "Unknown")

        # Fetch geolocation details
        geo_info = get_geolocation(ip)

        # Ensure day exists in dictionary
        if day not in user_data:
            user_data[day] = {}

        # Store user data (track visits separately)
        if ip not in user_data[day]:
            user_data[day][ip] = {
                "visits": 1,
                "user_agent": user_agent,
                "network": geo_info["isp"],
                "country": geo_info["country"],
                "region": geo_info["region"],
                "city": geo_info["city"],
            }
        else:
            user_data[day][ip]["visits"] += 1  # Increment visit count

        save_user_data(user_data)
    except Exception as e:
        return { "An Error has occurred in log_user ": str(e)}

# API to log a visit
@app.get("/log_visit/")
def log_visit(request: Request):
    try:
        log_user(request)
        return {"message": "User logged successfully"}
    except Exception as e:
        return { "An Error has occurred in log_visit ": str(e)}


# API to get daily users and visits
@app.get("/daily_users/")
def get_daily_users():
    try:
        user_data = load_user_data()
        day = datetime.now().strftime("%Y-%m-%d")
        total_users = len(user_data.get(day, {}))
        total_visits = sum(user["visits"] for user in user_data.get(day, {}).values())
        return {"unique_users": total_users, "total_visits": total_visits, "details": user_data.get(day, {})}
    except Exception as e:
        return { "An Error has occurred in get_daily_users ": str(e)}


############################ Daily Users - End  ###########################


####################################################### Main Work - Start ###########################################################
class CoverLetterInput(BaseModel):
    name: str
    job_title: str
    company: str
    skills: str
    template: str


@app.post("/generate_cover_letter/")
def generate_cover_letter(data: CoverLetterInput):
    try:
        TEMPLATES = coverletter_proc.load_templates()  # Reload templates dynamically
        if data.template not in TEMPLATES:
            return {"error": "Invalid template selection"}

        cover_letter = TEMPLATES[data.template].format(
            name=data.name, job_title=data.job_title, company=data.company, skills=data.skills)

        filename = f"{data.name}_cover_letter.pdf"
        coverletter_proc.generate_pdf(cover_letter, filename)
        count = coverletter_proc.load_count() + 1  # Increment count
        coverletter_proc.save_count(count)
        return FileResponse(filename, media_type="application/pdf", filename=filename)
    except Exception as e:
        return { "An Error has occurred in generate_cover_letter ": str(e)}


@app.get("/job_titles/")
def get_job_titles():
    try:
        return {"job_titles": coverletter_proc.load_job_titles()}
    except Exception as e:
            return { "An Error has occurred in get_job_titles ": str(e)}

@app.get("/companies/")
def get_companies():
    try:
        return {"companies": coverletter_proc.load_companies()}
    except Exception as e:
            return { "An Error has occurred in get_companies ": str(e)}

@app.get("/templates/")
def get_templates():
    try:
        return {"templates": list(coverletter_proc.load_templates().keys())}
    except Exception as e:
            return { "An Error has occurred in get_templates ": str(e)}

@app.get("/template_preview/")
def template_preview(template: str):
    try:
        TEMPLATES = coverletter_proc.load_templates()
        if template not in TEMPLATES:
            return {"error": "Invalid template selection"}
        Preview_template = TEMPLATES[template].format(
            name="John",
            job_title="Software Engineer",
            company="Microsoft",
            skills="Python, React, PowerBI")
        return {"preview": Preview_template}
    except Exception as e:
        return { "An Error has occurred in template_preview ": str(e)}


class EmailCapture(BaseModel):
    email: EmailStr  # Ensures only valid email formats are accepted

@app.post("/capture_email/")
async def capture_email(data: EmailCapture):
    try:
        file_name="emails.yaml"
        yaml_path = os.path.join(BASE_DIR, "Services", file_name)
        coverletter_proc.save_email_to_yaml(data.email,yaml_path)
        return {"message": "Email captured successfully"}
    except Exception as e:
        return { "An Error has occurred in capture_email ": str(e)}
    

class FeedbackInput(BaseModel):
    feedback: str
    email: EmailStr


@app.post("/submit_feedback/")
async def submit_feedback(data: FeedbackInput):
    try:
        file_name="feedback.yaml"
        yaml_path = os.path.join(BASE_DIR, "Services", file_name)
        coverletter_proc.save_feedback_to_yaml( data.feedback,data.email,yaml_path)
        return {"message": "Feedback submitted successfully"}
    except Exception as e:
        return {"error": f"An error occurred in submit_feedback: {str(e)}"}



@app.get("/download_companies/") #Api to download companies sheet 
def download_companies():
    try:
        file_name="companies.xlsx"
        file_path = os.path.join(BASE_DIR, "Services", file_name)

        if not os.path.exists(file_path):
            return {"error": "File not found. Please upload the correct file."}

        return FileResponse(path=file_path, filename="companies.xlsx", media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        return { "An Error has occurred in download_companies ": str(e)}


@app.get("/total_generated/") # API to get total cover letters generated
def total_generated():
    return {"total": coverletter_proc.load_count()}


####################################################### Main Work - End ###########################################################

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
