from fastapi import FastAPI ,HTTPException
import uvicorn
from typing import Any
from pydantic import BaseModel
import json


app = FastAPI()
filename = "ideas.json"

try:
    with open(filename, "r") as file:
        ideas = json.load(file)
except FileNotFoundError:
    ideas = {}

class Idea(BaseModel):
    name: str
    industry: str
    budget: float


@app.get('/')
def home():
    return {"Home" : "Welcome the idea house"}

@app.get("/ideas")
def get_ideas():
    return ideas


@app.post("/ideas")
def post_ideas(body:Idea):
    if ideas:
        new_id = str(int(max(ideas.keys(), key=int)) + 1)
    else:
        new_id = "1"
    
    ideas[new_id] = {
        "id": new_id,
        **body.model_dump()
    }
    with open(filename, "w") as file:
        json.dump(ideas, file, indent=4)

    return ideas[new_id]


@app.delete("/ideas/{id}")
def delete_idea(id: str):

    if id not in ideas:
        raise HTTPException(status_code=404, detail="Idea not found")

    removed = ideas.pop(id)

    with open(filename, "w") as file:
        json.dump(ideas, file, indent=4)

    return {"detail": f"Idea with id {id} has been deleted", "removed": removed}


@app.put("/ideas/{id}")
def update_idea(id: str, body: Idea):
    if id not in ideas:
        raise HTTPException(status_code=404, detail="Idea not found")

    ideas[id] = {
        "id": id,          
        **body.model_dump()
    }
    with open(filename, "w") as file:
        json.dump(ideas, file, indent=4)
    return ideas[id]
















def main():
    print("Hello from startup-api!")











if __name__ == "__main__":
    main()
