alpha = 'abcdefghijklmnopqrstuvz'

import string
tmp = ['a'] * 6
index = 1
for i in range(6 - 1, -1, -1):
    index, r = divmod(index, len(alpha))
    tmp[i] = alpha[r]
    print(''.join(tmp))

chars = string.digits + string.ascii_lowercase + string.ascii_uppercase + string.punctuation
print(chars)
    
print("digits:", string.digits)           # 숫자 (0-9)
print("ascii_lowercase:", string.ascii_lowercase)   # 소문자 (a-z)
print("ascii_uppercase:", string.ascii_uppercase)   # 대문자 (A-Z)
print("ascii_letters:", string.ascii_letters)       # 모든 알파벳 (a-z, A-Z)
print("punctuation:", string.punctuation)          # 특수문자
print("whitespace:", string.whitespace)           # 공백 문자들
print("printable:", string.printable)             # 출력 가능한 모든 문자
print("Formatter",string.Formatter)


from string import Template

# 템플릿 사용 예시
template = Template('Hello, $name!')
result = template.substitute(name='Python')
print(result)  # 출력: Hello, Python!

print(dir(string))  # string 모듈의 모든 속성과 메서드 출력 

import os
import multiprocessing
from multiprocessing import cpu_count


num_processes = cpu_count()
print(f"Using {num_processes} CPU cores")