import ollama


def execute(task, content):

    if task == "summarize":

        prompt = f"""
Summarize this email into 3 short bullet points.

Email:
{content}
"""

        response = ollama.chat(
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
Write a professional reply:

{content}
"""

        response = ollama.chat(
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