# Bulk Certificate Generator

A backend API that accepts a bulk certificate generation request, processes
certificates asynchronously, tracks job progress, and allows generated
certificates to be retrieved individually.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- ReportLab
- Pytest

## Features

- Bulk certificate generation
- Request validation
- Background processing
- Job status and progress tracking
- Individual certificate failure handling
- PDF certificate generation
- Certificate retrieval API
- Automated tests

## Project Setup

### 1. Clone the repository

```bash
git clone https://github.com/ayuzhjha/bulk-certificate-generator
cd bulk-certificate-generator
```

### 2. Create a virtual environment

```bash 
python -m venv venv

venv\Scripts\activate //activate it
```

### 3. Install dependencies

```bash 
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash 
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/certificate_generator
```

Make sure the PostgreSQL database certificate_generator exists.

### 5. create database tabels

```bash
python create_tables.py
```

## Start Dev server 

```bash
uvicorn main:app --reload
```

The API will be available at:
http://127.0.0.1:8000

Interactive API documentation:
http://127.0.0.1:8000/docs

### Made by AJ ;)