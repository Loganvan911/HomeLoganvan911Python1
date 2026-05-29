import openai

openai.api_key = "YOUR_API_KEY"

while True:
    text = input("Ти: ")

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": text}
        ]
    )

    print("Бот:", response.choices[0].message.content)