# BMI Calculator 🏋️

A beautiful, modern BMI (Body Mass Index) calculator web application built with Flask that calculates your BMI and categorizes it.

## Features

- **Height Input**: Enter your height in centimeters (cm)
- **Weight Input**: Enter your weight in kilograms (kg)
- **Instant Calculation**: BMI updates automatically as you type
- **Category Display**: Shows BMI category with color-coded badges (Underweight/Normal/Overweight/Obese)
- **Modern UI**: Sleek, dark-themed design with gradient backgrounds
- **Error Handling**: Validates inputs and handles errors gracefully
- **Responsive Design**: Works perfectly on desktop and mobile devices

## Installation

1. Navigate to the Calculator directory:
```bash
cd Calculator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Run the Flask application:
```bash
python app.py
```

The BMI calculator will be available at `http://localhost:5002`

## Usage

1. Enter your height in centimeters (cm) in the "Height (cm)" field
2. Enter your weight in kilograms (kg) in the "Weight (kg)" field
3. Your BMI value and category will be displayed instantly
4. Click "Clear" to reset all inputs

## BMI Categories

- **Underweight**: BMI < 18.5 (Blue badge)
- **Normal**: 18.5 ≤ BMI < 25 (Green badge)
- **Overweight**: 25 ≤ BMI < 30 (Orange badge)
- **Obese**: BMI ≥ 30 (Red badge)

## BMI Formula

BMI = Weight (kg) / Height (m)²

The calculator automatically converts height from centimeters to meters for the calculation.

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Modern CSS with gradients and animations

