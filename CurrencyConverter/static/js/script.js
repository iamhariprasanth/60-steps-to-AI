// Currency symbols mapping
const SYMBOLS = {
    'INR': '₹',
    'USD': '$',
    'EUR': '€',
    'GBP': '£'
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    loadExchangeRates();
    convertCurrency();
});

function setupEventListeners() {
    const fromAmount = document.getElementById('from-amount');
    const fromCurrency = document.getElementById('from-currency');
    const toCurrency = document.getElementById('to-currency');
    const swapBtn = document.getElementById('swap-btn');

    // Convert on input change
    fromAmount.addEventListener('input', convertCurrency);
    fromCurrency.addEventListener('change', convertCurrency);
    toCurrency.addEventListener('change', convertCurrency);

    // Swap currencies
    swapBtn.addEventListener('click', swapCurrencies);
}

async function convertCurrency() {
    const amount = parseFloat(document.getElementById('from-amount').value) || 0;
    const fromCurrency = document.getElementById('from-currency').value;
    const toCurrency = document.getElementById('to-currency').value;

    try {
        const response = await fetch('/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                amount: amount,
                from_currency: fromCurrency,
                to_currency: toCurrency
            })
        });

        const data = await response.json();

        if (data.success) {
            // Update converted amount
            document.getElementById('to-amount').value = data.converted_amount;

            // Update displays
            updateDisplay('from-display', data.from_symbol, data.amount);
            updateDisplay('to-display', data.to_symbol, data.converted_amount);

            // Update rate info
            updateRateInfo(data);

            // Update quick conversion
            updateQuickConversion(fromCurrency, toCurrency);
        }
    } catch (error) {
        console.error('Conversion error:', error);
    }
}

function updateDisplay(elementId, symbol, amount) {
    const display = document.getElementById(elementId);
    display.textContent = `${symbol} ${formatNumber(amount)}`;
    
    // Add animation
    display.style.animation = 'none';
    setTimeout(() => {
        display.style.animation = 'scaleIn 0.3s ease';
    }, 10);
}

function updateRateInfo(data) {
    const rateInfo = document.getElementById('rate-info');
    rateInfo.querySelector('.rate-text').textContent = 
        `1 ${data.from_currency} = ${data.rate} ${data.to_currency}`;
}

function swapCurrencies() {
    const fromCurrency = document.getElementById('from-currency');
    const toCurrency = document.getElementById('to-currency');

    // Swap values
    const temp = fromCurrency.value;
    fromCurrency.value = toCurrency.value;
    toCurrency.value = temp;

    // Get the converted amount and set it as the new input
    const toAmount = document.getElementById('to-amount').value;
    document.getElementById('from-amount').value = toAmount || 0;

    // Convert with new values
    convertCurrency();
}

async function loadExchangeRates() {
    try {
        const response = await fetch('/get-rates');
        const data = await response.json();

        populateRatesTable(data.rates, data.symbols);
    } catch (error) {
        console.error('Error loading rates:', error);
    }
}

function populateRatesTable(rates, symbols) {
    const tbody = document.getElementById('rates-tbody');
    tbody.innerHTML = '';

    const currencies = ['INR', 'USD', 'EUR', 'GBP'];
    const names = {
        'INR': 'Indian Rupee',
        'USD': 'US Dollar',
        'EUR': 'Euro',
        'GBP': 'British Pound'
    };

    currencies.forEach(currency => {
        const row = document.createElement('tr');
        
        const rateToINR = 1 / rates[currency];
        const rateFromINR = rates[currency];

        row.innerHTML = `
            <td class="currency-name">${names[currency]}</td>
            <td class="currency-symbol">${symbols[currency]}</td>
            <td class="rate-value">${formatNumber(rateToINR, 4)}</td>
            <td class="rate-value">${formatNumber(rateFromINR, 6)}</td>
        `;

        tbody.appendChild(row);
    });
}

function updateQuickConversion(fromCurrency, toCurrency) {
    const grid = document.getElementById('conversion-grid');
    grid.innerHTML = '';

    const amounts = [1, 10, 100, 1000, 10000, 100000];

    amounts.forEach(async amount => {
        const response = await fetch('/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                amount: amount,
                from_currency: fromCurrency,
                to_currency: toCurrency
            })
        });

        const data = await response.json();

        if (data.success) {
            const item = document.createElement('div');
            item.className = 'conversion-item';
            item.innerHTML = `
                <div class="conversion-from">${data.from_symbol} ${formatNumber(amount)}</div>
                <div class="conversion-to">${data.to_symbol} ${formatNumber(data.converted_amount)}</div>
            `;
            grid.appendChild(item);
        }
    });
}

function formatNumber(num, decimals = 2) {
    return parseFloat(num).toLocaleString('en-US', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    });
}
