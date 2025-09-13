min_age = 10
max_age = 60

min_money = 100000
max_money = 1000000

complete = 1
incomplete = 0

age = input("Input your age: ")
# 나이 입력값 검증
def check_age(age):
    if age.strip().isdigit() == False:
        return "Invalid input"
    if not (min_age <= int(age) <= max_age):
        return "Out of Age"
    return int(age)

money = input("Input your moneny: ")
# 지원 금액 입력값 검증
def check_money(money):
    if money.strip().isdigit() == False:
        return "Invalid Money"
    if not (min_money <= int(money) <= max_money):
        return "Out of Money"
    if int(money) % 100 != 0:
        return "Money must be multiple of 100"
    return int(money)

#수료 여부 검증
complete = input("Input your Complete Status (0 for Incomplete, 1 for Complete): ")

def check_complete(complete):
    if complete.strip().isdigit() == False:
        return "Invalid input"
    if int(complete) not in [0,1]:
        return "invalid wrong values"
    return int(complete)

support = 0

def calculate_support(age, money, complete):
    check_age_result = check_age(age)
    check_money_result = check_money(money)
    check_complete_result = check_complete(complete)

    if type(check_age_result) == str:
        return check_age_result
    if type(check_money_result) == str:
        return check_money_result
    if type(check_complete_result) == str:   
        return check_complete_result
    
    if 20 <= int(check_age_result) <=29:
        support_money = check_money_result * 0.9
    elif 30 <= int(check_age_result) <= 39:
        support_money = check_money_result * 0.7
    else:
        support_money = check_money_result

    if check_complete_result == 1:
        return support_money
    else:
        return 0
    

support_money = calculate_support(age, money, complete)
print("The support Amount is : " , support_money)
 

