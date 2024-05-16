### RabbitMQ Consumer

- Listen to RabbitMQ Topic 'task_queue' and execute a callback whenever event is triggered
- The callback should do the following:
    - callback expects 2 inputs - videoId and videoUrl
    - Download the video on worker thread
    - Generate Transcription & Captions
    - Update the database with generated content using videoId as base condition


Todos:
- Separate out logic for GPT and Whisper into 2 different consumers.
- Add logic for Video title, description, youtube tags


## Project Setup

    Pre-requisite: Python

### 1. Install ffmpeg
    brew install ffmpeg

### 2. Python setup

We recommend using `venv` for Virtual environment. You can read this article to learn more: https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/

    Steps:
    - `pip install virtualenv` to install venv
    - `cd apps/worker` to change directory to worker app
    - `python3 -m venv sanchay-env` to create a new virtual environment 'sanchay-env'
    - `source sanchay-env/bin/activate` to activate the newly created virtual environment
    - `pip install -r requirements.txt` to install all python packages

### 3. Setup Env Variables
    - copy .env.example and rename it to .env
    - OPENAI_API_KEY= (required, get the API key from https://platform.openai.com/api-keys)
    - GOOGLE_API_KEY= (optional, get the API key from https://ai.google.dev/gemini-api/docs/api-key)
    - MONGO_DB= (required, get the key from https://cloud.mongodb.com/)
