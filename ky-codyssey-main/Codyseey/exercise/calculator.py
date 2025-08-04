from flask import Flask

def plus(a,b):
    return a+b


def minus(a,b):
    return a-b

def multiply(a,b):
    return a*b

def divide(a,b):
    return a/b

def main():
    try:
        a = float(input("Enter first numbr:"))
    except ValueError:
        print("Invalid input")
        return
    try:
        b = float(input("Enter Second number:"))
        if b == 0:
            print("ZeroDivisionError")
            return 
    except ValueError:
        print("Invalid Numeber")
        return
    op=input("input operaor")
    if op not in ['+','-','*','/']:
        print("Invalid Operation")
        return
    
    if op == '+':
        result = plus(a,b)
    if op == '-':
        result = minus(a,b)
    if op == '*':
        result = multiply(a,b)
    if op == '/':
        result = divide(a,b)
    
    print("Result: ", result)

app = Flask(__name__)

if __name__ == "__main__":
    main()


