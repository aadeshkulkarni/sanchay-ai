from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/_readyz")
@app.get("/_healthz")
def read_root():
    return {"status": "ok"}


class Needs(BaseModel):
    transcoding: bool
    subtitles: bool
    thumbnails: bool


class Project(BaseModel):
    project: str
    videoURL: str
    needs: Needs


@app.get("/projects")
async def read_projects(db:db_dependency):
    result = db.query(models.Projects).all()
    return result

@app.post("/generate-all")
async def create_project(project:Project, db: db_dependency):
    # Step 1: Insert project into db
    db_project = models.Projects(project=project.project, videoURL=project.videoURL, needTranscoding=project.needs.transcoding, needSubtitles=project.needs.subtitles, needThumbnails=project.needs.thumbnails)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    # Step 2: Generate transcoding

    # Step 3: Upload to bucket

    # Step 4: Update table with bucket
    return project