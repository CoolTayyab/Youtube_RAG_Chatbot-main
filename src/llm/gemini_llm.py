from openai import OpenAI
import os
from dotenv import load_dotenv
from config import GEMINI_API_KEY

load_dotenv()

class GeminiModel:
    def __init__(self):
        api_key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError(
                "Missing Gemini API key. Set GEMINI_API_KEY or GOOGLE_API_KEY in .env."
            )

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        self.model_name = "gemini-2.5-flash"

    def generate(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Always answer in English, even when the question or context is in another language.",
                },
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content