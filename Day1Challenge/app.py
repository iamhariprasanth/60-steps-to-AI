from flask import Flask, render_template, request


def create_app() -> Flask:
    """Application factory for the Day 1 Challenge Flask app."""
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        name = ""
        age = 25
        greeting = None
        compliment = None

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            try:
                age = int(request.form.get("age", age))
            except (TypeError, ValueError):
                age = 25

            if name:
                greeting = f"It's wonderful to meet you! You are {age} years old."
                compliment = select_compliment(age)

        return render_template(
            "index.html",
            name=name,
            age=age,
            greeting=greeting,
            compliment=compliment,
        )

    return app


def select_compliment(age: int) -> str:
    """Return a playful compliment based on age."""
    if age <= 12:
        return "You're a bundle of energy and curiosity! 🌟"
    if age <= 19:
        return "You're writing an incredible story—keep turning the pages! 📚"
    if age <= 35:
        return "You're in the prime of your life! 🚀"
    if age <= 55:
        return "Your experience makes every moment brighter. ✨"
    return "Your wisdom lights the way for everyone around you. 🌈"


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)

