from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = ""

@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "city parameter is required"}), 400

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
