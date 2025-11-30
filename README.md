# Smart Task Analyzer

Smart Task Analyzer is an intelligent task-ranking and prioritization system built using
**Django REST Framework (backend)** and **vanilla HTML/CSS/JS (frontend)**.
It analyzes a list of tasks using urgency, importance, effort, and dependency structure
to generate an optimal order of execution.

This project was created as part of the **Singularium Technologies Internship Assignment – 2025**.

## 🚀 Features

### ✔ Task Analysis Engine  
- Computes a **priority score (0–100)** for every task  
- Uses weighted factors:
  - Urgency (based on due date)
  - Importance (user defined 1–10)
  - Effort (estimated hours)
  - Dependency penalties  
- Detects and reports **dependency cycles**  
- Supports **multiple analysis strategies**:
  - Smart Balance
  - Fastest Wins
  - High Impact
  - Deadline Driven

### ✔ Backend (Django REST Framework)
- Endpoint: `/api/tasks/analyze/`
- Accepts task list as JSON
- Returns analyzed results as JSON
- Fully CORS-enabled
- Validations for missing/wrong fields

### ✔ Frontend
- Simple and clean interface
- Add tasks with:
  - Title
  - Due date
  - Estimated hours
  - Importance
  - Dependencies
- Choose strategy and click **Analyze**
- Results rendered with:
  - Score bars
  - Color coding (High/Medium/Low priority)
  - Full explanation breakdown

---

## 🛠 Tech Stack

| Layer | Technology |
|------|------------|
| Backend | Python, Django, DRF |
| Frontend | HTML, CSS, JavaScript |
| Communication | Fetch + JSON |
| Environment | Virtualenv |
| Deployment (optional) | Render / Railway |


