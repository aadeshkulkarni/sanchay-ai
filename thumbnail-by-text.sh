#!/bin/bash

#command line tool curl needed

#MY PROCESS :
# I used the GPT 3.5 and Dalle for this process.
#gpt 3.5 will process the description of the title and dalle wil process image by that

GPT_API_KEY="YOUR_GPT_API_KEY"

DALI_API_KEY="YOUR_DALI_API_KEY"

VIDEO_TITLE="Your Video Title"

BASE_IMAGE_PATH="path/to/base/image.jpg"

OUTPUT_DIR="output_directory"

DESCRIPTION=$(curl -s -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $GPT_API_KEY" -d '{"prompt": "'"$VIDEO_TITLE"'" }' https://api.openai.com/v1/engines/davinci-codex/completions | jq -r '.choices[0].text' | tr -d '\n')

if [ -z "$BASE_IMAGE_PATH" ]; then
  curl -s -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $DALI_API_KEY" -d '{"text": "'"$DESCRIPTION"'", "num_images": 1}' https://api.openai.com/v1/dall-e/generate | jq -r '.images[0].url' | xargs curl -s -o "$OUTPUT_DIR/thumbnail.jpg"
else
  curl -s -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $DALI_API_KEY" -d '{"text": "'"$DESCRIPTION"'", "base_image_path": "'"$BASE_IMAGE_PATH"'"}' https://api.openai.com/v1/dall-e/generate | jq -r '.url' | xargs curl -s -o "$OUTPUT_DIR/thumbnail.jpg"
fi

echo "Thumbnail generated and saved to $OUTPUT_DIR/thumbnail.jpg"
