# calculator_app.py

class Calculator:
    def __init__(self):
        self.input_value1 = None
        self.input_value2 = None
        self.operator = None
        self.result = None

    def set_input_value1(self, value):
        """Set the first input value"""
        self.input_value1 = value

    def set_input_value2(self, value):
        """Set the second input value"""
        self.input_value2 = value

    def set_operator(self, operator):
        """Set the arithmetic operator"""
        self.operator = operator

    def calculate(self):
        """Perform the calculation based on the input values and operator"""
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
        else:
            raise ValueError("Invalid operator")

    def clear(self):
        """Clear the calculator input and result"""
        self.input_value1 = None
        self.input_value2 = None
        self.operator = None
        self.result = None

    def get_result(self):
        """Get the calculation result"""
        return self.result


def main():
    calculator = Calculator()

    while True:
        print("Simple Calculator App")
        print("1. Set Input Value 1")
        print("2. Set Input Value 2")
        print("3. Set Operator")
        print("4. Calculate")
        print("5. Clear")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            value = float(input("Enter input value 1: "))
            calculator.set_input_value1(value)
        elif choice == '2':
            value = float(input("Enter input value 2: "))
            calculator.set_input_value2(value)
        elif choice == '3':
            operator = input("Enter operator (+, -, *, /): ")
            calculator.set_operator(operator)
        elif choice == '4':
            try:
                calculator.calculate()
                print("Result:", calculator.get_result())
            except ValueError as e:
                print("Error:", e)
        elif choice == '5':
            calculator.clear()
            print("Calculator cleared")
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()