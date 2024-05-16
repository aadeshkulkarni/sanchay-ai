import os
import pathlib
import textwrap
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


client = OpenAI()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def generate_chapters_openai(subtitles):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""For the below video subtitles, generate video chapters of the form: [start_time] - [chapter_title]. 
                For example: 
                01:27 - Start of the class.
                03:00 - Why do you need React?
                07:03 - What is React?
                and so on.
                start_time format should be hh:mm:ss :\n {subtitles}""",
            }
        ],
        model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message


def generate_chapters_gemini(subtitles):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(
        f"""You are a helpful assistant that receives video\'s subtitles in vtt as input and responds back with chapters for the video in the format:
                        [
                        {{ "title": "Introduction", "start": "0:00"}},
                        {{ "title": "Chapter description", "start": "01:35" }}
                        {{ "title": "Chapter description", "start": "02:50"}}
                        {{ "title": "Chapter description", "start": "03:52" }}
                        ..
                        {{ "title": "Outro", "start": "07:46" }}
                        ]
                        Your response should be a valid json without the codeblock formatting.
                        {subtitles} """
    )
    response.resolve()
    return response.text


# def test():
#     model = genai.GenerativeModel("gemini-pro")
#     response = model.generate_content("What is the meaning of life?")
#     # print(response)
#     response.resolve()
#     print(response.text)
#    # print(to_markdown(response.text))

# test()