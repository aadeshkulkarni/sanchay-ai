export INPUT_FILE_PATH="./videos/How I Failed My Netflix Interview.mp4"
export OPENAI_API_KEY="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"
export OPENAI_MODEL="gpt-3.5-turbo-1106" 
export MAX_TOKENS=15000
export OUTPUT_TYPE="vtt" # options [txt, json, vtt, srt, tsv, all], logic supports vtt files only for now
export OUTPUT_DIR="./output" # Directory where output will be stored


# Step 1 | Generating subtitles
python3 subtitles.py

# Step 2 | Generating chapters
python3 chapters.py