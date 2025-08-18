def solution(ability):
    n = len(ability) # 학생 수
    m = len(ability[0]) # 과목 수
    visited = [False] * n # 학생 방문 여부

    def dfs(depth, total, visited):
        print(f"Depth: {depth}, Total: {total}, Visited: {visited}")  # 디버깅용
        
        if depth == m:
            return total
        
        max_score = 0

        for i in range(n):
            if not visited[i]:
                visited[i] = True
                score = dfs(depth+1, total+ability[i][depth], visited)
                max_score = max(max_score, score)
                visited[i] = False
                print(f"At depth {depth}, student {i}, score: {score}")  # 디버깅용
        
        return max_score
    
    # 이 줄에 breakpoint 설정
    return dfs(0, 0, visited)
if __name__ == "__main__":
    ability = [[20, 10, 40], [30, 20, 50], [10, 40, 30]]
    print(solution(ability))