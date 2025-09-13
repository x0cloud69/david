def solution(input_list):
  answer = []
  #answer.append("RR")
  #answer.append("Rr")
  
  n = len(input_list)     # 요청 행수 
  
  for i in range(n):
    # a : n generation
    # b : position
    a,b = input_list[i]
    
    remain = b % 4  # 나머지
    mod    = b / 4  # 몫

    check_mod = 4 ** (a -2)

    print(f"몫 : {mod}, 나머지 : {remain}, 차수 : {a}, 위치 : {b}, check_mod : {check_mod}")

    if b <= check_mod :
      answer.append("RR")
    elif b > (a * check_mod):
      answer.append("rr")    
    else:
      if remain == 1:
        answer.append("RR")
      elif remain == 2 or remain == 3:
        answer.append("Rr")
      else:
        answer.append("rr")
    
  
  return answer


if __name__ == "__main__":
  input_list = [[2,3]]
  answer = solution(input_list)
  print(f"Answer : {answer}")

