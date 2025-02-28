from fastapi import FastAPI
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from pydantic import BaseModel
from fpdf import FPDF
from fastapi.responses import FileResponse
import uvicorn
import os, requests
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import yaml 
import functions as coverletter_proc

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


######################## Job Title Add & Delete - Start ###############################
class JobTitleInput(BaseModel):
    title: str

@app.post("/add_job_title/")
def add_job_title(data: JobTitleInput):
    job_titles = coverletter_proc.load_job_titles()
    if data.title in job_titles:
        return {"error": "Job title already exists"}

    job_titles.append(data.title)
    
    with open("job_titles.yaml", "w") as f:
        yaml.safe_dump({"job_titles": job_titles}, f)

    return {"message": f"Job title '{data.title}' added successfully"}

@app.delete("/delete_job_title/")
def delete_job_title(data: JobTitleInput):
    job_titles = coverletter_proc.load_job_titles()
    if data.title not in job_titles:
        return {"error": "Job title not found"}

    job_titles.remove(data.title)

    with open("job_titles.yaml", "w") as f:
        yaml.safe_dump({"job_titles": job_titles}, f)

    return {"message": f"Job title '{data.title}' deleted successfully"}
############################ Job Title Add & Delete - End  ###########################


######################## Companies Add & Delete - Start ###############################
class CompaniesInput(BaseModel):
    title: str

@app.post("/add_companies/")
def add_companies(data: CompaniesInput):
    companies = coverletter_proc.load_companies()
    if data.title in companies:
        return {"error": "Companies already exists"}

    companies.append(data.title)
    
    with open("companies.yaml", "w") as f:
        yaml.safe_dump({"companies": companies}, f)

    return {"message": f"companies '{data.title}' added successfully"}

@app.delete("/delete_companies/")
def delete_companies(data: CompaniesInput):
    companies = coverletter_proc.load_companies()
    if data.title not in companies:
        return {"error": "Job title not found"}

    companies.remove(data.title)

    with open("companies.yaml", "w") as f:
        yaml.safe_dump({"companies": companies}, f)

    return {"message": f"Companies '{data.title}' deleted successfully"}
############################ Companies Title Add & Delete - End  ###########################

############################ Live Users - Start  ###########################
# Set to track active WebSocket connections
active_connections = set()

@app.websocket("/ws/live_users")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    await broadcast_user_count()

    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        await broadcast_user_count()

async def broadcast_user_count():
    user_count = len(active_connections)
    for connection in active_connections:
        await connection.send_text(f"Live Users: {user_count}")

############################ Live Users - End  ###########################


############################ Monthly Users - Start  ###########################

# Load user data from a YAML file
def load_user_data():
    if os.path.exists("monthly_users.yaml"):
        with open("monthly_users.yaml", "r") as f:
            return yaml.safe_load(f) or {}
    return {}

# Save user data to a YAML file
def save_user_data(user_data):
    with open("monthly_users.yaml", "w") as f:
        yaml.safe_dump(user_data, f, default_flow_style=False)

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
        print(f"Error fetching geolocation: {e}")  # Debugging
    return {"country": "Unknown", "region": "Unknown", "city": "Unknown", "isp": "Unknown"}

# Function to log user data
def log_user(request: Request):
    user_data = load_user_data()
    month = datetime.now().strftime("%Y-%m")

    ip = request.client.host or "Unknown"
    user_agent = request.headers.get("user-agent", "Unknown")

    # Fetch geolocation details
    geo_info = get_geolocation(ip)

    # Ensure month exists in dictionary
    if month not in user_data:
        user_data[month] = {}

    # Store user data (track visits separately)
    if ip not in user_data[month]:
        user_data[month][ip] = {
            "visits": 1,
            "user_agent": user_agent,
            "network": geo_info["isp"],
            "country": geo_info["country"],
            "region": geo_info["region"],
            "city": geo_info["city"],
        }
    else:
        user_data[month][ip]["visits"] += 1  # Increment visit count

    save_user_data(user_data)

# API to log a visit
@app.get("/log_visit/")
def log_visit(request: Request):
    log_user(request)
    return {"message": "User logged successfully"}

# API to get monthly users and visits
@app.get("/monthly_users/")
def get_monthly_users():
    user_data = load_user_data()
    month = datetime.now().strftime("%Y-%m")

    total_users = len(user_data.get(month, {}))
    total_visits = sum(user["visits"] for user in user_data.get(month, {}).values())

    return {"unique_users": total_users, "total_visits": total_visits, "details": user_data.get(month, {})}


############################ Monthly Users - End  ###########################

####################################################### Main Work - Start ###########################################################
class CoverLetterInput(BaseModel):
    name: str
    job_title: str
    company: str
    skills: str
    template: str


@app.post("/generate_cover_letter/")
def generate_cover_letter(data: CoverLetterInput):
    TEMPLATES = coverletter_proc.load_templates()  # Reload templates dynamically
    if data.template not in TEMPLATES:
        return {"error": "Invalid template selection"}

    cover_letter = TEMPLATES[data.template].format(
        name=data.name, job_title=data.job_title, company=data.company, skills=data.skills)

    filename = f"{data.name}_cover_letter.pdf"
    coverletter_proc.generate_pdf(cover_letter, filename)
    return FileResponse(filename, media_type="application/pdf", filename=filename)


@app.get("/job_titles/")
def get_job_titles():
    return {"job_titles": coverletter_proc.load_job_titles()}

@app.get("/companies/")
def get_companies():
    return {"companies": coverletter_proc.load_companies()}

@app.get("/templates/")
def get_templates():
    return {"templates": list(coverletter_proc.load_templates().keys())}

@app.get("/template_preview/")
def template_preview(template: str):
    TEMPLATES = coverletter_proc.load_templates()
    if template not in TEMPLATES:
        return {"error": "Invalid template selection"}

    return {"preview": TEMPLATES[template]}

####################################################### Main Work - End ###########################################################

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
