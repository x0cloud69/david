import heapq

def solution(ability,number):
    answer = 0

    heapq.heapify(ability)
    for i in range(number):
        min_data = heapq.heappop(ability)
        min_data2 = heapq.heappop(ability)
        sum_data = min_data + min_data2
        heapq.heappush(ability,sum_data)
        heapq.heappush(ability,sum_data)
    return sum(ability)
   

print(solution([10,3,7,2],2))
