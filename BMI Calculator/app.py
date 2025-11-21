from flask import Flask, render_template, request


def create_app() -> Flask:
    """Application factory for the Day 4 Challenge BMI Calculator."""
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        height = 0
        weight = 0
        bmi_value = None
        bmi_category = None

        if request.method == "POST":
            try:
                height = float(request.form.get("height", height))
                weight = float(request.form.get("weight", weight))
            except (TypeError, ValueError):
                height = 0
                weight = 0

            if height > 0 and weight > 0:
                bmi_value, bmi_category = calculate_bmi(height, weight)

        return render_template(
            "index.html",
            height=height,
            weight=weight,
            bmi_value=bmi_value,
            bmi_category=bmi_category,
        )

    return app


def calculate_bmi(height_cm: float, weight_kg: float) -> tuple[float, str]:
    """
    Calculate BMI and return the value and category.
    
    Args:
        height_cm: Height in centimeters
        weight_kg: Weight in kilograms
    
    Returns:
        Tuple of (BMI value, category string)
    """
    # Convert height from cm to meters
    height_m = height_cm / 100
    
    # Calculate BMI
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
    
    return round(bmi, 1), category


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)

