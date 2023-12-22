import os
import json
import re
import tiktoken
import openai
from openai import OpenAI


client = OpenAI()


OPENAI_MODEL = os.environ.get("OPENAI_MODEL")
MAX_TOKENS = os.environ.get("MAX_TOKENS")


def split_vtt_file(file_path, MAX_TOKENS):
    chunks = []
    with open(file_path, "r") as file:
        vtt_content = file.read().strip()
        vtt_segments = vtt_content.split("\n\n")

        current_chunk = ""
        for segment in vtt_segments:
            lines = segment.strip().split("\n")
            # Merge all lines starting from the 3rd line
            segment_text = " ".join(lines[2:])

            # Tiktokens to count total token length for the current chunk
            encoding = tiktoken.encoding_for_model(OPENAI_MODEL)
            number_of_tokens = len(encoding.encode(segment_text))
            # print(number_of_tokens)

            if len(current_chunk) + number_of_tokens <= int(MAX_TOKENS):
                current_chunk += segment + "\n\n"
            else:
                chunks.append(current_chunk.strip())
                current_chunk = segment + "\n\n"

        if current_chunk:
            chunks.append(current_chunk.strip())

    return chunks


def generate_chapters(chunk):
    print("Current Chunk length:", len(chunk))
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """You are a helpful assistant that receives video\'s subtitles in vtt as input and responds back with chapters for the video in the format:
                        [
                        { "title": "Introduction", "start": "0:00", "end": "01:34" },
                        { "title": "Chapter description", "start": "01:35", "end": "02:50" }
                        { "title": "Chapter description", "start": "02:50", "end": "03:51" }
                        { "title": "Chapter description", "start": "03:52", "end": "07:45" }
                        ..
                        { "title": "Outro", "start": "07:46", "end": "10:45" }
                        ]
                        Your response should be a valid json without the codeblock formatting.
                        """,
            },
            {
                "role": "user",
                "content": json.dumps(chunk),
            },
        ],
        model=OPENAI_MODEL,
    )
    res = chat_completion.choices[0].message.content
    return res


# Usage
print("\n")
print("Step 2: Generating chapters from the subtitles now")

chunks = split_vtt_file("./output/output.vtt", MAX_TOKENS)
chapters = []
print("Total chunks: ", len(chunks))
for index, chunk in enumerate(chunks):
    print("Processing " + str(index + 1) + "/" + str(len(chunks)))
    chaps = generate_chapters(chunk)
    print(chaps)
    chapters += json.loads(chaps)
    print("\n")

with open("./output/chapters.json", "w") as json_file:
    json.dump(chapters, json_file)

print("⚡️ Success! ⚡️  Chapters generated at ", "./output/chapters.json")
