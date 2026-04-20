

🌸 FemBridge – Women's Career Portal

A full-stack web application with AI-powered job recommendations, resume analysis, and chatbot support.

---

## 🚀 Quick Start

### 1. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the Backend Server
```bash
cd backend
python app.py
```
> Server runs at: **http://localhost:5000**

### 3. Open the Frontend -
Open `frontend/index.html` in your browser directly, or serve it with:
```bash
cd frontend
python -m http.server 8080
```
> Frontend at: **http://localhost:8080**

---

## 📁 Project Structure

```
fembridge/
├── backend/
│   ├── app.py                  ← Main Flask app (entry point)
│   ├── requirements.txt
│   ├── database/
│   │   └── fembridge.db        ← Auto-created on first run
│   ├── models/
│   │   └── db_setup.py         ← Schema + seed data
│   ├── routes/
│   │   ├── auth.py             ← /register /login /logout /profile
│   │   ├── jobs.py             ← /jobs /apply /my-applications
│   │   ├── applications.py     ← /applications/status
│   │   ├── ai.py               ← /recommend
│   │   └── chatbot.py          ← /chat
│   └── utils/
│       ├── recommender.py      ← NLP skill-matching engine
│       └── resume_parser.py    ← Resume text extraction + scoring
│
└── frontend/
    ├── index.html              ← Landing page
    ├── login.html              ← Login form
    ├── register.html           ← Registration form
    ├── dashboard.html          ← User dashboard
    ├── jobs.html               ← Job listings + filters
    ├── profile.html            ← Profile editor + resume upload
    ├── css/
    │   └── style.css           ← Pink/white theme + all components
    └── js/
        ├── main.js             ← Shared utilities (API, toast, auth)
        ├── auth.js             ← Login/register handlers
        ├── jobs.js             ← Job listing + filter logic
        ├── dashboard.js        ← Dashboard data loading
        └── chatbot.js          ← Floating chatbot UI
```

---

## 🔌 API Endpoints

| Method | Endpoint            | Description                     | Auth Required |
|--------|---------------------|---------------------------------|---------------|
| POST   | /register           | Create new user account         | No            |
| POST   | /login              | Login and create session        | No            |
| POST   | /logout             | Clear session                   | No            |
| GET    | /profile            | Get current user profile        | Yes           |
| PUT    | /profile            | Update name, skills, location   | Yes           |
| GET    | /jobs               | List jobs (with filters)        | No            |
| POST   | /apply              | Apply for a job                 | Yes           |
| GET    | /my-applications    | Get user's applications         | Yes           |
| GET    | /recommend          | AI job recommendations          | Yes           |
| POST   | /resume             | Upload and analyze resume       | Yes           |
| GET    | /resume/score       | Get stored resume score         | Yes           |
| GET    | /dashboard          | Get dashboard summary stats     | Yes           |
| POST   | /chat               | Chatbot message                 | No            |

---

## ✨ Features

- **Authentication** – Register, login, session management
- **Job Listings** – Filter by location, type, keyword search
- **Location Filtering** – Shows city jobs + Remote always
- **AI Recommendations** – NLP keyword matching against user skills
- **Resume Analyzer** – Upload .pdf/.docx/.txt, get 0–100 score + tips
- **Rule-based Chatbot** – 14+ intents, floating UI on all pages
- **Dashboard** – Applied jobs, resume score ring, AI recommendations
- **Profile** – Edit name, skills (with live tag preview), location


## 🎨 Design

- **Theme:** Pink (#c2185b) + White
- **Fonts:** Playfair Display (headings) + DM Sans (body)
- **Framework:** Bootstrap 5.3
- **Responsive:** Mobile-first layout


