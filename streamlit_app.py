import streamlit as st

# Initialize session state for calculator
if 'display' not in st.session_state:
    st.session_state.display = '0'
if 'current' not in st.session_state:
    st.session_state.current = '0'
if 'previous' not in st.session_state:
    st.session_state.previous = '0'
if 'operator' not in st.session_state:
    st.session_state.operator = None
if 'waiting_for_operand' not in st.session_state:
    st.session_state.waiting_for_operand = False

def update_display(value):
    st.session_state.display = value

def button_click(value):
    if st.session_state.waiting_for_operand:
        st.session_state.current = value
        st.session_state.waiting_for_operand = False
    else:
        st.session_state.current = st.session_state.current + value if st.session_state.current != '0' else value
    update_display(st.session_state.current)

def operator_click(op):
    st.session_state.previous = st.session_state.current
    st.session_state.operator = op
    st.session_state.waiting_for_operand = True

def equals_click():
    if st.session_state.operator:
        try:
            left = float(st.session_state.previous)
            right = float(st.session_state.current)
            if st.session_state.operator == '+':
                result = left + right
            elif st.session_state.operator == '-':
                result = left - right
            elif st.session_state.operator == '*':
                result = left * right
            elif st.session_state.operator == '/':
                if right != 0:
                    result = left / right
                else:
                    result = 'Error'
            else:
                result = st.session_state.current
            st.session_state.display = str(result) if isinstance(result, (int, float)) else result
            st.session_state.current = st.session_state.display
            st.session_state.operator = None
            st.session_state.waiting_for_operand = True
        except ValueError:
            st.session_state.display = 'Error'
            st.session_state.current = '0'
            st.session_state.previous = '0'
            st.session_state.operator = None
            st.session_state.waiting_for_operand = False

def clear_click():
    st.session_state.display = '0'
    st.session_state.current = '0'
    st.session_state.previous = '0'
    st.session_state.operator = None
    st.session_state.waiting_for_operand = False

# Streamlit UI
st.title("Simple Calculator")

# Display
st.text_input("Result:", value=st.session_state.display, disabled=True)

# Button rows
# Row 1: 7 8 9 /
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button('7'):
        button_click('7')
with c2:
    if st.button('8'):
        button_click('8')
with c3:
    if st.button('9'):
        button_click('9')
with c4:
    if st.button("DIV"):
        operator_click('/')

# Row 2: 4 5 6 *
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button('4'):
        button_click('4')
with c2:
    if st.button('5'):
        button_click('5')
with c3:
    if st.button('6'):
        button_click('6')
with c4:
    if st.button("MUL"):
        operator_click('*')

# Row 3: 1 2 3 -
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button('1'):
        button_click('1')
with c2:
    if st.button('2'):
        button_click('2')
with c3:
    if st.button('3'):
        button_click('3')
with c4:
    if st.button("SUB"):
        operator_click('-')

# Row 4: C 0 = +
c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button('C'):
        clear_click()
with c2:
    if st.button('0'):
        button_click('0')
with c3:
    if st.button('='):
        equals_click()
with c4:
    if st.button("ADD"):
        operator_click('+')