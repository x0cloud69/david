from flask import Flask



def calculate_power(number, exponent):
    result = 1

    conv_exponent = abs(exponent)

    if number == 0 or exponent == 0:
        return 1
    
    for _ in range(conv_exponent):
        result = result * number
    
    if exponent > 0:
       print("Result : ", float(result))
    else:
       print("Result : ", float(1/result))
             
    return result

def main():
    number = input("Enter number: ")
    exp = input("Enter exponent : ")

    try:
        conv_number = float(number)
        conv_exp = int(exp)
        result = calculate_power(conv_number, conv_exp)
    except ValueError:
        print("Invalid Number")
        return
    return conv_number, conv_exp


    
if __name__ == "__main__":
    main()