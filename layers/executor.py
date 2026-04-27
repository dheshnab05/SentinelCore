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
Write a direct email reply to the given email.

Rules:
- Reply ONLY to the email content.
- Understand the sender's message first.
- Keep the reply short and relevant.
- Do NOT create a new subject line.
- Do NOT invent context.
- Do NOT use placeholders like [Sender Name].
- Match the tone of the original email.
- If the email is appreciation, respond with thanks.
- If the email asks for something, respond accordingly.

Return only the reply body.

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