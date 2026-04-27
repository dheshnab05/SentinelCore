import ollama


# Reusable remote Ollama client
client = ollama.Client(
    host="https://fc10-162-216-141-56.ngrok-free.app"
)


def execute(task, content):

    if task == "summarize":

        prompt = f"""
You are an email summarizer.

STRICT RULES:
1. Use ONLY the email content provided.
2. Do NOT invent information.
3. Do NOT hallucinate.
4. If sender is visible, extract it.
5. Summarize in exactly 3 bullet points.

Format:

- Sender: ...
- Main points : ...

EMAIL CONTENT:
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
Write a professional reply for this email.

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