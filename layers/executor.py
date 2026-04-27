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
Summarize this email clearly and briefly.

Rules:
- Give the core message only
- Use simple language
- Maximum 5 bullet points
- Ignore greetings and signatures
- Ignore repeated lines
- Focus only on important content

Return format:

• Main purpose
• Important updates
• Required action (if any)
• Deadlines (if any)

Email:
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