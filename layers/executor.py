import ollama


# Reusable remote Ollama client
client = ollama.Client(
    host="https://fc10-162-216-141-56.ngrok-free.app"
)


def execute(task, content):

    # Normalize content
    content = content.strip()

    if task == "summarize":

        prompt = f"""
Summarize the following email into simple short bullet points.

STRICT RULES:
- Use ONLY the email content provided below.
- Do NOT invent anything.
- Do NOT assume anything.
- Do NOT mention anything not written in the email.
- Keep it simple and human-readable.

Output format:

• Sender:
• Main purpose:
• Action required:

EMAIL CONTENT:
{content}
"""

        response = client.chat(
            model="qwen2.5:3b",
            messages=[
                {
                    "role": "system",
                    "content": "You are an email summarizer. Only summarize the provided content."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    elif task == "reply":

        prompt = f"""
Generate a professional email reply for this email.

RULES:
- Reply only based on given email.
- Be concise.
- Be professional.
- Do not add unrelated content.

EMAIL CONTENT:
{content}
"""

        response = client.chat(
            model="qwen2.5:3b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional email reply assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    return "Unsupported task"