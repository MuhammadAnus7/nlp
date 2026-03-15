# AI Complaint Management System

Modern Flask-based complaint management platform with AI routing, priority detection, semantic query answering, escalation workflows, and analytics dashboards.

## Tech Stack
- **Backend:** Flask, SQLite
- **ML/NLP:** scikit-learn, Sentence Transformers, TextBlob, VADER, spaCy
- **Frontend:** HTML, Tailwind CSS, JavaScript, Chart.js

## Project Structure
```
app.py
requirements.txt

datasets/
  datas.xlsx
  queries.xlsx

ml_models/
  train_model.py
  complaint_classifier.py
  sentiment_analyzer.py
  query_engine.py

database/
  database.py
  models.py
  db.py

templates/
  index.html
  admin.html
  dashboard.html

static/js/
  app.js
  admin.js
  dashboard.js
```

## Run Instructions
```bash
pip install -r requirements.txt
python app.py
```

Open:
- `http://127.0.0.1:5000`
- `http://127.0.0.1:5000/admin`
- `http://127.0.0.1:5000/dashboard`

## Notes
- On startup, if `ml_models/model.pkl` is missing, the app automatically runs training from `datasets/datas.xlsx`.
- Query answering uses semantic similarity over `datasets/queries.xlsx` and returns fallback text when confidence is below threshold.
