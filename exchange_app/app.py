from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://api.frankfurter.app/latest"   # Frankfurter API endpoint

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        # Get form data
        amount = float(request.form.get("amount"))
        from_currency = request.form.get("from")
        to_currency = request.form.get("to")

        # Prevent conversion between identical currencies
        if from_currency == to_currency:
            result = {
                "from": from_currency,
                "to": to_currency,
                "amount": amount,
                "converted": amount,
                "rate": 1.0
            }
            return render_template("index.html", result=result)

        # Request to Frankfurter API
        url = f"{API_URL}?from={from_currency}&to={to_currency}"

        response = requests.get(url)
        data = response.json()

        print("API Response:", data)  # For JSON inspection

        try:
            rate = data["rates"][to_currency]
            converted = round(amount * rate, 2)

            result = {
                "from": from_currency,
                "to": to_currency,
                "amount": amount,
                "converted": converted,
                "rate": rate
            }
        except KeyError:
            # Handle case where conversion rate is not available
            result = {
                "error": "Conversion failed. Please check the currency codes."
            }


    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
