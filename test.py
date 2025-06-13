from ollama import chat
import ollama

response = chat(
    messages=[{
        'role': 'user',
        'content': 'Hello!'
    }],
    model='devstral:24b',
)

print(response.message.content)