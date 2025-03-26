import os
import groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Error: GROQ_API_KEY is not set. Check your .env file.")

client = groq.Client(api_key=GROQ_API_KEY)

def get_suggestions(issue, code_snippet):
    """
    Uses LLaMA 3.2 90B via Groq API to analyze and suggest fixes.
    """
    prompt = f"""
    Code Issue: {issue}
    Code:
    ```python
    {code_snippet}
    ```
    Suggest a fix and explain it step-by-step.
    """

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are an expert Python debugger."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
