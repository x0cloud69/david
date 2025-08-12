def solution(input_string):
    prev_char = None
    keep_char = []
    input_string = "dffghefabbbacdeee"
    single_char = []
    for char in input_string:
        if char != prev_char:
             keep_char.append(char)
        prev_char = char
        # Store the single character
        if char in single_char or len(single_char) == 0:
            single_char.append(char)
        elif char in single_char:
            single_char.append(char)
if __name__ == "__main__":
    input_string = "dffghefabbbacdeee"
    solution(input_string)   
