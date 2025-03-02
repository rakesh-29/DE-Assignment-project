# test_calculator_app.py

import pytest
from calculator_app import Calculator, get_user_input, display_menu, handle_set_input_value, handle_set_operator, handle_calculate, handle_clear, handle_user_input

@pytest.fixture
def calculator():
    return Calculator()

def test_calculator_init(calculator):
    assert calculator.input_value1 is None
    assert calculator.input_value2 is None
    assert calculator.operator is None
    assert calculator.result is None

def test_set_input_value1(calculator):
    calculator.set_input_value1(5)
    assert calculator.input_value1 == 5

def test_set_input_value1_invalid(calculator):
    with pytest.raises(ValueError):
        calculator.set_input_value1("abc")

def test_set_input_value2(calculator):
    calculator.set_input_value2(10)
    assert calculator.input_value2 == 10

def test_set_input_value2_invalid(calculator):
    with pytest.raises(ValueError):
        calculator.set_input_value2("def")

def test_set_operator(calculator):
    calculator.set_operator("+")
    assert calculator.operator == "+"

def test_set_operator_invalid(calculator):
    with pytest.raises(ValueError):
        calculator.set_operator("^")

def test_calculate_addition(calculator):
    calculator.set_input_value1(2)
    calculator.set_input_value2(3)
    calculator.set_operator("+")
    calculator.calculate()
    assert calculator.result == 5

def test_calculate_subtraction(calculator):
    calculator.set_input_value1(5)
    calculator.set_input_value2(2)
    calculator.set_operator("-")
    calculator.calculate()
    assert calculator.result == 3

def test_calculate_multiplication(calculator):
    calculator.set_input_value1(4)
    calculator.set_input_value2(5)
    calculator.set_operator("*")
    calculator.calculate()
    assert calculator.result == 20

def test_calculate_division(calculator):
    calculator.set_input_value1(10)
    calculator.set_input_value2(2)
    calculator.set_operator("/")
    calculator.calculate()
    assert calculator.result == 5

def test_calculate_division_by_zero(calculator):
    calculator.set_input_value1(10)
    calculator.set_input_value2(0)
    calculator.set_operator("/")
    with pytest.raises(ValueError):
        calculator.calculate()

def test_clear(calculator):
    calculator.set_input_value1(5)
    calculator.set_input_value2(10)
    calculator.set_operator("+")
    calculator.clear()
    assert calculator.input_value1 is None
    assert calculator.input_value2 is None
    assert calculator.operator is None
    assert calculator.result is None

def test_get_result(calculator):
    calculator.set_input_value1(2)
    calculator.set_input_value2(3)
    calculator.set_operator("+")
    calculator.calculate()
    assert calculator.get_result() == 5

def test_get_user_input(monkeypatch):
    def mock_input(prompt):
        return "5"
    monkeypatch.setattr("builtins.input", mock_input)
    assert get_user_input("Enter a number: ") == "5"

def test_display_menu(capsys):
    display_menu()
    captured = capsys.readouterr()
    assert "Simple Calculator App" in captured.out
    assert "1. Set Input Value 1" in captured.out
    assert "2. Set Input Value 2" in captured.out
    assert "3. Set Operator" in captured.out
    assert "4. Calculate" in captured.out
    assert "5. Clear" in captured.out
    assert "6. Exit" in captured.out

def test_handle_set_input_value(calculator, monkeypatch):
    def mock_get_user_input(prompt):
        return "5"
    monkeypatch.setattr("calculator_app.get_user_input", mock_get_user_input)
    handle_set_input_value(calculator, "Enter input value 1: ")
    assert calculator.input_value1 == 5

def test_handle_set_operator(calculator, monkeypatch):
    def mock_get_user_input(prompt):
        return "+"
    monkeypatch.setattr("calculator_app.get_user_input", mock_get_user_input)
    handle_set_operator(calculator)
    assert calculator.operator == "+"

def test_handle_calculate(calculator, monkeypatch):
    def mock_get_user_input(prompt):
        return "5"
    monkeypatch.setattr("calculator_app.get_user_input", mock_get_user_input)
    calculator.set_input_value1(2)
    calculator.set_input_value2(3)
    calculator.set_operator("+")
    handle_calculate(calculator)
    assert calculator.result == 5

def test_handle_clear(calculator):
    calculator.set_input_value1(5)
    calculator.set_input_value2(10)
    calculator.set_operator("+")
    handle_clear(calculator)
    assert calculator.input_value1 is None
    assert calculator.input_value2 is None
    assert calculator.operator is None
    assert calculator.result is None

def test_handle_user_input(calculator, monkeypatch):
    def mock_get_user_input(prompt):
        return "1"
    monkeypatch.setattr("calculator_app.get_user_input", mock_get_user_input)
    handle_user_input(calculator)
    assert calculator.input_value1 == 5

def test_main(monkeypatch):
    def mock_handle_user_input(calculator):
        pass
    monkeypatch.setattr("calculator_app.handle_user_input", mock_handle_user_input)
    main()

