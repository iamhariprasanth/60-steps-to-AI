# Day 1 Challenge – Greeting Form

This mini-project is the first step in the 60 Steps to AI journey. It is a simple Flask application that displays a form asking for a visitor's name and age (via slider) and produces a personalized greeting.

## Getting Started

1. Create a virtual environment (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   flask --app app run --debug
   ```

The app will be available at `http://127.0.0.1:5000/`.

## Project Structure

- `app.py`: Flask application with a single route handling the form.
- `templates/index.html`: HTML template containing the form and greeting display.
- `requirements.txt`: Python dependencies for the project.

## Next Steps

- Add validation or additional form fields.
- Persist form submissions to a database or file.
- Deploy to a hosting service once ready to share.

