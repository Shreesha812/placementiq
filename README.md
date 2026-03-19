# PlacementIQ 🎯

> AI-powered placement intelligence platform for students

PlacementIQ analyzes your resume against job descriptions and gives you a placement readiness score, skill gap analysis, and a personalized learning roadmap — powered by a multi-layer scoring engine and Llama 3.

## 🔗 Live Demo
**[placementiq on Vercel](https://frontend-roan-nu-76.vercel.app)**

## ✨ Features
- **Resume Parsing** — Upload your PDF resume and extract skills, projects, and education automatically
- **JD Analysis** — Paste any job description and get an instant match score
- **4-Component Scoring Engine** — Skill match, experience weight, project relevance, keyword context
- **AI Insights** — Powered by Llama 3 via Groq for personalized recommendations
- **Learning Roadmap** — Prioritized list of skills to learn with resources and time estimates
- **Resume Tips** — Specific suggestions to improve your resume for the role

## 🛠 Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15, TypeScript, Tailwind CSS, Recharts |
| Backend | FastAPI, Python 3.11, SQLAlchemy (async) |
| Database | PostgreSQL + pgvector |
| AI/LLM | Llama 3 via Groq API |
| NLP | TF-IDF, scikit-learn, custom skill taxonomy (500+ skills) |
| Auth | JWT + bcrypt |
| Deployment | Railway (backend) + Vercel (frontend) |

## 🏗 Architecture
```
Resume PDF → Text Extraction (PyMuPDF)
           → Section Parser (skills, experience, projects, education)
           → Skill Extractor (500+ canonical skills taxonomy)
           → Scoring Engine (weighted 4-component algorithm)
           → Groq LLM (insights, roadmap, tips)
           → Results Dashboard
```

## 🚀 Running Locally

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 17+
- pgvector

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # fill in your values
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev
```

## 📊 Scoring Algorithm
```
Score = 0.40 × skill_match
      + 0.20 × experience_weight
      + 0.20 × project_relevance
      + 0.20 × keyword_context
```

## 👨‍💻 Author
**Shreesha H S** — [GitHub](https://github.com/Shreesha812)

## 📄 License
MIT
