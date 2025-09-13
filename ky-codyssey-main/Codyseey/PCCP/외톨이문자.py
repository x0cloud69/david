def solution(input_str):
    alone_str = []
    passed_str = []

    for current_char in input_str:
        if (current_char in passed_str) and (current_char != passed_str[-1]):
            alone_str.append(current_char)
            passed_str.append(current_char) 
        else: 
            passed_str.append(current_char)

    alone_str = sorted(alone_str)
    a    = ''.join(set(alone_str))
    if result == '':
        result = 'N'
    print(result)


str = 'zbzbz'
solution(str)