from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "" 

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None

    if request.method == "POST":
        city = request.form.get("city")

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") == 200:
            weather = {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
            }
        else:
            weather = {"error": data.get("message", "Unknown error")}

    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(debug=True)
