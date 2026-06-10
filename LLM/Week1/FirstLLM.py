from ollama import chat

response = chat(
    model='gemma3:270m',
    messages=[
        {'role': 'user', 'content': 'What is PostgreSQL?'}
    ]
)

print(response['message']['content'])