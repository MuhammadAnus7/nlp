# AI-Powered Complaint Management System (Educational Organization)

Production-style Flask application for complaint routing, priority detection, query answering, auto-retraining, escalations, and analytics.

## Features
- Complaint submission with AI department detection (spaCy + scikit-learn).
- Priority detection using urgent keywords + sentiment (TextBlob + VADER).
- Query answering using semantic similarity (Sentence Transformers).
- SQLite DB with complaints, queries, departments, feedback, logs, model_versions, retraining_queue, escalation history.
- Admin panel for filtering and resolution.
- Analytics dashboard with Chart.js visualizations.
- Auto-learning pipeline: complaint resolutions feed retraining queue.
- Retraining triggers:
  - 100 queued records
  - weekly scheduled retrain
- Escalation checks:
  - 8 hours -> Senior Department
  - 24 hours -> Management

## Project Structure
```
.
├── app.py
├── requirements.txt
├── datasets/
├── database/
│   └── db.py
├── ml_models/
│   ├── complaint_classifier.py
│   ├── query_answering.py
│   └── sentiment_model.py
├── services/
│   ├── complaint_service.py
│   ├── data_loader_service.py
│   ├── escalation_service.py
│   ├── log_service.py
│   ├── priority_service.py
│   └── query_service.py
├── retraining/
│   └── auto_retrainer.py
├── analytics/
│   └── analytics_service.py
├── utils/
│   └── config.py
├── templates/
│   ├── index.html
│   ├── admin.html
│   └── dashboard.html
└── static/js/
    ├── main.js
    ├── admin.js
    └── dashboard.js
```

## Dataset Expectations
- `datasets/datas.xlsx` columns: `text`, `department`
- `datasets/queries.xlsx` columns: `question`, `answer`, `department`

If files are missing, fallback sample data is used.

## Installation
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

> `spacy.blank("en")` is used by default, so app can run even without the download.

## Run
```bash
python app.py
```

Open:
- http://127.0.0.1:5000
- http://127.0.0.1:5000/admin
- http://127.0.0.1:5000/dashboard

## API Endpoints
- `POST /api/complaints` -> submit complaint
- `GET /api/complaints?department=...` -> list complaints
- `POST /api/complaints/<id>/resolve` -> resolve complaint
- `POST /api/query` -> ask question
- `GET /api/analytics` -> chart data
- `GET /health` -> health check
