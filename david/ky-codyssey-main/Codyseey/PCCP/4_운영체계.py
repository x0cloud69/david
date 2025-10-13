import heapq

def solution(program):
    """
    프로세스 스케줄링 시뮬레이션 함수
    
    Args:
        program: [점수, 호출시각, 실행시간]으로 구성된 2차원 리스트
    
    Returns:
        결과를 담은 리스트. answer[0] = 전체 종료 시각, answer[i] = 점수 i의 총 대기시간
    """
    
    # 1. 초기화
    answer = [0] * 11  # answer[0]은 총 실행 시간, answer[1~10]은 점수별 대기 시간
    total_programs = len(program)
    
    # 프로그램을 '호출 시각' 순으로 미리 정렬합니다. 시뮬레이션이 편리해집니다.
    # 호출 시각이 같다면 점수 순으로 정렬되도록 2차 기준을 추가할 수 있습니다.
    program.sort(key=lambda x: x[1])

    print(f"정렬된 프로그램 리스트: {program}")
    
    # 대기 큐(Priority Queue). (점수, 호출시각, 실행시간) 튜플을 저장합니다.
    # heapq는 튜플의 첫 번째 요소(점수)를 기준으로 최소 힙을 구성합니다.
    # 점수가 같으면 두 번째 요소(호출시각)를 기준으로 자동 정렬됩니다.
    waiting_queue = []
    print(f"초기 대기 큐: {waiting_queue}")
    
    currentTime = 0      # 현재 시각
    program_idx = 0      # 정렬된 program 리스트를 가리키는 인덱스
    executed_count = 0   # 실행 완료된 프로그램 수

    # 2. 메인 시뮬레이션 루프
    # 모든 프로그램이 실행 완료될 때까지 반복
    while executed_count < total_programs:
        
        # 현재 시각(currentTime)까지 호출된 모든 프로그램을 대기 큐에 추가
        while program_idx < total_programs and program[program_idx][1] <= currentTime:
            score, call_time, run_time = program[program_idx]
            heapq.heappush(waiting_queue, (score, call_time, run_time))
            program_idx += 1
            
        # [Case 1] 대기 큐에 실행할 프로그램이 있는 경우
        if waiting_queue:
            # 우선순위가 가장 높은 프로그램을 꺼냄 (점수가 가장 낮은 프로그램)
            score, call_time, run_time = heapq.heappop(waiting_queue)
            
            # 대기 시간 계산 및 결과 배열에 누적
            wait_time = currentTime - call_time
            answer[score] += wait_time
            
            # 현재 시각을 프로그램 종료 시각으로 업데이트
            currentTime += run_time
            
            # 실행 완료 카운트 증가
            executed_count += 1
            
        # [Case 2] 대기 큐는 비어있지만, 아직 도착할 프로그램이 남은 경우
        # (CPU가 쉬고 있는 상태)
        else:
            # 다음 프로그램이 도착하는 시각으로 시간을 점프시킴
            currentTime = program[program_idx][1]

    # 3. 최종 결과 정리
    # 모든 프로그램 실행이 끝난 후의 최종 시각을 answer[0]에 저장
    answer[0] = currentTime
    
    return answer


program1 = [[2, 0, 10], [1, 5, 5], [3, 5, 3]]
solution(program1)

# # --- 예제 테스트 ---
# program1 = [[2, 0, 10], [1, 5, 5], [3, 5, 3]]
# # 예상 결과: [23, 5, 0, 3, 0, 0, 0, 0, 0, 0, 0]
# print(f"예제 1 결과: {solution(program1)}")

# program2 = [[3, 6, 4], [4, 2, 5], [1, 0, 5], [5, 0, 5]]
# # 예상 결과: [19, 0, 0, 4, 3, 14, 0, 0, 0, 0, 0]
# print(f"예제 2 결과: {solution(program2)}")
