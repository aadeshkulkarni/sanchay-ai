## Setup

### Install openai-Whisper
    pip install -U openai-whisper

### Install ffmpeg
    brew install ffmpeg

### Install setuptools-rust
    pip install setuptools-rust

### Install tiktoken
    pip install --upgrade tiktoken

#### Note:
- Ensure that your video is stored in videos directory.
- Edit Env in ./run.sh, most importantly, the INPUT_FILE_PATH property & the OPENAI_API_KEY property

### Run the script
    chmod +x run.sh
    ./run.sh



#### Env

- INPUT_FILE_PATH - Video file path
- OPENAI_API_KEY -  https://platform.openai.com/api-keys
- OPENAI_MODEL - https://platform.openai.com/docs/models (Can use only chat based models for the script to work)
- MAX_TOKENS - This is used to split the subtitles into chunks of MAX_TOKENS. MAX_TOKENS should be 4/5th of your OPENAI_MODEL's max tokens.
- OUTPUT_TYPE - options [txt, json, vtt, srt, tsv, all], logic supports vtt files only for now
- OUTPUT_DIR - Directory where output will be stored
