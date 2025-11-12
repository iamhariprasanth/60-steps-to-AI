# Expense Splitter 💰

A Flask web application to split expenses fairly among friends for dinners, trips, or any group activities.

## Features

- ✅ Enter total amount and number of people
- ✅ Add names and email IDs (optional but unique)
- ✅ Track individual contributions
- ✅ Calculate who owes or gets back money
- ✅ Show detailed transactions
- ✅ Fully responsive mobile-friendly design

## Installation

1. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
flask --app app run --debug
```

Or directly:
```bash
python app.py
```

Then open your browser and navigate to `http://localhost:5000`

## How to Use

1. Enter the **total bill amount**
2. Enter the **number of people** splitting the bill
3. For each person, optionally add:
   - Name (must be unique if provided)
   - Email ID (must be unique if provided, validated format)
   - Contribution amount (how much they already paid)
4. Click **Calculate Split** to see:
   - How much each person should pay
   - Who owes money and to whom
   - Who gets money back and from whom
   - Detailed transaction breakdown

## Example

- Total bill: ₹1000
- 3 people:
  - Alice paid ₹500
  - Bob paid ₹200
  - Charlie paid ₹0

Result:
- Each should pay: ₹333.33
- Alice gets back: ₹166.67
- Bob owes: ₹133.33
- Charlie owes: ₹333.33

Transactions:
- Bob → Alice: ₹133.33
- Charlie → Alice: ₹33.34

## Validation

- Names must be unique (if provided)
- Email IDs must be unique and valid format (if provided)
- Contributions cannot be negative
- At least one person must have a name or email

## Technology Stack

- Python 3
- Flask
- HTML5/CSS3 (responsive design)
- Vanilla JavaScript

