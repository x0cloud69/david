"""  정렬 프로그램 작성 - **sort_calculator.py**
사용자가 터미널에서 공백으로 구분된 숫자들을 입력하면, 입력된 숫자들을 오름차순으로 정렬하여 출력하는 프로그램을 작성한다.

파이썬 계산기 기능 요구사항

📌 기능 요구사항
입력 형식
터미널에서 input()을 사용하여 숫자들을 공백으로 구분하여 입력받는다.
출력 형식
정렬된 숫자들을 오름차순으로 다음과 같은 형식으로 출력한다:

Sorted: <숫자1> <숫자2> <숫자3> ...

출력되는 숫자들은 반드시 소수점을 포함한 실수(float) 형태로 출력한다.

예외 처리
입력에 숫자가 아닌 값이 포함되었거나 입력이 비어 있는 경우 "Invalid input."을 출력한다.


★ 구현 방식 및 기술 요구사항  1
Python 내장 함수인 sorted() 와 리스트 메서드인 .sort() 사용을 금지한다. (자동 채점에서 확인됨)
반드시 직접 정렬 알고리즘을 구현해야 한다. (버블 정렬, 선택 정렬 등 자유롭게 구현 가능)
입력값은 반드시 터미널에서 input()을 사용하고, 공백으로 나누어 처리(split())한다.
숫자 변환은 반드시 float()로 처리한다.
프로그램은 다음의 형태로 작성하여 실행된다:

 """

""" def sort_numbers(numbers):
    # 입력된 숫자들을 오름차순으로 정렬 (선택 정렬 알고리즘 사용)
    n = len(numbers)
    for i in range(n):
        for j in range(0, n-i-1):
            if numbers[j] > numbers[j+1]:
                # Swap if the element found is greater than the next element
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
    return numbers """



def selection_sort_numbers(numbers):

    # 입력된 숫자들을 오름차순으로 선택 정렬
    n = len(numbers)
        
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if numbers[j] < numbers[min_idx]:
                min_idx = j
        numbers[i], numbers[min_idx] = numbers[min_idx], numbers[i]
    return numbers
        
def main():
    try:
        # 사용자로부터 입력 받기
        input_str = input("숫자를 입력 해주세요(공백으로 구분):")
        # 입력이 비어 있거나 숫자를 하나만 넣었을때
        if not input_str or len(input_str.strip()) < 2:
            print("Invalid input.")
            return
        # 입력된 문자열을 공백으로 분리하고 float로 변환
        numbers = [float(x) for x in input_str.split()]
        # 정렬 함수 호출
        sorted_numbers = selection_sort_numbers(numbers)
        # 결과 출력
        print("Sorted:", " ".join(map(str, sorted_numbers)))
    except ValueError:
        print("Invalid input.")

if __name__ == "__main__":
    main()
