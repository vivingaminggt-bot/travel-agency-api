import os
from groq import Groq

MODEL = "llama-3.3-70b-versatile"


def get_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))


def chat_reply(history, new_message):
    client = get_client()
    messages = [
        {"role": "system", "content": "You are a friendly travel agency assistant. Help customers with trip questions, recommendations, and booking advice. Keep replies short and helpful."}
    ] + history + [{"role": "user", "content": new_message}]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=500,
    )
    return response.choices[0].message.content


def generate_recommendation(preferences, available_trips):
    client = get_client()
    trips_text = "\n".join([
        f"- {t['title']} in {t['city']}, {t['country']} | ${t['price_per_person']}/person | {t['available_seats']} seats left"
        for t in available_trips
    ])

    prompt = f"""A customer is looking for a trip with these preferences: {preferences}

Here are the available trips:
{trips_text}

Recommend the top 2 trips that best match their preferences and explain why in 2-3 sentences."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
    )
    return response.choices[0].message.content