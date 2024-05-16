import os
import json
import whisper
import urllib.request
from bson.objectid import ObjectId
from writer import get_writer
from gpt import generate_chapters_gemini

def perform_magic(video_url):
    model = whisper.load_model("tiny")
    result = model.transcribe("./videos/" + video_url)
    writer = get_writer()
    writer_args = {
        "highlight_words": False,
        "max_line_count": None,
        "max_line_width": None,
        "max_words_per_line": None,
    }
    captions = writer(result, writer_args) 
    result["captions"] = captions
    print(len(captions))
    chapters = generate_chapters_gemini(captions)
    print(chapters)
    result["chapters"] = chapters
    return result


def download_video(video_url, output_path):
    if not os.path.exists(os.path.dirname("./videos/" + output_path)):
        os.makedirs(os.path.dirname("./videos/" + output_path))
    urllib.request.urlretrieve(video_url, "./videos/" + output_path)


def update_data(collection, video_id, output):
    condition = {"_id": ObjectId(video_id)}
    newvalues = {
        "$set": {"transcription": output["text"], "captions": output["captions"], "chapters": output["chapters"]}
    }
    result = collection.update_one(condition, newvalues)
    print(result)


def log_error_to_db(collection, video_id, error):
    condition = {"_id": ObjectId(video_id)}
    newvalues = {"$set": {"failed": True, "error": error}}
    result = collection.update_one(condition, newvalues)
    print(result)
