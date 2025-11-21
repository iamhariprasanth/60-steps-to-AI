// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all tabs and buttons
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelectorAll('.tab-btn').forEach(b => {
            b.classList.remove('active');
        });

        // Add active class to clicked button and corresponding tab
        btn.classList.add('active');
        const tabName = btn.getAttribute('data-tab');
        document.getElementById(tabName).classList.add('active');
    });
});

// Conversion types configuration
const converters = {
    currency: {
        inputId: 'currency-from',
        outputId: 'currency-to',
        fromUnitId: 'currency-from-unit',
        toUnitId: 'currency-to-unit',
        formulaId: 'currency-formula'
    },
    temperature: {
        inputId: 'temp-from',
        outputId: 'temp-to',
        fromUnitId: 'temp-from-unit',
        toUnitId: 'temp-to-unit',
        formulaId: 'temperature-formula'
    },
    length: {
        inputId: 'length-from',
        outputId: 'length-to',
        fromUnitId: 'length-from-unit',
        toUnitId: 'length-to-unit',
        formulaId: 'length-formula'
    },
    weight: {
        inputId: 'weight-from',
        outputId: 'weight-to',
        fromUnitId: 'weight-from-unit',
        toUnitId: 'weight-to-unit',
        formulaId: 'weight-formula'
    }
};

// Initialize event listeners
function initializeConverters() {
    Object.keys(converters).forEach(type => {
        const config = converters[type];
        const input = document.getElementById(config.inputId);
        const fromUnit = document.getElementById(config.fromUnitId);
        const toUnit = document.getElementById(config.toUnitId);

        // Real-time conversion on input change
        input.addEventListener('input', () => performConversion(type));
        input.addEventListener('change', () => performConversion(type));

        // Real-time conversion on unit change
        fromUnit.addEventListener('change', () => performConversion(type));
        toUnit.addEventListener('change', () => performConversion(type));
    });
}

// Perform conversion via API
async function performConversion(type) {
    const config = converters[type];
    const value = parseFloat(document.getElementById(config.inputId).value) || 0;
    const fromUnit = document.getElementById(config.fromUnitId).value;
    const toUnit = document.getElementById(config.toUnitId).value;
    const outputField = document.getElementById(config.outputId);
    const formulaField = document.getElementById(config.formulaId);

    try {
        // Show loading state
        outputField.classList.add('loading');
        formulaField.textContent = 'Converting...';

        const response = await fetch('/api/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: type,
                value: value,
                from_unit: fromUnit,
                to_unit: toUnit
            })
        });

        const data = await response.json();

        // Remove loading state
        outputField.classList.remove('loading');

        if (data.success) {
            outputField.value = data.result || '';
            formulaField.textContent = data.formula || '';
            
            // Add success animation
            outputField.classList.add('success');
            setTimeout(() => {
                outputField.classList.remove('success');
            }, 500);
        } else {
            outputField.value = '';
            formulaField.textContent = '❌ ' + (data.error || 'Conversion error');
        }
    } catch (error) {
        console.error('Error:', error);
        outputField.classList.remove('loading');
        outputField.value = '';
        formulaField.textContent = '❌ Network error. Please try again.';
    }
}

// Swap units function
async function swapUnits(type) {
    const config = converters[type];
    const input = document.getElementById(config.inputId);
    const output = document.getElementById(config.outputId);
    const fromUnit = document.getElementById(config.fromUnitId);
    const toUnit = document.getElementById(config.toUnitId);

    // Swap input/output values
    const tempValue = input.value;
    input.value = output.value || 0;
    output.value = tempValue;

    // Swap units
    const tempUnit = fromUnit.value;
    fromUnit.value = toUnit.value;
    toUnit.value = tempUnit;

    // Perform conversion with swapped units
    performConversion(type);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeConverters();
    // Trigger initial conversion for each converter
    performConversion('currency');
    performConversion('temperature');
    performConversion('length');
    performConversion('weight');
});

// Handle Enter key to trigger conversion
document.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        Object.keys(converters).forEach(type => {
            const config = converters[type];
            const input = document.getElementById(config.inputId);
            if (input === document.activeElement) {
                performConversion(type);
            }
        });
    }
});
