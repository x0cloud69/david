def caeser(text,shift,mode='encryption'):

  try:
    if mode == 'decryption':
      shift = -shift

    result_text = ""
    for char in text:
        if char.isalpha():
          if char.isupper():
              temp_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
          else:
              temp_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
              temp_char = char
      
        result_text += temp_char
    return result_text
  except Exception:
      raise

def main():
    try:
      text = input("암호화 하고자 하는 문자열을 입력하세요 : ").strip()
      mode_num = input("암호화 / 복호화 여부를 선택하세요 [1,2] : ").strip()
      if mode_num not in ['1','2']:
        raise ValueError
      
      mode = 'encryption'
      if mode_num == '2':
         mode = 'decryption'      
      shift_str = input("Shift 할 숫자를 입력 하세요 : ").strip()
      
      if shift_str.isdigit():
        shift = int(shift_str)
      else:
        raise ValueError
      
      result_text = caeser(text,shift,mode)
      print(result_text)
    except ValueError:
      print("Input Error 입니다")
      return
    except Exception:
      print("Processing Error")
      return 


if __name__ == ('__main__'):
  main()

                       
         