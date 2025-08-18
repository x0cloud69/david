def solution(queries):
    def get_genotype(depth, position):
        # 첫 번째 세대는 항상 Rr
        if depth == 1:
            return "Rr"
        
        # 부모의 위치 계산
        parent_position = (position - 1) // 4 + 1
        parent_genotype = get_genotype(depth - 1, parent_position)
        
        # 부모가 순종(RR 또는 rr)이면 자식도 같은 유전자형
        if parent_genotype == "RR":
            return "RR"
        if parent_genotype == "rr":
            return "rr"
        
        # 부모가 Rr인 경우
        child_position = (position - 1) % 4
        if child_position == 0:
            return "RR"
        elif child_position == 1 or child_position == 2:
            return "Rr"
        else:  # child_position == 3
            return "rr"

    return [get_genotype(depth, position) for depth, position in queries]

# 테스트
if __name__ == "__main__":
    test_cases = [
        [[1,1]],     # 예상 결과: ["Rr"]
        [[2,1]],     # 예상 결과: ["RR"]
        [[2,2]],     # 예상 결과: ["Rr"]
        [[2,3]],     # 예상 결과: ["Rr"]
        [[2,4]],     # 예상 결과: ["rr"]
        [[3,1]],     # 예상 결과: ["RR"]
        [[3,4]],     # 예상 결과: ["RR"]
        [[3,5]],     # 예상 결과: ["RR"]
        [[3,8]],     # 예상 결과: ["RR"]
        [[3,9]],     # 예상 결과: ["Rr"]
    ]

    
    for test in test_cases:
        print(f"Input: {test}")
        print(f"Output: {solution(test)}\n")
