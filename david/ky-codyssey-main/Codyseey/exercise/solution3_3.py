# CIPHER_TEXT = 'erkekr, DDrker ereeiic efkef'

def caesar_cipher_decode(target_text: str) -> list[str]:
   """
   주어진 문자열에 대해 26가지 모든 카이사르 암호 시프트 결과를 반환합니다.
   """
   result = []  # list() 대신 [] 사용
   for shift in range(26):
       temp_str = ''
       for char in target_text:
           if char.isalpha():
               # isupper()로 대문자/소문자 구분
               start_code = ord('A') if char.isupper() else ord('a')
               temp_char = chr(((ord(char) - start_code + shift) % 26) + start_code)
           else:
               # 알파벳이 아니면 그대로 유지
               temp_char = char
           temp_str += temp_char
       result.append(temp_str)
   return result  # 불필요한 괄호 제거

def main():
     CIPHER_TEXT = 'erkekr, DDrker ereeiic efkef'
     
     try:
      # 1. 복호화 결과 리스트 받기
      decoded_results = caesar_cipher_decode(CIPHER_TEXT)

      # 2. 결과 리스트를 화면에 출력 (출력 로직을 main으로 이동)
      print("--- 가능한 복호화 결과 ---")
      for i, text in enumerate(decoded_results):
          print(f"{i + 1:2d}: {text}") # enumerate와 f-string으로 깔끔하게 출력
      print("--------------------------")

      # 3. 사용자 입력 받기
      num_input = int(input("몇 번째 문자열을 선택하시겠습니까? : "))
      
      # 4. 입력 값 유효성 검사
      if not (1 <= num_input <= 26):
        # 좀 더 명확한 에러 메시지를 위해 ValueError를 직접 발생
        raise ValueError("1부터 26 사이의 숫자를 입력해야 합니다.")
      
      # 5. 선택된 결과 출력 (중복 int() 변환 제거)
      print("\n>> 선택된 결과:")
      print(decoded_results[num_input - 1])

     except ValueError as e:
       # 발생한 에러 메시지를 함께 출력해주면 더 좋습니다.
       print(f"입력 오류: {e}")
       return
     except Exception as e:
      # 예상치 못한 다른 모든 에러 처리
      print(f"처리 중 오류가 발생했습니다: {e}")

if __name__ == '__main__': # 불필요한 괄호 제거
     main()
