def solution(command):
    
    current_direction = 'N'

    x = 0
    y = 0

    for i in range(len(command)):

        value = command[i]
        if value in ['R','L']:
            if current_direction == 'N':
                if value == 'R':
                    current_direction = 'E'
                if value == 'L':
                    current_direction = 'W'
            elif current_direction == 'S':
                if value == 'R':
                    current_direction = 'W'
                if value == 'L':
                    current_direction = 'E'
            elif current_direction == 'E':
                if value == 'R':
                    current_direction = 'S'
                if value == 'L':
                    current_direction = 'N'
            elif current_direction == 'W':
                if value == 'R':
                    current_direction = 'N'
                if value == 'L':
                    current_direction = 'S'
        
        if value == 'G':
            if current_direction == 'N':
                y = y + 1
            if current_direction == 'S':
                y = y -1
            if current_direction == 'E':
                x = x + 1 
            if current_direction == 'W':
                x = x - 1
        
        if value == 'B':
            if current_direction == 'N':
                y = y - 1
            if current_direction == 'S':
                y = y + 1
            if current_direction == 'E':
                x = x - 1 
            if current_direction == 'W':
                x = x + 1

   # answer.append([x,y])
    return [x,y]

print(solution('GRGLGRG'))
