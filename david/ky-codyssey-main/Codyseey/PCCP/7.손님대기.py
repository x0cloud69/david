import time

def solution(menu, order, k):
    answer = 0 # 매장내 손님 수

    que = menu.copy()
    waiting_que = []
    time_limit = len(order) * k
    time_process = 0
    convert_order = []
    
    for i in range(len(order)):
      if i == 0:
        convert_order.append(menu[order[i]])
      else:
        convert_order.append(convert_order[i-1] + menu[order[i]])
           
    print(convert_order)
    
    i = 0
    while time_process < time_limit:

      # 대기 큐에 손님 추가
            # pop 해서 손님 빼기
      if waiting_que:       
        if time_process >= waiting_que[0]:
          waiting_que.pop(0)
  
      waiting_que.append(convert_order[i])
      print(f"waiting_que(추가가): {waiting_que}")    

      answer = max(answer, len(waiting_que))
      print(f"대기인원 : {answer}")
       
      i += 1
      # 최대 대기 손님 저장

      print(f"time_process: {time_process}")
      time_process += k    
    return answer
  
print(solution([5], [0, 0, 0, 0, 0], 5))
  
