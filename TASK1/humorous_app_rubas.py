import requests, os
from dotenv import load_dotenv
from openai import OpenAI
import sys, json
from flask import Flask, request, Response, render_template

app = Flask(__name__)

load_dotenv()

api_key = os.getenv('API_KEY')
hf_api_key = os.getenv('HF_API_KEY')


# ----------------- Serve your HTML UI -----------------
@app.route('/')
def home():
    return render_template('index.html')


# ----------------- Humor News API -----------------
@app.route('/humor-news') 
def fetch_news():
    country = request.args.get('country')
    category = request.args.get('category')
    
    sys.stdout.reconfigure(encoding='utf-8')

    params = {
        'apiKey': api_key
    }
    if country:
        params['country'] = country
    if category:
        params['category'] = category

    response = requests.get('https://newsapi.org/v2/top-headlines', params=params)
    data = response.json()
    
    results = []
    
    if response.status_code == 200:
        articles = data.get('articles', [])
       
        for article in articles:
            sentence = article.get('description', '')

            if sentence:
                humorous_text = transform_news_to_humorous(sentence)
            else:
                humorous_text = ""

            results.append({
                "title": article.get('title', ''),
                "author": article.get('author', 'Unknown'),
                "original_description": sentence or "",
                "humorous_description": humorous_text
            })
            
        # Save JSON locally
        with open('humorous-response.json', 'w', encoding='utf-8') as f:
            json.dump({"status": "success", "data": results}, f, ensure_ascii=False)
   
        return Response(
            json.dumps({"status": "success", "data": results}, ensure_ascii=False),
            mimetype="application/json"
        )
    else:
        return Response(
            json.dumps({"status": "error", "message": data.get("message", "Failed to fetch news")}, ensure_ascii=False),
            mimetype="application/json",
            status=500
        )
        
        
# ----------------- LLM Humor Transformation -----------------
def transform_news_to_humorous(sentence):
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=hf_api_key,
    )
    
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b:fireworks-ai",
        messages=[{
            "role": "user",
            "content": f"Rewrite this sentence humorously with relevant emojis in the end, "
                       f"exactly {len(sentence.split())} words total (without counting emojis as words). "
                       f"Output only the sentence, no explanation.\n\n{sentence}"
        }]
    )
    
    return completion.choices[0].message.content.strip()
            

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
