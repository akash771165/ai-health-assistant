import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError(
        "HF_TOKEN .env file mein nahi mila."
    )


client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN
)


MODEL = "openai/gpt-oss-120b"


def ask_llm(messages):

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.3,
        max_tokens=1000
    )

    return response.choices[0].message.content