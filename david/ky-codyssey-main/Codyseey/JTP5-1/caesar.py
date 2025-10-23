import os


current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir,"emergency_storage_key","password.txt")
write_path = os.path.join(current_dir,"result.txt")

password = []

dict_password = ['god','hello','key','love','nice','open','pack','rain','salt','stop','time','work']


with open(file_path, 'r') as file:
 password = list(file.read())
 print(password)


 result_value = []
 
 i = 0
 def caesar_cipher_decode(target_text):
   for i in range(26):
     i = i+1
     transfer_text = ''
     for char in target_text:
       result = ''
       if ord(char) >= 97 and ord(char) <= 122:
         jdx = ord(char)-i
         if jdx < 97:
           jdx = 123 - (97 - jdx)
         result = chr(jdx)
       elif ord(char) >= 65 and ord(char) <= 90: # 대문자
         jdx = ord(char)-i
         if jdx < 65:
            jdx = 91 - (65 - jdx)
         result = chr(jdx)
       else:
         result = char
       transfer_text = transfer_text + result    
     result_value.append(transfer_text) 
     print(f"shift : {i} result : {transfer_text}")

#    break    
#     #################################################
#     #  보너스스
#     #################################################
    
    #  if any(word in transfer_text for word in dict_password):
    #     print(f"shift : {i} result : {transfer_text}")
    #     # break    
   
    
  # num = int(input("몇번째 번호가 맞는지 입력하세요 : "))
  
#    with open(write_path,"w") as file:
#      file.write(result_value[num-1])
    

    
 if __name__ == "__main__":
   caesar_cipher_decode(password)
   num = int(input("몇번째 번호가 맞는지 입력하세요 : "))
  
   with open(write_path,"w") as file:
      file.write(result_value[num-1])  