def solution(queries):
    answer = []
    n = len(queries)

    for i in range(n):
        depth, position = queries[i]
        mod = position / 4             # 몫
        check_remain = position % 4    # 나머지
        check_mod = 4 ** (depth -2)      # 몫
    
        if depth == 1:  # 첫 번째 세대는 항상 Rr
            answer.append("Rr")
        else:  
            if position <= check_mod:
                answer.append("RR")
            elif position > (4 * check_mod):
                answer.append("rr")
            else:
                if check_remain == 2 or check_remain == 3:
                    answer.append("Rr")
                elif check_remain == 1:
                    answer.append("RR")
                else:
                    answer.append("rr")

    return answer

if __name__ == "__main__":
  input_list = [[1,1], [2,7], [2,3], [2,4], [3,1], [3,4], [3,5],[3,8], [3,9]]
  answer = solution(input_list)
  print(f"Answer : {answer}")

""" 
   [[2,1]], # ["RR"]
        [[2,2]], # ["Rr"]
        [[2,3]], # ["Rr"]
        [[2,4]], # ["rr"]
        [[3,1]], # ["RR"]
        [[3,8]], # ["RR"] 
        
        
          [[1,1]],     # 예상 결과: ["Rr"]
        [[2,1]],     # 예상 결과: ["RR"]
        [[2,2]],     # 예상 결과: ["Rr"]
        [[2,3]],     # 예상 결과: ["Rr"]
        [[2,4]],     # 예상 결과: ["rr"]
        [[3,1]],     # 예상 결과: ["RR"]
        [[3,4]],     # 예상 결과: ["RR"]
        [[3,5]],     # 예상 결과: ["RR"]
        [[3,8]],     # 예상 결과: ["RR"]
        [[3,9]],     # 예상 결과: ["Rr"]"""