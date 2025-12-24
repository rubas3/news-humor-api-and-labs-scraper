# API Scraping Assignment

This repository contains two Python-based data engineering tasks completed as part of the assignment.

---

## Project Structure

-**TASK1/**
- Flask-based REST API
- Fetches news from NewsAPI
- Transforms news descriptions into humorous text using an LLM
- Contains two versions:
    - `humorous_app_rubas.py` → With UI to display results on a web page
    - `humorous_app_without_ui.py` → Returns JSON responses only (no UI)

- **TASK2/**
  - Web scraper for lab test data
  - Scrapes test details from 10 labs listed on https://www.marham.pk/labs
  - Implements pagination
  - Exports the data to a CSV file

---

## Setup Instructions

1. Create and activate a virtual environment (Windows example):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

2. Install dependencies for a task:

```powershell
pip install -r TASK1/requirements.txt
pip install -r TASK2/requirements.txt
```

Running
- TASK1 (Flask API):

1. Create a `.env` file in `TASK1/` with:

```
API_KEY=your_newsapi_key
HF_API_KEY=your_huggingface_router_key
```

2. Run the app:

```powershell
python TASK1/humorous_app_rubas.py
```
After this a humorous-response.json file will be created as an output.

- TASK2 (scraper):

```powershell
python TASK2/marham_app_rubas.py
```
After this a labs_data.csv file will be created as an output.
