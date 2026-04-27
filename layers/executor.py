import ollama


# Reusable remote Ollama client
client = ollama.Client(
    host="https://1d05-162-216-141-56.ngrok-free.app"
)


def execute(task, content):

    if task == "summarize":

        prompt = f"""
Summarize this email into 3 short bullet points.

Include:
- sender (if identifiable)
- main purpose of the email
- important action or next step

Email:
{content}
"""

        response = client.chat(
            model="qwen2.5:3b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    elif task == "reply":

      prompt = f"""
Write a natural reply to this email.

Rules:
- Understand what the sender is asking.
- Reply as the receiver of the email.
- If sender asks for review/feedback, acknowledge and confirm action.
- If sender shares an update, acknowledge it naturally.
- If sender appreciates, thank them.
- Keep reply short (2-4 lines).
- No subject line.
- No placeholders.
- No extra formal template.
- Return only the reply text.

Email:
{content}
"""

    response = client.chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]