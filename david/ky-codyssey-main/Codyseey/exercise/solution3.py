CIPHER_TEXT = 'erkekr, DDrker ereei Qic efkef' # 변경 1. 전역 상수 설정

def caesar_cipher_decode(target_text: str) -> list[str]: # 변경 2. 문제에서 제공되는 함수 그대로 사용
    if target_text == '': # 변경 3. 빈 칸(상수 값 없음)에 대한 raise ValueError 처리
        raise ValueError

    result  = []

    try:
        for i in range(26):
            temp_result = ""
            for char in target_text: # 변경 4. 변수명 str은 파이썬 기본 타입과 겹치므로 char로 변경)
                if char.isalpha(): #if !,
                    if char.isupper():
                        temp_str = char  # [변경 4]에 해당 -> 변수명 변경
                    else:
                        temp_str = chr(((ord(char)-ord('a') - i ) % 26 ) + ord('a'))
                else:
                    temp_str = char
                temp_result += temp_str
            result.append(temp_result)
        return result
    except Exception:
         raise
    
def main():
    try:
        result = caesar_cipher_decode(CIPHER_TEXT) # [변경 3]에 해당 -> 함수/인자명
    
        for i, r_str in enumerate(result): #변수 이름이 내장 자료형 str과 혼동
            print(f"{i}: {r_str}")         # ㄴ 'str'로 타 변수값 변환 시 object 혼동으로 TypeError가 발생할 수 있음. 

        s = input() # 변경 5. input() 시 [ '' ] 처리 
        if s == '':
            raise ValueError

        int_s = int(s) # 변경 6. input() 값 [ int ] 처리 및 범위 설정
        if not 0 <= int_s <= 25: #<< 0~25 
            raise ValueError
        
        print(f'Result: {result[int_s]}')

    except ValueError:
        print('Invalid input.')
        return
    
    except Exception:
        print("Processing error")
        return
    
if __name__ == '__main__':
    main()