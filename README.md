# FlyRank Task API

A simple RESTful CRUD API built using **FastAPI** for the FlyRank Backend Internship Week 2 Assignment.

---

## Features

- Create Tasks
- Read All Tasks
- Read Task by ID
- Update Tasks
- Delete Tasks
- Built-in Swagger UI
- Input Validation
- Proper HTTP Status Codes

---

## Tech Stack

- Python 3
- FastAPI
- Uvicorn

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/flyrank-task-api.git
```

Move inside the project

```bash
cd flyrank-task-api
```

Create Virtual Environment

```bash
python3 -m venv venv
```

Activate it

Mac/Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run Server

```bash
uvicorn app.main:app --reload
```

Server runs at

```
http://127.0.0.1:8000
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | API Information |
| GET | /health | Health Check |
| GET | /tasks | Get All Tasks |
| GET | /tasks/{id} | Get Task by ID |
| POST | /tasks | Create Task |
| PUT | /tasks/{id} | Update Task |
| DELETE | /tasks/{id} | Delete Task |

---

## Example curl

```bash
curl -i -X POST http://127.0.0.1:8000/tasks \
-H "Content-Type: application/json" \
-d '{"title":"Learn FastAPI"}'
```

---

## HTTP Status Codes

| Code | Meaning |
|------|----------|
| 200 | Success |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 404 | Not Found |

---

## Swagger UI

![Swagger UI](images/swagger-ui.png)

---

## Author

Lucky