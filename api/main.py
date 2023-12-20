from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi import BackgroundTasks
import subprocess
import os
import json

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/chapters")
async def generate_chapters(video_url: str, background_tasks: BackgroundTasks):
    # Step 1: Run subtitles.py asynchronously
    background_tasks.add_task(run_subtitles, video_url)

    # Step 2: Return response
    response_content = {
        "message": "Generating chapters. Check back later for the result."
    }
    return JSONResponse(content=response_content, status_code=200)


def run_subtitles(video_url: str):
    # Step 1: Download video using youtube-dl or any other suitable tool
    # Example: subprocess.run(["youtube-dl", video_url, "-o", "videos/video.mp4"])

    # Step 2: Set environment variables
    os.environ["INPUT_FILE_PATH"] = "./videos/video.mp4"
    os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"
    os.environ["OPENAI_MODEL"] = "gpt-3.5-turbo-1106"
    os.environ["MAX_TOKENS"] = "15000"
    os.environ["OUTPUT_TYPE"] = "vtt"
    os.environ["OUTPUT_DIR"] = "./output"

    # Step 3: Run subtitles.py
    subprocess.run(["python3", "subtitles.py"])

    # Step 4: Run chapters.py
    subprocess.run(["bash", "run_chapters.sh"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
