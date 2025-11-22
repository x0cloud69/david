"""
Python 코드로 스택(Stack) 구조를 완성한다.
스택 구조에 내용을 입력할 수 있도록 추가하는 함수를 push() 함수를 만든다.
push() 함수는 10개가 다 채워지면 추가되지 않고 경고 메시지만 알려준다.
가장 마지막에 추가된 내용을 가져올 수 있게 pop() 함수를 만든다.
pop() 함수의 경우 가져올 내용이 없으면 가져오지 않고 경고 메시지만 알려준다.
전체 내용이 비였는지 확인하는 empty() 함수를 추가한다.
마지막 내용을 삭제하지 않고 내용만 확인하는 peek() 함수를 추가한다.
스택 구조가 완성되면 내용을 입력하고 가져와 본다. 단 이때 내용에는 고유한 번호등을 붙여서 스택의 구조가 정상적으로 잘 동작하는지 확인해야 한다.
"""

stack = []
def push(data):
    global stack
    if len(stack) >= 10:
        raise ValueError
    stack.append(data)
    return 

def empty():
    _answer_ = 'False'
    if len(stack) == 0:
        _answer_ = 'True'
    return _answer_


def pop():
    global stack
    _answer_ = empty()
    if _answer_ == 'False':
        _result_ = stack[-1]      
        del stack[-1]
    else:
        raise ValueError  
    return _result_

def peek():
    global stack
    if len(stack) == 0:
        raise ValueError
    _last_ = stack[-1]
    return _last_ 
    


def menu():
    print("=====================")
    print("1. Stack Data 입력   ")
    print("2. Stack Data 추출   ")
    print("3. Stack Peek        ")
    print("0. 종료              ")
    print("=====================")    
def main():
    _index_ = 0
    while True:
        menu()
        _num_ = input("처리 하고자 하는 작업을 선택 하세요. ")
        if _num_ == '1':
            _str_ = input("Data 를 입력하세요 : ")
            try:
                push(_str_)
                print(f"Index : {_index_} ,  Data : {stack}")
                _index_ += 1
            except ValueError:
                print("Stack 이 Full 입니다")
        elif _num_ == '2':
            try:
                _answer_ = pop()
                print(_answer_)
            except ValueError:
                print("Stack 이 Empty 입니다다")
        elif _num_ == '3':
            try:
                _answer_ = peek()
                print(_answer_)
            except ValueError:
                print("Stack 이 Empty 입니다다.")
        if _num_ == '0':
            return
            
                
if __name__ == '__main__':
    main()



    