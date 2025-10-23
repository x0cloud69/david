# CIPHER_TEXT = 'erkekr, DDrker ereeiic efkef'

def ceaser(target_text:str) -> list[str]:
     # 1~26 번까지 반복 char(암호화 문자 변수), result (암호화 문자열 리스트)
    result = []
    try:
      for i in range(26):
          result_temp = ""
          for char in target_text:
               if char.isalpha():
                  if char.isupper():
                     temp_char = chr((ord(char) - ord('A') + i) % 26 + ord('A'))
                  else:
                     temp_char = chr((ord(char) - ord('a') + i) % 26 + ord('a'))
               else:
                  temp_char= char
               result_temp += temp_char
          result.append(result_temp)
      return result
    except Exception:
            raise

def main():
   CIPHER_TEXT = 'erkekr, DDrker ereeiic efkef'
   try:
     result = ceaser(CIPHER_TEXT)
     for i,str in enumerate(result):
         print(i+1,str)
     input_num = input("암호화 해제를 위한 번호 입력 : ").strip()
     input_num = int(input_num)
     if input_num <=0 or input_num>26:
        raise ValueError
     print(input_num,result[input_num-1])
   except ValueError:
      print("Input Error : ")
      return 
   except Exception:
     print("Process Error : ")
     return

if __name__ == '__main__':
   main()