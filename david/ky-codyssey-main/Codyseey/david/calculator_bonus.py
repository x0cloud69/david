""" ✅ 2. 계산기 프로그램 구현 (calculator.py)
david라는 디렉토리에 작업한다.
다음 요구사항에 맞는 파이썬 계산기 프로그램을 calculator.py라는 이름의 파일로 작성한다:

📌 기능 요구사항

사용자 입력 받기
수식 형태로 입력 (예: 2 + 3)
기본 연산 기능
함수 이름	동작 설명
add(a, b)	덧셈
subtract(a, b)	뺄셈 (a - b)
multiply(a, b)	곱셈
divide(a, b)	나눗셈 (a / b)
예외 처리
b == 0일 때 "Error: Division by zero." 출력
잘못된 연산자는 "Invalid operator." 출력
출력 형식
"Result: &lt;계산결과&gt;" """

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Error: Division by zero.")
    return a / b

def calculate(a, b, operator):
    if operator == '+':
        return add(a, b)
    elif operator == '-':
        return subtract(a, b)
    elif operator == '*':
        return multiply(a, b)
    elif operator == '/':
        return divide(a, b)
    else:
        raise ValueError("Invalid operator.")

def parse_expression(expression):
    # 수식 파싱 함수
    try:
        # 공백 제거
        expression = expression.replace(" ", "")
        
        # 연산자 찾기
        operators = ['+', '-', '*', '/']
       # found_ops = [op for op in operators if op in expression]

        # 연산자가 1개만 있어야 함
        op_count = sum(expression.count(op) for op in operators)
        if op_count != 1:
            raise ValueError("Invalid expression.")

        for op in operators:
            if op in expression:
                operator = op
                operator_index = expression.index(op)
                break

        a = int(expression[:operator_index])
        b = int(expression[operator_index + 1:])
        return a, b, operator

    except ValueError:







































        
        raise ValueError("Invalid expression.")

def main():
    try:
        expression = input("Enter expression: ")
        a, b, operator = parse_expression(expression)
        
        result = calculate(a, b, operator)
        print(f"Result: {result}")

    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()