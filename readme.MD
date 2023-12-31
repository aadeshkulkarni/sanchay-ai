# Sanchay AI
- Sanchay is a Sanskrit word that means `collection` or `accumulation`. 
- We think that It is a fitting name for this project because it captures the `essence` of what it does - it takes a video and collects its key elements (`transcription, subtitles, and video chapters`) in an organized and easily accessible manner. 
- It's like creating a collection of information from a single source, making it more useful and convenient to work with. The name Sanchaya also has a nice ring to it.
- Sanchay-AI internally uses `Whisper` and `OpenAI` to achieve this feat.

## Project Setup

> Pre-requisite: Python

### Install openai-Whisper
    pip install -U openai-whisper

### Install ffmpeg
    brew install ffmpeg

### Install setuptools-rust
    pip install setuptools-rust

### Install tiktoken
    pip install --upgrade tiktoken

#### Note:
- Ensure that your video is stored in `videos directory`.
- Edit Env in `./run.sh`, most importantly, the `INPUT_FILE_PATH` property & the `OPENAI_API_KEY` property

### Run the script
    chmod +x run.sh
    ./run.sh


### Environment Variables

| Key | Description |
| --- | --- |
| INPUT_FILE_PATH | Video file path |
| OPENAI_API_KEY |  https://platform.openai.com/api-keys |
| OPENAI_MODEL | https://platform.openai.com/docs/models |
| MAX_TOKENS | This is used to split the subtitles into chunks of MAX_TOKENS. MAX_TOKENS should be 4/5th of your OPENAI_MODEL's max tokens |
| OUTPUT_TYPE | options [txt, json, vtt, srt, tsv, all], logic supports vtt files only for now |
| OUTPUT_DIR | Directory where output will be stored |