from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class TaskCreate(BaseModel):
    title : str

class TaskUdate(BaseModel):
    title : str
    done : bool    

tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Complete FlyRank Assignment",
        "done": False
    },
    {
        "id": 3,
        "title": "Practice DSA",
        "done": True
    }
]

@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": [
            "/tasks"
        ]
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.get("/tasks")
def get_tasks() :
    return tasks

@app.get("/tasks/{id}")
def get_task(id : int) :
    for task in tasks:
        if task["id"] == id:
            return task
        
    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )    

@app.post("/tasks", status_code=201)
def create_task(task : TaskCreate):
    if task.title.strip() == "" :
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )
    
    new_taks = {
        "id" : len(tasks) + 1,
        "title" : task.title,
        "done" : False
    }

    tasks.append(new_taks)
    return tasks


@app.put("/tasks/{id}")
def update_task(id : int, updated_task : TaskUdate):
    for task in tasks:
        if task["id"] == id:

            if updated_task.title.strip() == "":
                raise HTTPException(
                    status_code=400,
                    detail="Title cannot be empty"
                )

            task["title"] = updated_task.title
            task["done"] = updated_task.done

            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )


@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    for index, task in enumerate(tasks):
        if task["id"] == id:
            tasks.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )