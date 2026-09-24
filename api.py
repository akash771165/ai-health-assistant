import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_hf_token():
    # Streamlit Cloud
    try:
        token = st.secrets.get("HF_TOKEN")
        if token:
            return token
    except Exception:
        pass

    # Local development
    token = os.getenv("HF_TOKEN")

    if not token:
        raise ValueError(
            "HF_TOKEN not found. "
            "Add it to .env locally or Streamlit Secrets."
        )

    return token


HF_TOKEN = get_hf_token()

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