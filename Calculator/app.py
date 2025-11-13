from flask import Flask, render_template, request, jsonify


def create_app() -> Flask:
    """Application factory for the Calculator Flask app."""
    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def index():
        """Render the calculator page."""
        return render_template("index.html")

    @app.route("/calculate", methods=["POST"])
    def calculate():
        """Calculate the result based on two numbers and an operation."""
        try:
            data = request.get_json()
            num1 = float(data.get("num1", 0))
            num2 = float(data.get("num2", 0))
            operation = data.get("operation", "+")

            result = perform_calculation(num1, num2, operation)

            return jsonify({
                "success": True,
                "result": result
            })
        except (ValueError, TypeError) as e:
            return jsonify({
                "success": False,
                "error": "Invalid input. Please enter valid numbers."
            }), 400
        except ZeroDivisionError:
            return jsonify({
                "success": False,
                "error": "Division by zero is not allowed."
            }), 400
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"An error occurred: {str(e)}"
            }), 500

    return app


def perform_calculation(num1: float, num2: float, operation: str) -> float:
    """Perform the mathematical operation."""
    operations = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b if b != 0 else None,
        "%": lambda a, b: a % b if b != 0 else None,
        "**": lambda a, b: a ** b,
    }

    if operation not in operations:
        raise ValueError(f"Unsupported operation: {operation}")

    result = operations[operation](num1, num2)
    
    if result is None:
        raise ZeroDivisionError("Division by zero")
    
    return round(result, 10)


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True, port=5002)

