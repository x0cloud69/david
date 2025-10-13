def solution(ability, number):
    answer = 0

    ability.sort()

    for i in range(number):
        sum_data = ability[0] + ability[1]
        ability[0] = sum_data
        ability[1] = sum_data
        ability.sort()

        answer = sum(ability)

    return answer

print(solution([10,3,7,2], 2))



##### 테스트 케이스

# ability = [10,3,7,2]
# print(f"Original Data : {ability}")
# ability.sort()
# print(f"Sorted Data : {ability}")

# sum_data = ability[0]+ability[1]
# ability[0] = sum_data 
# ability[1] = sum_data

# # 배열의 sum 값
# total = sum(ability)
# print(f"Sum of all abilities : {total}")

# print(f"Swapped Data : {ability}")

