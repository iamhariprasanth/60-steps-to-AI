# ⚡ Unit Converter - Day 5 Challenge

A real-time unit conversion web application built with Flask that supports currency, temperature, length, and weight conversions with instant results and visual formulas.

## 🎯 Features

### ✨ Supported Conversions
- **💱 Currency**: INR ↔ USD (Real-time exchange rates)
- **🌡️ Temperature**: Celsius ↔ Fahrenheit 
- **📏 Length**: cm, inch, meter, km, mile conversions
- **⚖️ Weight**: kg, lb, g, oz, stone conversions

### 🚀 Key Capabilities
- **Real-time Conversion**: Instant results as you type
- **Live Formula Display**: See the calculation formula for every conversion
- **Swap Units**: Quick swap button to reverse conversions
- **Real Exchange Rates**: Currency converter fetches live rates from API
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Beautiful UI**: Modern gradient design with smooth animations
- **No Refresh Required**: Seamless AJAX-based conversions

## 📁 Project Structure

```
UnitConverter/
├── app.py                 # Flask backend with conversion logic
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main UI template
└── static/
    ├── css/
    │   └── style.css     # Styling and responsive design
    └── js/
        └── script.js     # Frontend logic and real-time conversions
```

## 🛠️ Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup Steps

1. **Navigate to the project directory**:
```bash
cd UnitConverter
```

2. **Create a virtual environment (optional but recommended)**:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## 🚀 Running the Application

1. **Start the Flask server**:
```bash
python app.py
```

2. **Open your browser** and navigate to:
```
http://localhost:5000
```

3. The application will be running with debug mode enabled for development.

## 💡 Usage Guide

### Currency Conversion
- Enter an amount in the "From" field
- Select currencies (INR or USD)
- Result appears instantly in the "To" field
- Real exchange rates are fetched in real-time
- Use the swap button to quickly reverse the conversion

### Temperature Conversion
- Enter temperature in either Celsius or Fahrenheit
- Select source and target units
- Instant conversion with formula display
- Common conversions: 0°C = 32°F, 100°C = 212°F

### Length Conversion
- Supports multiple units: cm, inch, meter, km, mile
- Mix and match any units for conversion
- Useful for international measurements

### Weight Conversion
- Supports: kg, lb, g, oz, stone
- Precise conversions with decimal accuracy
- Common conversions: 1 kg ≈ 2.2 lb

## 🔧 Technical Details

### Backend (Flask)
- **Conversion Endpoints**: `/api/convert` (POST)
- **Real-time Exchange Rates**: Fetches from exchangerate-api.com
- **Error Handling**: Graceful fallback to default rates if API fails
- **Decimal Precision**: Returns results rounded to 4 decimal places

### Frontend (HTML/CSS/JavaScript)
- **Tab Navigation**: Easy switching between conversion types
- **Real-time Updates**: Listens to input and select changes
- **Async API Calls**: Non-blocking conversions
- **Loading States**: Visual feedback during conversions
- **Animations**: Smooth transitions and success feedback

### Conversion Formulas

**Temperature**:
- C to F: (C × 9/5) + 32
- F to C: (F - 32) × 5/9

**Length** (all convert through cm):
- 1 inch = 2.54 cm
- 1 meter = 100 cm
- 1 km = 100,000 cm
- 1 mile ≈ 160,934 cm

**Weight** (all convert through kg):
- 1 lb ≈ 0.453592 kg
- 1 g = 0.001 kg
- 1 oz ≈ 0.0283495 kg
- 1 stone ≈ 6.35029 kg

## 📱 Responsive Design

The application is fully responsive with breakpoints for:
- **Desktop**: Full multi-column layout with swap buttons
- **Tablet**: Adjusted spacing and font sizes
- **Mobile**: Single column layout with optimized touch targets

## 🌐 API Endpoints

### POST /api/convert
Converts a value from one unit to another.

**Request Body**:
```json
{
  "type": "currency",           // "currency", "temperature", "length", "weight"
  "value": 100,                 // Numeric value to convert
  "from_unit": "INR",          // Source unit
  "to_unit": "USD"             // Target unit
}
```

**Response**:
```json
{
  "success": true,
  "result": 1.2,               // Converted value
  "formula": "100 INR × 0.012 = 1.2 USD"
}
```

## 🎨 Customization

### Changing Colors
Edit `static/css/style.css` to modify the gradient colors:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Adding More Units
1. Add unit options to HTML select elements in `templates/index.html`
2. Update conversion factors in `app.py`
3. Test the conversions

### Adjusting Precision
Change the rounding value in `app.py`:
```python
'result': round(result, 4)  # Change 4 to desired decimal places
```

## ⚠️ Notes

- Currency rates are cached during the session and refreshed on each conversion attempt
- If the exchange rate API is unavailable, the app uses a fallback rate
- All other conversions use fixed, standardized conversion factors
- The app includes comprehensive error handling for invalid inputs

## 🐛 Troubleshooting

**Exchange rates not updating**: Check internet connection and API availability
**Conversions not working**: Ensure Flask server is running (check http://localhost:5000)
**CSS/JS not loading**: Clear browser cache (Ctrl+Shift+Delete or Cmd+Shift+Delete)
**Port already in use**: Change port in `app.py`: `app.run(debug=True, port=5001)`

## 📊 Performance

- **Real-time Results**: <100ms typical response time
- **API Calls**: Only for currency conversions (cached per session)
- **Lightweight**: All calculations done client-side where possible
- **Optimized**: Minimal network requests and fast computation

## 🔐 Security

- Input validation on both frontend and backend
- No sensitive data stored
- CORS-friendly (can be extended for API use)
- Error messages don't expose system details

## 📈 Future Enhancements

- Add more currency pairs
- Support for Kelvin temperature
- Historical exchange rate tracking
- Unit conversion history
- Favorited conversions
- Dark mode theme
- Offline support with cached rates

## 🎓 Learning Outcomes

This project demonstrates:
- Flask web framework fundamentals
- Real-time API integration
- Asynchronous JavaScript (AJAX/Fetch API)
- Responsive web design
- Form handling and validation
- Error handling and user feedback
- Mathematical conversions

## 📝 License

This project is created for educational purposes as part of the "60 Steps to AI" challenge.

---

**Happy Converting! 🎉**
