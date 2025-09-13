"""  2. 제곱 계산 프로그램 구현하기 - power_calculator.py
Python을 사용하여 제곱 계산 프로그램을 구현한다.

Python 파일명: power_calculator.py

구현 요구사항:

사용자로부터 숫자와 제곱할 횟수(지수)를 입력받음
입력받은 숫자를 지정한 횟수만큼 거듭제곱한 결과 출력
Python의 내장 연산자 ** 또는 pow() 함수 사용 금지
반복문을 사용하여 직접 제곱 계산 구현
숫자는 float(), 지수는 int()로 형변환
사용자 입력 예시:

Enter number: 3
Enter exponent: 4
출력 형식:

Result: 81
예외 처리:

숫자 입력이 숫자형이 아닐 경우 "Invalid number input." 출력
지수 입력이 정수가 아닐 경우 "Invalid exponent input." 출력
테스트 방식:

Visual Studio Code에서 power_calculator.py 파일을 열고 터미널에서 python power_calculator.py 명령어로 실행한다.
프로그램의 실행 로직: """

def calculate_power(base, exponent):
  if base == 0:
     print("0은 음수 지수를 가질 수 없습니다.")
     return None
  #거급제곱 계산을 위한 함수
  result = 1
  
  if exponent >= 0:
    for _ in range(exponent):
      result = result * base
  else:
    for _ in range(-exponent):
      result = result * base
    result = 1 / result
  
  return result

def main():
  #숫자(base)와 지수(exponent) 입력 및 예외처리
  try:
    base = float(input("Enter number: "))
  except ValueError:
    print("Invalid number input.")
    return

  #지수 (exponent) 입력 및 예외처리
  try:
    exponent = int(input("Enter exponent: "))
  except ValueError:
    print("Invalid exponent input.")
    return

  # 결과 계산 및 출력
  result = calculate_power(base,exponent)
  print(f"Result: {result}")

if __name__ == "__main__":
  main()
  