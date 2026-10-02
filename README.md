# CareerPath AI

CareerPath AI is a full-stack career development workspace. It combines a React
frontend with a Django REST API for authentication, career exploration,
skill-gap analysis, readiness scoring, learning roadmaps, job description
analysis, assessments, and AI-assisted mock interviews.

## Stack

- Frontend: React 18, React Router, Vite
- Backend: Django 6.1, Django REST Framework, Simple JWT
- Database: SQLite for local development
- AI integration: Google Gemini through the backend only

## Local setup

### Backend

From the repository root:

```powershell
cd backend
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Copy `backend/.env.example` to `backend/.env` and set local values:

```text
DJANGO_SECRET_KEY=replace-with-a-long-random-value
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
GEMINI_API_KEY=your-key
```

For production, set `DJANGO_DEBUG=False`, provide a unique secret
`DJANGO_SECRET_KEY`, and configure `DJANGO_ALLOWED_HOSTS` for the deployed
domains. The application refuses to start with debug disabled if the secret
key is missing.

The local SQLite database is created by Django migrations. Do not commit
`.env`, the database, or virtual-environment files.

### Frontend

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open [http://127.0.0.1:5173](http://127.0.0.1:5173). Vite proxies `/api`
requests to the Django server on port `8000`, so both servers must be running.

## Main routes

The authenticated workspace includes:

- Dashboard and profile
- Career catalog and career details
- Skill-gap analysis and readiness scores
- Learning roadmap and recommended resources
- Job description analysis and saved analyses
- Skill assessments and assessment history
- AI mock interviews and interview history

The API is available under `/api/`. Registration uses `/api/register/`, while
JWT authentication uses `/api/token/` and `/api/token/refresh/`.

Structured skills are managed through `/api/skills/` and are the source of
truth for skill gaps, readiness, recommendations, and job comparisons.
`current_skills` remains an optional free-form profile field for compatibility.
The normal `/api/careers/<id>/skill-gap/` endpoint performs only database
calculation. Gemini is called only after an authenticated user explicitly
requests `/api/careers/<id>/ai-analysis/`.

The readiness score is the percentage of required skill proficiency covered by
the user's recorded skills for a career. It is a progress indicator, not a
prediction of employment or hiring probability.

## Validation

Run the backend checks:

```powershell
cd backend
.\venv\Scripts\python.exe manage.py test
.\venv\Scripts\python.exe manage.py check
```

Build the frontend:

```powershell
cd frontend
npm run build
```

The backend test suite includes authentication, ownership, structured skills,
skill gaps, job analysis persistence, assessment validation, and privacy tests.
AI calls are mocked in tests, so they do not consume Gemini quota.
