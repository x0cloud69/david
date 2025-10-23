CIPHER_TEXT = 'erkekr, DDrker ereei Qic efkef' # 변경 1. 전역 상수 설정

def caesar_cipher_decode(target_text: str) -> list[str]: # 변경 2. 문제에서 제공되는 함수 그대로 사용
   try:
     if target_text == '':
        raise ValueError
     result = []
     for i in range(26):
         result_temp = ""
         for char in target_text:
             if char.isalpha():
                if char.isupper():
                   temp_char= char
                else:
                   temp_char = chr((ord(char) - ord('a') - i ) % 26 + ord('a'))
             else:
                 temp_char = char
             result_temp += temp_char
         result.append(result_temp)
     return result
   except ValueError:
        raise
   except Exception:
        raise

def main():
   try:
      result =caesar_cipher_decode(CIPHER_TEXT)
      for i, _str_ in enumerate(result):
        print(f"{i}: {_str_}")
      s_input = input()
      if s_input == '':
         raise ValueError
      s_num = int(s_input)
      if not (0<=s_num<=25):
        raise ValueError
      print(f"Result: {result[s_num]}")
   except ValueError:
        print("Input Error")
        return
   except Exception:
        print("Processing Error")
        return

if __name__ == '__main__':
   main()