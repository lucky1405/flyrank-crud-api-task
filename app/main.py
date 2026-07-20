from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.database import initialize_database, get_all_tasks, get_task_by_id, create_task_db

app = FastAPI(
    title="FlyRank Task API",
    description="A simple CRUD API built with FastAPI for the FlyRank Backend Internship Assignment.",
    version="1.0.0"
)

initialize_database()


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

@app.get(
    "/",
    summary="Get API Information",
    description="Returns basic information about the Task API."
)
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": [
            "/tasks"
        ]
    }


@app.get(
    "/health",
    summary="Health Check",
    description="Checks whether the server is running."
)
def health():
    return {
        "status": "ok"
    }

@app.get(
    "/tasks",
    summary="Get All Tasks",
    description="Returns all available tasks."
)
def get_tasks() :
    # return tasks
    return get_all_tasks()

@app.get(
    "/tasks/{id}",
    summary="Get Task by ID",
    description="Returns a single task using its ID."
)
def get_task(id : int) :
    # for task in tasks:
    #     if task["id"] == id:
    #         return task
        
    # raise HTTPException(
    #     status_code=404,
    #     detail=f"Task {id} not found"
    # )    
    task = get_task_by_id(id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {id} not found"
        )
    return task

@app.post(
    "/tasks",
    status_code=201,
    summary="Create Task",
    description="Creates a new task."
)
def create_task(task : TaskCreate):
    if task.title.strip() == "" :
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )
    
    # new_taks = {
    #     "id" : len(tasks) + 1,
    #     "title" : task.title,
    #     "done" : False
    # }

    # tasks.append(new_taks)
    # return tasks
    return create_task_db(task.title)


@app.put(
    "/tasks/{id}",
    summary="Update Task",
    description="Updates an existing task."
)
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


@app.delete(
    "/tasks/{id}",
    status_code=204,
    summary="Delete Task",
    description="Deletes a task by ID."
)
def delete_task(id: int):
    for index, task in enumerate(tasks):
        if task["id"] == id:
            tasks.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )