import streamlit as st
from calculator_app import Calculator

# Create a Streamlit app title and header
st.title("Simple Calculator App")
st.header("Perform arithmetic operations with ease!")

# Create a calculator instance
calculator = Calculator()

# Create input fields for input values and operator
input_value1 = st.text_input("Enter input value 1:", value="", key="input_value1")
input_value2 = st.text_input("Enter input value 2:", value="", key="input_value2")
operator = st.selectbox("Select operator:", ["+", "-", "*", "/"], key="operator")

# Create a calculate button
calculate_button = st.button("Calculate")

# Create a clear button
clear_button = st.button("Clear")

# Create a result display area
result_area = st.text_area("Result:", value="", height=100, key="result_area")

# Handle calculate button click
if calculate_button:
    try:
        calculator.set_input_value1(float(input_value1))
        calculator.set_input_value2(float(input_value2))
        calculator.set_operator(operator)
        calculator.calculate()
        result_area.value = str(calculator.get_result())
    except ValueError as e:
        st.error("Error: {}".format(e))

# Handle clear button click
if clear_button:
    calculator.clear()
    input_value1 = ""
    input_value2 = ""
    operator = "+"
    result_area.value = ""

# Run the app
if __name__ == "__main__":
    st.write("Welcome to the Simple Calculator App!")