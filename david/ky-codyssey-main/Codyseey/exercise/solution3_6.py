CIPHER_TEXT = 'erkekr, DDrker ereei Qic efkef'

def seasor(text):
    result  = []
    try:
      for i in range(26):
         temp_result = ""
         for str in text:
              
             if str.isalpha():
                if str.isupper():
                    temp_str = str 
                else:
                     temp_str = chr(((ord(str)-ord('a') - i ) % 26 ) + ord('a'))
             else:
                temp_str = str
             temp_result += temp_str
         result.append(temp_result)
      return result
    except Exception:
         raise
def main():
  try:
   result = seasor(CIPHER_TEXT)
  #  print(result)
   for i,str in enumerate(result):
       print(i,str)
  except Exception:
    print("Processing Error")
    return
if __name__ == '__main__':
    main()
