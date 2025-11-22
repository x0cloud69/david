def solution(bandage, health, attacks):
    t, x, y = bandage  # 시전 시간, 초당 회복량, 추가 회복량
    max_health = health  # 최대 체력
    last_attack_time = attacks[-1][0]  # 마지막 공격 시간
    
    # 공격 시간을 키로 하는 딕셔너리 생성
    # attack_dict = {time: damage for time, damage in attacks}
    attack_dict = dict(attacks)
    print(attack_dict)
    
    current_health = health  # 현재 체력
    consecutive_time = 0  # 연속 시전 시간
    
    # 시간에 따른 시뮬레이션
    for current_time in range(1, last_attack_time + 1):
        # 공격 받는 경우
        if current_time in attack_dict:
            current_health -= attack_dict[current_time]
            consecutive_time = 0  # 연속 시전 초기화
            
            # 사망 체크
            if current_health <= 0:
                return -1
        # 공격 받지 않는 경우
        else:
            consecutive_time += 1  # 연속 시전 시간 증가
            current_health += x  # 초당 회복량
            
            # 연속 시전 성공 시 추가 회복
            if consecutive_time == t:
                current_health += y
                consecutive_time = 0
            
            # 최대 체력 초과 방지
            current_health = min(current_health, max_health)
    
    return current_health

print(solution([3, 100, 300], 100, [[2, 30], [4, 50], [5, 20], [9, 10]]))