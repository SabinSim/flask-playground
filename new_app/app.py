from flask import Flask, render_template
import requests

app = Flask(__name__)

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

@app.route("/")
def index():
    # 1) Get list of top story IDs
    ids = requests.get(TOP_STORIES_URL).json()

    # 2) Get only the top 10 stories
    news_list = []
    for item_id in ids[:10]:
        item = requests.get(ITEM_URL.format(item_id)).json()
        news_list.append({
            "title": item.get("title"),
            "url": item.get("url")
        })

    # 3) Pass to HTML
    return render_template("index.html", news=news_list)

if __name__ == "__main__":
    app.run(debug=True)
