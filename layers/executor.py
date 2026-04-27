import ollama


# Reusable remote Ollama client
client = ollama.Client(
    host="https://fc10-162-216-141-56.ngrok-free.app"
)


def execute(task, content):

    if task == "summarize":

       prompt = f"""
You must summarize ONLY the email below.

CRITICAL RULES:
1. Use only facts written in the email.
2. Do not invent meetings, dates, or tasks.
3. Do not create examples.
4. Ignore greetings and signatures.
5. If information is missing, do not add it.

TASK:
Convert the email into 3 concise bullet points.

EMAIL CONTENT START
{content}
EMAIL CONTENT END

Return only bullet points.
"""

       response = client.chat(
       model="qwen2.5:3b",
       messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    options={
        "temperature": 0
    }
)

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