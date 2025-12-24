import os, json, requests
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, request, Response, render_template

app = Flask(__name__)
load_dotenv()

NEWS_API_KEY = os.getenv("API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/humor-news")
def humor_news():
    country = request.args.get("country")
    category = request.args.get("category")

    params = {"apiKey": NEWS_API_KEY}
    if country:
        params["country"] = country
    if category:
        params["category"] = category

    try:
        news_response = requests.get(
            "https://newsapi.org/v2/top-headlines",
            params=params,
            timeout=10
        )
        news_response.raise_for_status()
    except Exception as e:
        return Response(
            json.dumps({"status": "error", "message": str(e)}),
            mimetype="application/json",
            status=500
        )

    articles = news_response.json().get("articles", [])[:5]  # LIMIT 5
    results = []

    for article in articles:
        description = article.get("description") or ""
        author = article.get("author") or "Unknown"

        try:
            humorous = (
                transform_to_humor(description)
                if description else "No description available 🤷‍♂️"
            )
        except Exception:
            humorous = "⚠️ Humor service unavailable"

        results.append({
            "title": article.get("title"),
            "author": author,
            "original_description": description,
            "humorous_description": humorous
        })

    # ------------------- JSON FILE SAVE -------------------
    with open("humorous-response.json", "w", encoding="utf-8") as f:
        json.dump({"status": "success", "data": results}, f, ensure_ascii=False, indent=2)
    # -------------------------------------------------------

    return Response(
        json.dumps({"status": "success", "data": results}, ensure_ascii=False),
        mimetype="application/json"
    )


def transform_to_humor(text):
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=HF_API_KEY
    )

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b:fireworks-ai",
        messages=[{
            "role": "user",
            "content": (
                f"Rewrite this sentence humorously with emojis at the end. "
                f"Keep exactly {len(text.split())} words (emojis not counted). "
                f"Output only the sentence.\n\n{text}"
            )
        }],
        timeout=15
    )

    return completion.choices[0].message.content.strip()


if __name__ == "__main__":
    app.run(debug=True)
