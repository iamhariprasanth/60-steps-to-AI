# Day 4 Challenge - BMI Calculator 🏋️

A web-based Body Mass Index (BMI) calculator built with Flask.

## Features

- Input height in centimeters (cm)
- Input weight in kilograms (kg)
- Calculate BMI value
- Display BMI category:
  - **Underweight**: BMI < 18.5
  - **Normal**: 18.5 ≤ BMI < 25
  - **Overweight**: 25 ≤ BMI < 30
  - **Obese**: BMI ≥ 30

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Flask application:
```bash
python app.py
```

Then open your browser and navigate to `http://localhost:5000`

## BMI Formula

BMI = weight (kg) / (height (m))²

Since height is input in centimeters, the formula converts it to meters:
BMI = weight (kg) / ((height (cm) / 100)²)

