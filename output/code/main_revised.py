# calculator_app.py

import time

class Calculator:
    def __init__(self):
        self.input_value1 = None
        self.input_value2 = None
        self.operator = None
        self.result = None

    def set_input_value1(self, value):
        """Set the first input value"""
        if not self._is_valid_number(value):
            raise ValueError("Invalid input value. Please enter a number.")
        self.input_value1 = value

    def set_input_value2(self, value):
        """Set the second input value"""
        if not self._is_valid_number(value):
            raise ValueError("Invalid input value. Please enter a number.")
        self.input_value2 = value

    def set_operator(self, operator):
        """Set the arithmetic operator"""
        if operator not in ['+', '-', '*', '/']:
            raise ValueError("Invalid operator. Please enter one of the following: +, -, *, /")
        self.operator = operator

    def calculate(self):
        """Perform the calculation based on the input values and operator"""
        start_time = time.time()
        try:
            if self.operator == '+':
                self.result = self.input_value1 + self.input_value2
            elif self.operator == '-':
                self.result = self.input_value1 - self.input_value2
            elif self.operator == '*':
                self.result = self.input_value1 * self.input_value2
            elif self.operator == '/':
                if self.input_value2 != 0:
                    self.result = self.input_value1 / self.input_value2
                else:
                    raise ValueError("Division by zero is not allowed")
            calculation_time = time.time() - start_time
            if calculation_time > 0.05:
                print("Calculation took {:.2f}ms, which exceeds the 50ms performance requirement.".format(calculation_time * 1000))
        except Exception as e:
            raise ValueError("Error occurred during calculation: {}".format(e))

    def clear(self):
        """Clear the calculator input and result"""
        self.input_value1 = None
        self.input_value2 = None
        self.operator = None
        self.result = None

    def get_result(self):
        """Get the calculation result"""
        return self.result

    def _is_valid_number(self, value):
        """Check if the input value is a valid number"""
        try:
            float(value)
            return True
        except ValueError:
            return False


def get_user_input(prompt):
    """Get user input and validate it"""
    while True:
        try:
            value = input(prompt)
            if value.strip() == "":
                raise ValueError("Input cannot be empty")
            return value
        except ValueError as e:
            print("Invalid input. Please try again. {}".format(e))


def display_menu():
    """Display the calculator menu"""
    print("Simple Calculator App")
    print("1. Set Input Value 1")
    print("2. Set Input Value 2")
    print("3. Set Operator")
    print("4. Calculate")
    print("5. Clear")
    print("6. Exit")


def handle_set_input_value(calculator, prompt):
    """Handle setting input values"""
    value = get_user_input(prompt)
    try:
        calculator.set_input_value1(float(value)) if prompt == "Enter input value 1: " else calculator.set_input_value2(float(value))
    except ValueError as e:
        print("Error:", e)


def handle_set_operator(calculator):
    """Handle setting the operator"""
    operator = get_user_input("Enter operator (+, -, *, /): ")
    try:
        calculator.set_operator(operator)
    except ValueError as e:
        print("Error:", e)


def handle_calculate(calculator):
    """Handle calculation"""
    try:
        calculator.calculate()
        print("Result:", calculator.get_result())
    except ValueError as e:
        print("Error:", e)


def handle_clear(calculator):
    """Handle clearing the calculator"""
    calculator.clear()
    print("Calculator cleared")


def handle_user_input(calculator):
    """Handle user input and perform calculations"""
    while True:
        display_menu()
        choice = get_user_input("Enter your choice: ")

        if choice == '1':
            handle_set_input_value(calculator, "Enter input value 1: ")
        elif choice == '2':
            handle_set_input_value(calculator, "Enter input value 2: ")
        elif choice == '3':
            handle_set_operator(calculator)
        elif choice == '4':
            handle_calculate(calculator)
        elif choice == '5':
            handle_clear(calculator)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    calculator = Calculator()
    handle_user_input(calculator)


if __name__ == "__main__":
    main()