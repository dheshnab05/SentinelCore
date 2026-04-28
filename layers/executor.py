import ollama


# Reusable remote Ollama client
client = ollama.Client(
    host="https://3374-162-216-141-56.ngrok-free.app"
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

    elif task == "simplify":

        prompt = f"""
Simplify this email into clear and meaningful points.

Rules:
- Understand the actual intent of the email.
- Ignore greetings (Hello, Dear Team, etc.).
- Ignore signatures (Regards, Best regards, etc.).
- Extract only important information.
- Convert into simple easy-to-read points.
- Keep it short.
- Do not rewrite the full email.
- Do not invent details.

Return format:

Simplified:
• point 1
• point 2
• point 3

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

    return "Unsupported task"