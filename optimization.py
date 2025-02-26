class Calculator:
    def __init__(self):
        # 建立算法，並且綁定符號
        self.operations = {
            '+': self.add,
            '-': self.subtract,
            '*': self.multiply,
            '/': self.divide,
        }

    def add(self, a, b):
        '''執行加法'''

        return a + b
    
    def subtract(self, a, b):
        '''執行減法'''

        return a - b

    def multiply(self, a, b):
        '''執行乘法'''

        return a * b

    def divide(self, a, b):
        '''執行除法'''

        # 分母不可為0
        if b == 0:
            return "Error: Division by zero"
        return a / b
    
    def get_user_input(self):
        '''輸入兩個數字'''

        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            return num1, num2
        
        except ValueError:
            print("Error: Invalid input, please enter numeric values") 
            return None, None
        
    def calculate(self):
        '''主要函式'''

        operation = input("Enter operation (+, -, *, /): ")
        if operation not in self.operations:
            print("Error: Invalid operation.")
            return
        
        num1, num2 = self.get_user_input()

        if num1 is None or num2 is None:
            return

        # call對應的運算式; e.g operations[symbol](function)
        result = self.operations[operation](num1, num2) 
        print(f"Result: {result}")

if __name__ == "__main__":
    calculator = Calculator()
    calculator.calculate()

    
