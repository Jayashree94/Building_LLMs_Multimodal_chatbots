# Create OpenAI client

from openai import OpenAI
openai = OpenAI()

response = openai.chat.completions.create(model="gpt-5-nano", messages=[{"role": "user", "content": "Tell me a fun fact"}])

response.choices[0].message.content

