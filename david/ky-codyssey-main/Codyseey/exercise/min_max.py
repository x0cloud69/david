from flask import Flask

def main():
    str = input("Enter a string:")
    
    try:
        number_list = [float(i) for i in str.split()]
    except ValueError:
        print("Invalid Input")
        return
    
    min_value = number_list[0]
    max_value = number_list[0]

    for number in number_list:
        if number < min_value:
            min_value = number
        if number > max_value:
            max_value=number

    print(f"Min:", {min_value}, "Max:" ,{max_value})

    return 







if __name__ == "__main__":
    main()