from anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    messages=[{"role": "user", "content": "Describe the color Blue to someone who's never been able to see in 1 sentence"}],
    max_tokens=100
)
print(response.content[0].text)