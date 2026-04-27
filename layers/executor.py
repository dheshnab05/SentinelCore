import ollama


# Reusable remote Ollama client
client = ollama.Client(
    host="https://fc10-162-216-141-56.ngrok-free.app"
)


def execute(task, content):

    if task == "summarize":

        prompt = f"""
Summarize the following email.

STRICT RULES:
- Use ONLY the email content.
- Do NOT invent facts.
- Do NOT assume anything.
- Ignore greetings (like Dear Team, Hello).
- Ignore signatures (like Regards, Best regards).
- Focus only on actual message content.

Return exactly in this format:

Summary:
- point 1
- point 2
- point 3
- point 4 (if needed)

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
Write a professional reply for this email.

Rules:
- Be polite
- Be short
- Stay relevant to the email

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