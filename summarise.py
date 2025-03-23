import openai
import time


def summarise(text: str, client: openai.OpenAI) -> str:
    """Summarise a news article text with GPT

    Args:
        text (str): text of a news article
        client ()

    Returns:
        dict: dictionary of article title, topics, text, url and post date
    """
    # sleep on it so no overlodas
    time.sleep(1)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"""Generate a 1 or 2 sentence summary (under
                60 words) of an Australian news article. Focus on key
                events, decisions or impacts. Avoid quotes. Text: {text}"""

            }],
            temperature=0.2,
            max_tokens=50
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Summary unavailable (API error) - {e}")
