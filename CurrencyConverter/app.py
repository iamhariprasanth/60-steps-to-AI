from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Static exchange rates (base: 1 INR)
EXCHANGE_RATES = {
    'INR': 1.0,
    'USD': 0.012,      # 1 INR = 0.012 USD
    'EUR': 0.011,      # 1 INR = 0.011 EUR
    'GBP': 0.0095      # 1 INR = 0.0095 GBP
}

# Currency symbols
CURRENCY_SYMBOLS = {
    'INR': '₹',
    'USD': '$',
    'EUR': '€',
    'GBP': '£'
}

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', currencies=EXCHANGE_RATES.keys())

@app.route('/convert', methods=['POST'])
def convert():
    """Convert currency"""
    try:
        data = request.json
        amount = float(data.get('amount', 0))
        from_currency = data.get('from_currency', 'INR')
        to_currency = data.get('to_currency', 'USD')
        
        # Convert to INR first (base currency)
        amount_in_inr = amount / EXCHANGE_RATES[from_currency]
        
        # Convert from INR to target currency
        converted_amount = amount_in_inr * EXCHANGE_RATES[to_currency]
        
        # Get exchange rate
        rate = EXCHANGE_RATES[to_currency] / EXCHANGE_RATES[from_currency]
        
        return jsonify({
            'success': True,
            'amount': amount,
            'from_currency': from_currency,
            'to_currency': to_currency,
            'converted_amount': round(converted_amount, 2),
            'rate': round(rate, 6),
            'from_symbol': CURRENCY_SYMBOLS[from_currency],
            'to_symbol': CURRENCY_SYMBOLS[to_currency]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/get-rates')
def get_rates():
    """Get all exchange rates"""
    return jsonify({
        'rates': EXCHANGE_RATES,
        'symbols': CURRENCY_SYMBOLS
    })

if __name__ == '__main__':
    app.run(debug=True, port=5003)
