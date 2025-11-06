# Notes App - Frontend + Backend

Simple React + FastAPI app with JWT auth and CRUD notes.

## Features
- Signup/Login (JWT)
- Protected Notes Dashboard
- Create, Read, Update, Delete notes
- Search / Filter notes
- Responsive UI

## Run Backend
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

## Features
cd frontend
npm install
npm start
