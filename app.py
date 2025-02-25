from flask import Flask, request, render_template_string

app = Flask(__name__)

# Factorial Function
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

# Prime Number Check Function
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Fibonacci Series Function
def fibonacci(n):
    fib_series = [0, 1]
    for i in range(2, n):
        fib_series.append(fib_series[-1] + fib_series[-2])
    return fib_series[:n]

# HTML Form Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Logic Demo</title>
</head>
<body>
    <h2>Enter a Number</h2>
    <form method="post">
        <input type="number" name="number" required>
        <button type="submit">Submit</button>
    </form>

    {% if number is not none %}
        <h3>Results for Number: {{ number }}</h3>
        <p>Factorial: {{ factorial }}</p>
        <p>Prime Check: {{ prime }}</p>
        <p>Fibonacci Series: {{ fibonacci }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    number = None
    factorial_result = None
    prime_result = None
    fibonacci_result = None

    if request.method == "POST":
        number = int(request.form["number"])
        factorial_result = factorial(number)
        prime_result = "Yes" if is_prime(number) else "No"
        fibonacci_result = fibonacci(number)

    return render_template_string(HTML_TEMPLATE, number=number, factorial=factorial_result, prime=prime_result, fibonacci=fibonacci_result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

