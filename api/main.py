from fastapi import FastAPI, Depends, UploadFile, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import sys
from scripts.subtitles import generate_subtitles
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

app = FastAPI()


@app.get("/_readyz")
@app.get("/_healthz")
def read_root():
    return {"status": "ok"}


@app.post("/subtitles")
def create_subtitles(video_name: str, file: UploadFile):
    if not os.path.exists("videos"):
        os.makedirs("videos")

    file_path = f"videos/{video_name}.mp4"
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    if not file.content_type.startswith("video/"):
        return {"error": "Invalid file type. Only video files are allowed."}

    if not os.path.exists("output"):
        os.makedirs("output")
    output_path = generate_subtitles(file_path,"vtt","./output",video_name)
    response = FileResponse(output_path, media_type="text/vtt", filename=f"{video_name}.vtt")
    response.headers["Content-Disposition"] = f"attachment; filename={video_name}.vtt"
    return response