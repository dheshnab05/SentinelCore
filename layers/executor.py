import ollama


# Create reusable client
client = ollama.Client(
    host="https://e697-162-216-141-56.ngrok-free.app "
)


def execute(task, content):

    if task == "summarize":

        prompt = f"""
Summarize this email into 3 short bullet points.

Include:
- who sent it (if identifiable)
- what the email is mainly about
- important action or next step

Email:
{content}
"""

        response = client.chat(
            model="phi3:mini",
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
            model="phi3:mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    return "Unsupported task"