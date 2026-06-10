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

def message_to_ollama(message):
    response = ollama.chat.completions.create(model="llama3.2:latest", messages=[{"role": "user", "content": message}])
    return response.choices[0].message.content

message_input = gr.Textbox(label="Your message", placeholder="Type something to ollama...", lines=7)
message_output = gr.Textbox(label="Response", placeholder="ollama response message will appear here...", lines=7)


view = gr.Interface(
    message_to_ollama,
    title="Ollama chat App",
    description="Type a message and I'll respond with ollama!",
    inputs=message_input,
    outputs=message_output,
    examples=[["Hello, world!"], ["Gradio is great!"], ["I love building chatbots!"]],
    flagging_mode="never"
)

view.launch(inbrowser=True, share=True, auth=("jaya", "shree"))