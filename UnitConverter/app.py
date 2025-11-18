from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Exchange rate cache (in production, use a database or cache like Redis)
EXCHANGE_RATES = {}

def get_exchange_rate():
    """Fetch current exchange rates from an API"""
    try:
        # Using a free exchange rate API
        response = requests.get('https://api.exchangerate-api.com/v4/latest/INR', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data['rates'].get('USD', 0.012)  # Fallback rate if API fails
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
    return 0.012  # Fallback to approximate rate

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/convert', methods=['POST'])
def convert():
    """API endpoint for real-time conversions"""
    try:
        data = request.json
        conversion_type = data.get('type')
        value = float(data.get('value', 0))
        from_unit = data.get('from_unit')
        to_unit = data.get('to_unit')

        result = None
        formula = ""

        if conversion_type == 'currency':
            result, formula = convert_currency(value, from_unit, to_unit)
        elif conversion_type == 'temperature':
            result, formula = convert_temperature(value, from_unit, to_unit)
        elif conversion_type == 'length':
            result, formula = convert_length(value, from_unit, to_unit)
        elif conversion_type == 'weight':
            result, formula = convert_weight(value, from_unit, to_unit)

        return jsonify({
            'success': True,
            'result': round(result, 4) if result is not None else None,
            'formula': formula
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

def convert_currency(value, from_unit, to_unit):
    """Convert between currencies"""
    if from_unit == to_unit:
        return value, f"{value} {from_unit} = {value} {to_unit}"
    
    # Get fresh exchange rate
    rate = get_exchange_rate()
    
    if from_unit == 'INR' and to_unit == 'USD':
        result = value * rate
        formula = f"{value} INR × {rate} = {result} USD"
    elif from_unit == 'USD' and to_unit == 'INR':
        result = value / rate
        formula = f"{value} USD ÷ {rate} = {result} INR"
    else:
        return None, ""
    
    return result, formula

def convert_temperature(value, from_unit, to_unit):
    """Convert between temperature units"""
    if from_unit == to_unit:
        return value, f"{value}° {from_unit} = {value}° {to_unit}"
    
    if from_unit == 'C' and to_unit == 'F':
        result = (value * 9/5) + 32
        formula = f"({value} × 9/5) + 32 = {result}° F"
    elif from_unit == 'F' and to_unit == 'C':
        result = (value - 32) * 5/9
        formula = f"({value} - 32) × 5/9 = {result}° C"
    else:
        return None, ""
    
    return result, formula

def convert_length(value, from_unit, to_unit):
    """Convert between length units"""
    if from_unit == to_unit:
        return value, f"{value} {from_unit} = {value} {to_unit}"
    
    # Convert to cm first
    to_cm = {
        'cm': 1,
        'inch': 2.54,
        'meter': 100,
        'km': 100000,
        'mile': 160934
    }
    
    if from_unit not in to_cm or to_unit not in to_cm:
        return None, ""
    
    cm_value = value * to_cm[from_unit]
    result = cm_value / to_cm[to_unit]
    formula = f"{value} {from_unit} = {result} {to_unit}"
    
    return result, formula

def convert_weight(value, from_unit, to_unit):
    """Convert between weight units"""
    if from_unit == to_unit:
        return value, f"{value} {from_unit} = {value} {to_unit}"
    
    # Convert to kg first
    to_kg = {
        'kg': 1,
        'lb': 0.453592,
        'g': 0.001,
        'oz': 0.0283495,
        'stone': 6.35029
    }
    
    if from_unit not in to_kg or to_unit not in to_kg:
        return None, ""
    
    kg_value = value * to_kg[from_unit]
    result = kg_value / to_kg[to_unit]
    formula = f"{value} {from_unit} = {result} {to_unit}"
    
    return result, formula

if __name__ == '__main__':
    app.run(debug=True, port=5000)
