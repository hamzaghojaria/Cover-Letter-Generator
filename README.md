# CoverZen - Cover Letter Generator 🚀

## Description
CoverZen is a web-based application designed to generate personalized cover letters effortlessly. Users can enter their details, select a template, and receive a downloadable PDF cover letter.

## Features
- 🎯 Smart suggestions for Job Titles, Companies, and Skills.
- 🎨 Multiple cover letter templates to choose from.
- 🔥 Live preview of selected templates.
- 📩 Optional email capture for premium templates.
- 🌙 Dark mode support.
- 💬 User feedback system.
- ⏬ Downloadable list of top hiring companies.

## Tech Stack
- **Frontend:** HTML, CSS (Bootstrap 5.3), JavaScript
- **Backend:** FastAPI (Python)
- **Storage:** YAML for configuration and data storage
- **PDF Generation:** ReportLab
- **WebSocket:** Live user tracking

## Installation & Setup
### Prerequisites
- Python 3.8+
- pip

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/coverzen.git
   cd coverzen
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the FastAPI backend:
   ```bash
   uvicorn main:app --reload
   ```
4. Open `index.html` in a browser or serve it via a local web server.

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/generate_cover_letter/` | POST | Generate cover letter PDF |
| `/job_titles/` | GET | Get list of job titles |
| `/companies/` | GET | Get list of companies |
| `/templates/` | GET | Get list of templates |
| `/submit_feedback/` | POST | Submit user feedback |

## Usage
1. Enter your Name, Job Title, and Company.
2. Add up to 5 Skills.
3. Choose a Template.
4. Click **Generate Cover Letter** and download the PDF.

## Screenshots
![CoverZen UI](https://your-image-link.com)

## Contributors
- [Saad Ghojaria](https://www.linkedin.com/in/saad-ghojaria/)
- [Hamza Ghojaria](https://www.linkedin.com/in/hamzaghojaria/)

