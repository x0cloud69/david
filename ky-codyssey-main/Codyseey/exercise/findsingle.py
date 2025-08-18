#############################################
# 변수 정의
#############################################
# input_string = 입력된 문자열
# prev_char = 이전 문자 배열
# cur_char  = 현재 문자
# single_char = 단독 문자 리스트
#############################################

#############################################
# Psuedo Code
#############################################
# 1. 입력된 문자열의 첫번째 문자를 prev_char[0]에 저장
# 2. 입력된 문자열을 순회하면서 prev_char의 마지막 문자와 현재문자를 비교 한다.
# 3. prev_char의 마지막 문자와 cur_char가 같으면 continue
# 4. prev_char의 마지막 문자와 cur_char가 다르면 prev_char에 cur_char를 추가한다.
# 5. prev_char의 배열값 중에 cur_char가 있는지 확인한다.
#    5-1. 있으면 single_char에 cur_char를 추가한다.
#    5-2. 없으면 single_char에 cur_char를 추가하지 않는다.
#############################################
def solution(input_string):
    prev_char = []
    input_string = "zbzbz"
    single_char = []
    for char in input_string:
        if prev_char and char == prev_char[-1]:
             continue
        else:
             if char in prev_char and char not in single_char:
                 single_char.append(char)
             prev_char.append(char)
    answer = ''.join(sorted(single_char))
    if not answer:
         answer = "N"
    return answer



if __name__ == "__main__":
      print("Result : ", solution("input_string"))