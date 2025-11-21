from flask import Flask, render_template, request, jsonify


def create_app() -> Flask:
    """Application factory for the BMI Calculator Flask app."""
    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def index():
        """Render the BMI calculator page."""
        return render_template("index.html")

    @app.route("/calculate", methods=["POST"])
    def calculate():
        """Calculate BMI from height (cm) and weight (kg)."""
        try:
            data = request.get_json()
            height_cm = float(data.get("height", 0))
            weight_kg = float(data.get("weight", 0))

            # Validate inputs
            if height_cm <= 0 or weight_kg <= 0:
                return jsonify({
                    "success": False,
                    "error": "Height and weight must be greater than zero."
                }), 400

            if height_cm > 300:
                return jsonify({
                    "success": False,
                    "error": "Height seems unrealistic. Please enter height in centimeters."
                }), 400

            if weight_kg > 1000:
                return jsonify({
                    "success": False,
                    "error": "Weight seems unrealistic. Please enter weight in kilograms."
                }), 400

            bmi_value, category = calculate_bmi(height_cm, weight_kg)

            return jsonify({
                "success": True,
                "bmi": bmi_value,
                "category": category
            })
        except (ValueError, TypeError) as e:
            return jsonify({
                "success": False,
                "error": "Invalid input. Please enter valid numbers."
            }), 400
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"An error occurred: {str(e)}"
            }), 500

    return app


def calculate_bmi(height_cm: float, weight_kg: float) -> tuple[float, str]:
    """
    Calculate BMI from height in centimeters and weight in kilograms.
    
    Args:
        height_cm: Height in centimeters
        weight_kg: Weight in kilograms
    
    Returns:
        Tuple of (BMI value, BMI category)
    """
    # Convert height from cm to meters
    height_m = height_cm / 100
    
    # Calculate BMI: weight (kg) / height (m)²
    bmi = weight_kg / (height_m ** 2)
    
    # Determine category
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    
    # Round BMI to 1 decimal place
    return round(bmi, 1), category


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True, port=5002)

