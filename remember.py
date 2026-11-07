from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

history = [
    {"role": "user", "content": "Hi! My name is Priya and my favorite color is teal."},
    {"role": "assistant", "content": "Nice to meet you, Priya! Teal is a great color."},
    {"role": "user", "content": "What is my name and my favorite color?"}
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=history
)

print(response.choices[0].message.content)
