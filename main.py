from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import datetime

app = FastAPI(title="DevVault API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Snippet(BaseModel):
    id: Optional[int] = None
    title: str
    language: str
    code: str
    tags: List[str]
    created_at: Optional[str] = None

snippets_db = []
counter = 1

@app.get("/")
def read_root():
    return {"message": "Welcome to DevVault - Daily Code & Snippet Manager API"}

@app.get("/snippets", response_model=List[Snippet])
def get_snippets():
    return snippets_db

@app.post("/snippets", response_model=Snippet)
def create_snippet(snippet: Snippet):
    global counter
    snippet.id = counter
    snippet.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    snippets_db.append(snippet)
    counter += 1
    return snippet

@app.delete("/snippets/{snippet_id}")
def delete_snippet(snippet_id: int):
    for index, item in enumerate(snippets_db):
        if item.id == snippet_id:
            snippets_db.pop(index)
            return {"message": "Snippet deleted successfully"}
    raise HTTPException(status_code=404, detail="Snippet not found")
