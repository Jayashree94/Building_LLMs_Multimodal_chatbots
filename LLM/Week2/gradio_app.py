import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
import gradio as gr

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
openai = OpenAI()

requests.get("http://localhost:11434").content
OLLAMA_BASE_URL = "http://localhost:11434/v1"

ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key='ollama')
# Get a fun fact

# response = ollama.chat.completions.create(model="llama3.2:latest", messages=[{"role": "user", "content": "Tell me a fun fact"}])

# response.choices[0].message.content
# print(response.choices[0].message.content)


def shout(text):
    print(f"Shouting: {text.upper()}")
    return text.upper()

shout("hello world")

gr.Interface(fn=shout, inputs="text", outputs="textbox", flagging_mode="never").launch(inbrowser=True, share=True, auth=("jaya", "shree"))

#share=true to get a public link to share the app, but be careful with this if your app allows users to input sensitive data!
#inbrowser=True to open the app in a new tab in your default browser instead of an iframe in the notebook (which can sometimes have issues with authentication popups, etc.)
