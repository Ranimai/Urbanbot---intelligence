import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_response(prompt):
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",                           # model="llama-3.1-70b-versatile" also work
        messages=[
            {"role": "system", "content": "You are a Smart City AI assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return completion.choices[0].message.content


