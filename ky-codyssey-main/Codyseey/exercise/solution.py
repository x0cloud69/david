input_values = input("Input the number of Lines: ")

def check_input(input_values):
    if input_values.strip().isdigit() == False:
        return "Invalid input."
    if not (3 <= int(input_values) <=30):
        return "Out of range"
    return int(input_values)

def cal_line(n):
    answer = 0
    if type(n) == str:
        return n
    answer = n * (n - 3) /2
    return answer



result = check_input(input_values)
print("Answer:", cal_line(result))
