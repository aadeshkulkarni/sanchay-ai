import os
import whisper
from whisper import utils

INPUT_PATH = os.environ.get("INPUT_FILE_PATH")
OUTPUT_PATH = os.environ.get("OUTPUT_DIR")
OUTPUT_TYPE = os.environ.get("OUTPUT_TYPE")

def generate_subtitles():
    '''generate subtitles and output to a path'''
    model = whisper.load_model("tiny")
    result = model.transcribe(INPUT_PATH)
    writer = utils.get_writer(OUTPUT_TYPE, OUTPUT_PATH)
    writer_args = {
        "highlight_words": False,
        "max_line_count": None,
        "max_line_width": None,
        "max_words_per_line": None,
    }
    writer(result, OUTPUT_PATH, **writer_args)
    print("⚡️ Success! ⚡️ Subtitles have been generated!")
    