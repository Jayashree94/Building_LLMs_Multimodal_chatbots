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

def shout(text):
    print(f"Shouting: {text.upper()}")
    return text.upper()

message_input = gr.Textbox(label="Your message", placeholder="Type something to shout...", lines=7)
message_output = gr.Textbox(label="Response", placeholder="Shouted message will appear here...", lines=7)


view = gr.Interface(
    shout,
    title="Shout App",
    description="Type a message and I'll shout it back at you!",
    inputs=message_input,
    outputs=message_output,
    examples=[["Hello, world!"], ["Gradio is great!"], ["I love building chatbots!"]],
    flagging_mode="never"
)

view.launch(inbrowser=True, share=True, auth=("jaya", "shree"))