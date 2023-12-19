'''server using fast api to get chapters from given video URL'''
import os
import warnings
import json
import whisper
import tiktoken
from fastapi import FastAPI
from whisper import utils
from openai import OpenAI

OPENAI_MODEL = "gpt-3.5-turbo-1106"
MAX_TOKENS = 15000

OUTPUT_PATH = "./output"
OUTPUT_FILE = "output.vtt"
OUTPUT_TYPE = "vtt"

client = OpenAI(api_key="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")
app = FastAPI()

async def generate_subtitles(video_url: str):
    model = whisper.load_model("tiny")
    result = model.transcribe(video_url)  # Ensure this is awaitable
    writer = utils.get_writer(OUTPUT_TYPE, OUTPUT_PATH)
    writer_args = {
        "highlight_words": False,
        "max_line_count": None,
        "max_line_width": None,
        "max_words_per_line": None,
    }
    output_file_path = os.path.join(OUTPUT_PATH, OUTPUT_FILE)
    writer(result, OUTPUT_PATH, **writer_args)
    print('output file path', output_file_path)
    return output_file_path

async def split_vtt_file(file_path: str, tokens: int):
    chunks = []
    with open(file_path, "r", encoding="utf-8") as file:
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

            if len(current_chunk) + number_of_tokens <= int(tokens):
                current_chunk += segment + "\n\n"
            else:
                chunks.append(current_chunk.strip())
                current_chunk = segment + "\n\n"

        if current_chunk:
            chunks.append(current_chunk.strip())
    return chunks

async def generate_chapters(chunk: str):
    '''generate chapters from given chunk'''
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

@app.get("/chapters")
async def get_chapters(video_url: str):
    if not video_url:
        return {"error": "Please provide a valid video URL"}
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            subtitles_path = await generate_subtitles(video_url)

        chunks = await split_vtt_file(subtitles_path, MAX_TOKENS)
        chapters = []
        for chunk in chunks:
            chaps = await generate_chapters(chunk)
            chapters.extend(json.loads(chaps))

        output_chapters_path = os.path.join(OUTPUT_PATH, "chapters.json")
        with open(output_chapters_path, "w", encoding="utf-8") as json_file:
            json.dump(chapters, json_file)

        return {"chapters": chapters, "chapters_file": output_chapters_path}
    except Exception as e:
        return {"error": f"Error generating chapters: {e}"}

# [Rest of your code remains the same]
