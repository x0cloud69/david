def solution(ability):
  n = len(ability) # 학생 수
  m = len(ability[0]) # 과목수
  visited = [False] * n # 학생 방문 여부
  
  def recursive_dfs(depth, total, visited):
    if depth == m:
      return total
    max_score = 0
    for i in range(n):
      if not visited[i]:
        visited[i] = True
        print(f"Before: person : {i},depth: {depth}, ability: {ability[i][depth]}, total: {total}, visited: {visited}")
        score = recursive_dfs(depth+1, total+ability[i][depth], visited)
        max_score = max(max_score,score)
        print(f"After: person : {i}, depth: {depth}, ability: {ability[i][depth]}, total: {total},max_score: {max_score}, visited: {visited}")
        visited[i] = False
    return max_score

  return recursive_dfs(0,0,visited)
  
if __name__ == "__main__":
    ability = [[20, 10, 40], [30, 20, 50], [10, 40, 30]]
    print(solution(ability))
    