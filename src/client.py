from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="")

completion = client.chat.completions.create(
    model="Mistral-7B-Instruct-v0.3",
    messages=[
        {"role": "user", "content": "Tell me a fun fact about AI."},
    ],
)

print(completion.choices[0].message.content)
