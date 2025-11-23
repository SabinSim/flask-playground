from flask import Flask, render_template, request

# Initialize the Flask application
app = Flask(__name__)

# Main page route (input form)
@app.route("/")
def index():
    # Render the index.html template for user input
    return render_template("index.html")

# Calculation processing route
@app.route("/calculate", methods=["POST"])
def calculate():
    # Retrieve form data
    try:
        num1 = float(request.form["num1"])
        num2 = float(request.form["num2"])
        operation = request.form["operation"]
    except ValueError:
        # Handle cases where input is not a valid number
        result = "Invalid input: Please enter valid numbers."
        operation = "error"
        num1 = 0
        num2 = 0
        return render_template("result.html",
                               num1=num1, num2=num2,
                               operation=operation, result=result)

    # Calculation logic
    if operation == "add":
        result = num1 + num2
    elif operation == "sub":
        result = num1 - num2
    elif operation == "mul":
        result = num1 * num2
    elif operation == "div":
        if num2 == 0:
            # Handle division by zero error
            result = "Cannot divide by zero."
        else:
            result = num1 / num2
    else:
        # Handle unexpected operation values
        result = "Invalid operation."

    # Render the result.html template with the results
    return render_template("result.html",
                           num1=num1, num2=num2,
                           operation=operation, result=result)

if __name__ == "__main__":
    # Run the application in debug mode
    app.run(debug=True)
