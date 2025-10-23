# CIPHER_TEXT = 'erkekr, DDrker ereeiic efkef'
def ceaser(target_text:str)-> list[str]:
   result         = []
   try:
     for i in range(26):
       result_temp = ""
       for char in target_text:
           if char.isalpha():
             if char.isupper():
                temp_chr = chr((ord(char) - ord('A') + i ) % 26 + ord('A'))
             else:
                temp_chr = chr((ord(char) - ord('a') + i) % 26 + ord('a'))
           else:
                temp_chr = char
           result_temp += temp_chr
       result.append(result_temp)
     return result
   except Exception:
       raise

def main():
   CIPHER_TEXT = 'erkekr, DDrker ereeiic efkef'
   try:
      result = ceaser(CIPHER_TEXT)
      for i,text in enumerate(result):
       print(i+1,text)
      input_num = int(input("Selete the number : ").strip())
      if input_num < 1 or input_num > 26:
         raise ValueError
      else:
         print(result[input_num-1])
 
      
   except ValueError:
       print("Input Numer Error. ")
       return
   except Exception as e:
       print(e)
       return 

if __name__== "__main__":
  main()