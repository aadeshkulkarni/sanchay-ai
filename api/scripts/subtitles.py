import whisper
from whisper import utils


def generate_subtitles(input_file_path, output_type, output_file_path, output_file_name):
    model = whisper.load_model("tiny")
    result = model.transcribe(input_file_path)
    writer = utils.get_writer(output_type, output_file_path)
    writer_args = {
        "highlight_words": False,
        "max_line_count": None,
        "max_line_width": None,
        "max_words_per_line": None,
    }
    writer(result, output_file_name, **writer_args)
    output_path = f"{output_file_path}/{output_file_name}.{output_type}"
    print("⚡️ Success! ⚡️ Subtitles have been generated @ "+output_path)
    return output_path
