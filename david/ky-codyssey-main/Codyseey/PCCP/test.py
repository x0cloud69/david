def solution(menu, order, k):
    n = len(order)  # 총 손님 수
    
    # 각 손님의 도착 시간
    arrival_times = [i * k for i in range(n)]
    
    # 각 손님의 음료 제작 완료(퇴장) 시간 계산
    leave_times = []
    current_time = 0  # 현재 시간
    
    for i in range(n):
        # 손님 도착 시간과 현재 시간 중 더 늦은 시간부터 음료 제작 시작
        current_time = max(current_time, arrival_times[i])
        # 음료 제작 시간 추가
        current_time += menu[order[i]]
        # 퇴장 시간 저장
        leave_times.append(current_time)
    
    # 시간별 카페에 있는 손님 수 계산
    max_customers = 0
    for i in range(n):
        # i번째 손님이 도착했을 때 카페에 있는 손님 수 계산
        customers = 0
        for j in range(n):
            # j번째 손님이 i번째 손님 도착 시간에 카페에 있는지 확인
            if arrival_times[j] <= arrival_times[i] < leave_times[j]:
                customers += 1
        max_customers = max(max_customers, customers)
    
    return max_customers

print(solution([5,10,3], [0, 1, 2, 2, 0], 5))