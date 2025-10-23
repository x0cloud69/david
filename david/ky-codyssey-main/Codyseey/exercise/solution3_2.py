# CIPHER_TEXT = 'erkekr, DDrker ereeiic efkef'

def caesar_cipher_decode(target_text: str) -> list[str]:
   result = list()
   for shift in range(26):
       temp_str = ''
       for char in target_text:
           try:
              if char.isalpha():
                 if char.isupper():
                    temp_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
                 else:
                    temp_char = chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
              else:
                 temp_char = char
              temp_str += temp_char
             
           except Exception:
                   raise  
       result.append(temp_str)  
       print(shift+1,temp_str)
   return (result)

def main():
     CIPHER_TEXT = 'erkekr, DDrker ereeiic efkef'
     try: 
      result =caesar_cipher_decode(CIPHER_TEXT)
      num_input = int(input("몇번째 문자열을 출력하고 싶습니까? : "))
      if 1 > num_input or num_input > 26:
        raise ValueError
      print(result[int(num_input)-1])
     except ValueError:
       print('Error Input...')
       return    
     except Exception:
      print("Processing Error...")
if __name__ ==('__main__'):
     main()
