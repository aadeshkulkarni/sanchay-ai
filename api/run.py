import uvicorn
from main import app

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")