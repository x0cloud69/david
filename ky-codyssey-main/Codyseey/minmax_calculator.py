""" 
✅ 2. 최소값 최대값 프로그램 구현하기 - **minmax_calculator.py**
입력된 숫자들 중 최소값(minimum) 과 최대값(maximum) 을 출력하는 프로그램을 작성한다.

파이썬 계산기 기능 요구사항
📌 기능 요구사항
입력 예시
3 9 1 4 2
입력된 숫자중 최대값 최소값 출력

예외 처리
숫자 이외의 값이 입력될 경우 "Invalid input."을 출력한다.
출력 예시
Min: 1.0, Max: 9.0

🧱 구현 방식 및 기술 요구사항
Python 내장 함수 min()과 max() 사용을 금지한다.
입력값 처리는 반드시 터미널에서 input()을 사용한다.
입력된 숫자는 공백으로 나누어 처리한다. (split() 활용)
숫자로 변환 시 float()를 사용한다.
반드시 다음과 같은 블록으로 실행한다.
if __name__ == "__main__":
    main()

개발환경
Git은 2.28.0 버전 이상을 사용한다. (해당 버전 이상부터 main 브랜치가 기본으로 설정 가능하다.)
기본 브랜치 이름을 main으로 변경 및 확인 방법
git config --global init.defaultBranch main

Git에서 기본 제공되는 명령어로 터미널에서 실행하며 별도의 GUI 도구를 사용하지 않는다. 
윈도우는 Windows Terminal에서 Git Bash로 작업한다. 맥과 리눅스는 OS에 포함된 Terminal을 사용한다.

제약사항
Git은 2.28.0 버전 이상을 사용한다. (해당 버전 이상부터 main 브랜치가 기본으로 설정 가능하다.)
Git에서 기본 제공되는 명령어로 터미널에서 실행하며 별도의 GUI 도구를 사용하지 않는다. 
윈도우는 Windows Terminal에서 Git Bash로 작업한다. 맥과 리눅스는 OS에 포함된 Terminal을 사용한다.


보너스 과제
버전 관리 시스템의 종류 3가지를 Markdown 문서로 제출한다.
.git 디렉토리의 역할의 의미를 Markdown 문서로 제출한다.
파일명은 git_directory.md로 저장한다.
작업 디렉토리에 .git디렉토리를 삭제한 후 git의 상태를 확인한다. 휴지통에서 .git디렉토리를 복원한 후 git의 상태를 확인한다.
"""

def find_min_max(numbers):
    if not numbers: # 빈 리스트 체크
        return None, None  # 반환값이 2개로 설정되어 있으므로 None 반환
    
    min_val = numbers[0]  # 첫 번째 숫자를 최소값으로 초기화
    max_val = numbers[0]  # 첫 번째 숫자를 최대값으로 초기화
    
    for num in numbers:
        if num < min_val:  # 현재 숫자가 최소값보다 작으면
            min_val = num
        if num > max_val:  # 현재 숫자가 최대값보다 크면
            max_val = num
            
    return min_val, max_val

def main():
    try:
        input_str = input("숫자를 입력 해주세요 : ") # 입력받기
        numbers = [float(x) for x in (input_str.split())] # 입력된 문자열을 공백으로 분리하고 float로 변환
        min_val, max_val = find_min_max(numbers) # 최소값과 최대값 찾기
        print(f"Min: {min_val}, Max: {max_val}") # 결과 출력

    except ValueError:
        print("Invalid input.")

if __name__ == "__main__":
    main()



