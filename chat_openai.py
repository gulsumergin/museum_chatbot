# chat_openai.py
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(artist_context, user_message):
    messages = [
        {"role": "system", "content": artist_context},
        {"role": "user", "content": user_message}
    ]

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7,
        max_tokens=200,
    )

    return response.choices[0].message.content
