import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def llm_signal(text):

    prompt = f"""
You are an AI detector.

Return ONLY a decimal number between 0.0 and 1.0.

0.0 means definitely human.
1.0 means definitely AI.

Text:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=10
    )

    try:
        score = float(response.choices[0].message.content.strip())
    except:
        score = 0.5

    return max(0.0, min(score, 1.0))


def style_signal(text):

    words = re.findall(r"\b\w+\b", text)
    sentences = re.split(r"[.!?]+", text)

    if len(words) == 0:
        return 0.5

    avg_sentence = len(words) / max(len(sentences), 1)

    unique_ratio = len(set(words)) / len(words)

    punctuation = len(re.findall(r"[,:;!?]", text)) / max(len(words), 1)

    score = (
        avg_sentence / 30 +
        unique_ratio +
        punctuation
    ) / 3

    return round(max(0.0, min(score, 1.0)), 2)