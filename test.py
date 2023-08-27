from json import load
from os import environ
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = environ.get("OPENAI_API_KEY")
messages = [
    {
        "role": "system",
        "content": "You are a bot that writes essays in mla format that have no erros. Please output in markdown",
    }
]

while True:
    message = input("User : ")
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    reply = chat.choices[0].message.content
    with open(f"{message.replace(' ', '-')}.md", "w") as f:
        f.write(reply)
    messages.append({"role": "assistant", "content": reply})
