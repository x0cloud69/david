import sys
import os
import math
import random
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QStyle
from PyQt6.QtCore import Qt


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
            # 윈도우 플래그 설정
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowSystemMenuHint |
            Qt.WindowType.WindowMinMaxButtonsHint |
            Qt.WindowType.WindowCloseButtonHint
        )
        
        # 윈도우가 항상 최상위에 표시되도록 설정
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        # UI 파일 로드
        ui_file = os.path.join(os.path.dirname(__file__), 'engineering.ui')
        uic.loadUi(ui_file, self)

        # 계산기 상태 변수
        self.current_number = "0"
        self.previous_number = None
        self.operator = None
        self.waiting_for_operand = False
        self.display_text = "0"
        self.formula = ""  # 공식식
        self.angle_mode = "DEG"  # 각도 모드 (DEG/RAD)
        self.memory = 0  # 메모리 값

        # 버튼 이벤트 연결
        self.connect_buttons()
    
    def connect_buttons(self):
        # 숫자 버튼 (0-9)
        number_buttons = [self.btn_0, self.btn_1, self.btn_2, self.btn_3, self.btn_4,
                         self.btn_5, self.btn_6, self.btn_7, self.btn_8, self.btn_9]
        
        for i, button in enumerate(number_buttons):
            button.clicked.connect(lambda checked, num=str(i): self.number_clicked(num))
        
        # 연산자 버튼
        self.btn_plus.clicked.connect(self.add)
        self.btn_minus.clicked.connect(self.subtract)
        self.btn_mul.clicked.connect(self.multiply)
        self.btn_divid.clicked.connect(self.divide)
        self.btn_sign.clicked.connect(self.sign)
     #   self.test_1.clicked.connect(self.test_1_clicked)
     
        # 기타 버튼
        self.btn_result.clicked.connect(self.equal)
        self.btn_point.clicked.connect(self.decimal_clicked)
        self.btn_cls.clicked.connect(self.reset)
        self.btn_ratio.clicked.connect(self.percent)
        self.btn_par.clicked.connect(self.par)
        self.btn_backspace.clicked.connect(self.backspace)
        
        # 공학용 함수 버튼들
        self.btn_sin.clicked.connect(self.sin_function)
        self.btn_cos.clicked.connect(self.cos_function)
        self.btn_tan.clicked.connect(self.tan_function)
        self.btn_asin.clicked.connect(self.asin_function)
        self.btn_acos.clicked.connect(self.acos_function)
        self.btn_atan.clicked.connect(self.atan_function)
        self.btn_log.clicked.connect(self.log_function)
        self.btn_ln.clicked.connect(self.ln_function)
        self.btn_sqrt.clicked.connect(self.sqrt_function)
        self.btn_pow.clicked.connect(self.pow_function)
        self.btn_square.clicked.connect(self.square_function)
        self.btn_cube.clicked.connect(self.cube_function)
        self.btn_pi.clicked.connect(self.pi_function)
        self.btn_e.clicked.connect(self.e_function)
        self.btn_fact.clicked.connect(self.factorial_function)
        self.btn_abs.clicked.connect(self.abs_function)
        self.btn_ceil.clicked.connect(self.ceil_function)
        self.btn_floor.clicked.connect(self.floor_function)
        self.btn_1_over_x.clicked.connect(self.one_over_x_function)
        self.btn_10_pow.clicked.connect(self.ten_pow_function)
        self.btn_e_pow.clicked.connect(self.e_pow_function)
        self.btn_2_pow.clicked.connect(self.two_pow_function)
        
        # 추가 공학용 함수들
        self.btn_sinh.clicked.connect(self.sinh_function)
        self.btn_cosh.clicked.connect(self.cosh_function)
        self.btn_tanh.clicked.connect(self.tanh_function)
        self.btn_angle_mode.clicked.connect(self.toggle_angle_mode)
        self.btn_random.clicked.connect(self.random_function)
        self.btn_mod.clicked.connect(self.mod_function)
        
        # 메모리 기능들
        self.btn_mc.clicked.connect(self.memory_clear)
        self.btn_mr.clicked.connect(self.memory_recall)
        self.btn_ms.clicked.connect(self.memory_store)
        self.btn_m_plus.clicked.connect(self.memory_add)
        self.btn_m_minus.clicked.connect(self.memory_subtract)
        self.btn_clear_entry.clicked.connect(self.clear_entry)
        
        # 초기 디스플레이 업데이트
        self.update_display()
        
 #   def test_1_clicked(self):
    def sign(self):
       # self.formula += '-'
        """양수/음수 변환"""
        if not self.formula:
            # 수식이 비어있으면 - 입력
            self.formula = '-'
           # self.current_number = '-'
        elif self.formula[-1] in '+-*/(':
            # 연산자나 괄호 뒤에 - 입력
            self.formula += '-'
           # self.current_number = '-'
        elif self.formula.endswith(')'):
            # 괄호로 끝나는 경우: (숫자) -> -(숫자) 또는 -(숫자) -> (숫자)
            if self.formula.startswith('-('):
                # -(숫자) -> (숫자)
                self.formula = self.formula[2:]
               # self.current_number = self.formula
            else:
                # (숫자) -> -(숫자)
                self.formula = '-' + self.formula
               # self.current_number = '-' + self.current_number
        else:
            # 현재 숫자의 부호 변경
            if self.current_number.startswith('-'):
                # 음수 -> 양수
                self.current_number = self.current_number[1:]
                # formula에서 마지막 음수 숫자를 양수로 변경
                import re
                pattern = r'-\d+(\.\d+)?$'
                self.formula = re.sub(pattern, self.current_number, self.formula)
            else:
                # 양수 -> 음수
                self.current_number = '-' + self.current_number
                # formula에서 마지막 양수 숫자를 음수로 변경
                import re
                pattern = r'\d+(\.\d+)?$'
                self.formula = re.sub(pattern, self.current_number, self.formula)
        self.update_display()
      #  print(f"화면 업데이트 완료")
        
    def add(self):
        self.formula += '+'
        self.update_display()
    def subtract(self):
       self.formula += '-'
       self.update_display()
    def multiply(self):
         self.formula += '*'
         self.update_display()
    def divide(self):
         self.formula += '/'
         self.update_display()
    def backspace(self):
        """뒤에서 한 글자씩 지우기"""
        if len(self.formula) > 0:
            self.formula = self.formula[:-1]
            self.update_display()
    def par(self):
        # 괄호 쌍 맞추기: ( 개수와 ) 개수 확인
        open_count = self.formula.count('(')
        close_count = self.formula.count(')')
        
        if open_count > close_count:
            # 열린 괄호가 더 많으면 닫는 괄호 추가
            self.formula += ')'
        else:
            # 그렇지 않으면 여는 괄호 추가
            self.formula += '('
        
        self.update_display()

    def number_clicked(self, number):
        """숫자 키를 누를 때마다 화면에 숫자가 누적"""
        if self.waiting_for_operand or self.current_number == "0":
            self.current_number = number
            self.waiting_for_operand = False
        else:
            self.current_number += number
            
        self.formula += number
        
        self.update_display()

    def decimal_clicked(self):
        """소수점 키를 누르면 소수점이 입력 (이미 소수점이 있으면 추가 입력 안됨)"""
        if self.waiting_for_operand:
            self.current_number = "0."
            self.waiting_for_operand = False
        elif "." not in self.current_number:
            self.current_number += "."
            self.formula += "."
        
        self.update_display()



    def equal(self):
        """결과를 출력하는 equal() 메소드"""
        try:
            # 연산자 우선순위를 고려한 계산
            result = self.evaluate_expression(self.formula)
            self.current_number = str(result)
            self.operator = None
            self.previous_number = None
            self.waiting_for_operand = True
            
        except ZeroDivisionError:
            self.current_number = "Error"
        except Exception as e:
            self.current_number = "Error"
        
        self.formula += f" = {self.current_number}"
        self.result_display()
        
    def evaluate_expression(self, expression):
        """연산자 우선순위를 고려한 수식 계산"""
        try:
            # = 기호가 있으면 = 뒤의 부분만 사용
            if '=' in expression:
                expression = expression.split('=')[-1].strip()
            
            # 수식 유효성 검사
            if not self.is_valid_expression(expression):
                raise ValueError("잘못된 수식입니다")
            
            # 앞자리 0이 있는 숫자 처리 (02 -> 2)
            import re
            expression = re.sub(r'\b0+(\d+)', r'\1', expression)
            
            # 거듭제곱 연산자 ^ 를 ** 로 변환
            expression = expression.replace('^', '**')
            
            # 공학용 함수들을 Python 함수로 변환
            expression = self.convert_math_functions(expression)
            
            # Python의 eval을 사용하여 연산자 우선순위 자동 처리
            # math 모듈을 사용할 수 있도록 locals에 추가
            result = round(eval(expression, {"math": math}), 6)
            return result
        except Exception as e:
            print(f"계산 오류: {expression}, 오류: {e}")
            raise e  # 오류를 다시 발생시켜서 equal()에서 처리하도록 함
    
    def is_valid_expression(self, expression):
        """수식 유효성 검사"""
        import re
        
        # 빈 수식 체크
        if not expression or expression.strip() == "":
            return False
        
        # 연속된 연산자 체크 (+, -, *, /)
        if re.search(r'[+\-*/]{2,}', expression):
            return False
        
        # 연산자로 시작하거나 끝나는지 체크 (단, -는 음수로 시작 가능)
        if re.match(r'^[+*/]', expression):
            return False
        if re.search(r'[+\-*/]$', expression):
            return False
        
        # 괄호 쌍 체크
        open_count = expression.count('(')
        close_count = expression.count(')')
        if open_count != close_count:
            return False
        
        # 숫자나 연산자, 괄호, 소수점, 거듭제곱, 공학용 함수만 포함하는지 체크
        if not re.match(r'^[0-9+\-*/().\s^a-zA-Z⁻¹²³√⌈⌉⌊⌋|]+$', expression):
            return False
        
        return True
    
    def convert_math_functions(self, expression):
        """공학용 함수들을 Python 함수로 변환"""
        import re
        
        # sin, cos, tan 함수 (도 단위 입력을 라디안으로 변환)
        expression = re.sub(r'sin\(([^)]+)\)', r'math.sin(math.radians(\1))', expression)
        expression = re.sub(r'cos\(([^)]+)\)', r'math.cos(math.radians(\1))', expression)
        expression = re.sub(r'tan\(([^)]+)\)', r'math.tan(math.radians(\1))', expression)
        
        # 역삼각함수 (라디안 결과를 도로 변환)
        expression = re.sub(r'sin⁻¹\(([^)]+)\)', r'math.degrees(math.asin(\1))', expression)
        expression = re.sub(r'cos⁻¹\(([^)]+)\)', r'math.degrees(math.acos(\1))', expression)
        expression = re.sub(r'tan⁻¹\(([^)]+)\)', r'math.degrees(math.atan(\1))', expression)
        
        # 로그 함수
        expression = re.sub(r'log\(([^)]+)\)', r'math.log10(\1)', expression)
        expression = re.sub(r'ln\(([^)]+)\)', r'math.log(\1)', expression)
        
        # 제곱근
        expression = re.sub(r'√\(([^)]+)\)', r'math.sqrt(\1)', expression)
        
        # 제곱, 세제곱
        expression = re.sub(r'\(([^)]+)\)²', r'(\1)**2', expression)
        expression = re.sub(r'\(([^)]+)\)³', r'(\1)**3', expression)
        
        # 절댓값
        expression = re.sub(r'\|([^|]+)\|', r'abs(\1)', expression)
        
        # 올림, 내림
        expression = re.sub(r'⌈([^⌉]+)⌉', r'math.ceil(\1)', expression)
        expression = re.sub(r'⌊([^⌋]+)⌋', r'math.floor(\1)', expression)
        
        # 역수
        expression = re.sub(r'1/\(([^)]+)\)', r'1/(\1)', expression)
        
        # 거듭제곱 함수들
        expression = re.sub(r'10\^\(([^)]+)\)', r'10**(\1)', expression)
        expression = re.sub(r'e\^\(([^)]+)\)', r'math.e**(\1)', expression)
        expression = re.sub(r'2\^\(([^)]+)\)', r'2**(\1)', expression)
        
        # 쌍곡선 함수들
        expression = re.sub(r'sinh\(([^)]+)\)', r'math.sinh(\1)', expression)
        expression = re.sub(r'cosh\(([^)]+)\)', r'math.cosh(\1)', expression)
        expression = re.sub(r'tanh\(([^)]+)\)', r'math.tanh(\1)', expression)
        
        return expression

    def reset(self):
        """초기화 메소드"""
        self.current_number = "0"
        self.previous_number = None
        self.operator = None
        self.waiting_for_operand = False
        self.display_text = "0"
        self.display_process.setText("공식")
        self.formula = ""
        self.update_display()

    # def negative_positive(self):
    #     """음수/양수 변환 메소드"""
    #     if self.current_number != "0" and self.current_number != "Error":
    #         if self.current_number.startswith('-'):
    #             self.current_number = self.current_number[1:]
    #         else:
    #             self.current_number = '-' + self.current_number
    #         self.update_display()

    def percent(self):
        """퍼센트 계산 메소드"""
        if self.current_number != "0" and self.current_number != "Error":
            try:
                value = float(self.current_number)
                self.current_number = str(value / 100)
                self.update_display()
            except:
                self.current_number = "Error"
                self.update_display()
                
                

    def update_display(self):
       self.display_process.setText(self.formula)
        
    def result_display(self):
        self.display_result.setText(self.current_number)
    
    # 공학용 계산기 함수들
    def sin_function(self):
        """사인 함수"""
        try:
            if self.current_number != "0" and self.current_number != "Error":
                value = float(self.current_number)
                if self.angle_mode == "DEG":
                    result = math.sin(math.radians(value))
                else:  # RAD
                    result = math.sin(value)
                self.current_number = str(round(result, 6))
                self.formula = f"sin({value})"
                self.update_display()
                self.result_display()
        except:
            self.current_number = "Error"
            self.result_display()
    
    def cos_function(self):
        """코사인 함수"""
        try:
            if self.current_number != "0" and self.current_number != "Error":
                value = float(self.current_number)
                if self.angle_mode == "DEG":
                    result = math.cos(math.radians(value))
                else:  # RAD
                    result = math.cos(value)
                self.current_number = str(round(result, 6))
                self.formula = f"cos({value})"
                self.update_display()
                self.result_display()
        except:
            self.current_number = "Error"
            self.result_display()
    
    def tan_function(self):
        """탄젠트 함수"""
        try:
            if self.current_number != "0" and self.current_number != "Error":
                value = float(self.current_number)
                if self.angle_mode == "DEG":
                    result = math.tan(math.radians(value))
                else:  # RAD
                    result = math.tan(value)
                self.current_number = str(round(result, 6))
                self.formula = f"tan({value})"
                self.update_display()
                self.result_display()
        except:
            self.current_number = "Error"
            self.result_display()
    
    def asin_function(self):
        """아크사인 함수"""
        try:
            if self.current_number != "0" and self.current_number != "Error":
                value = float(self.current_number)
                if -1 <= value <= 1:
                    result = math.degrees(math.asin(value))  # 라디안을 도로 변환
                    self.current_number = str(round(result, 6))
                    self.formula = f"sin⁻¹({value})"
                    self.update_display()
                    self.result_display()
                else:
                    self.current_number = "Error"
                    self.result_display()
        except:
            self.current_number = "Error"
            self.result_display()
    
    def acos_function(self):
        """아크코사인 함수"""
        try:
            if self.current_number != "0" and self.current_number != "Error":
                value = float(self.current_number)
                if -1 <= value <= 1:
                    result = math.degrees(math.acos(value))
                    self.current_number = str(round(result, 6))
                    self.formula = f"cos⁻¹({value})"
                    self.update_display()
                    self.result_display()
                else:
                    self.current_number = "Error"
                    self.result_display()
        except:
            self.current_number = "Error"
            self.result_display()
    
    def atan_function(self):
        """아크탄젠트 함수"""
        try:
            if self.current_number != "0" and self.current_number != "Error":
                value = float(self.current_number)
                result = math.degrees(math.atan(value))
                self.current_number = str(round(result, 6))
                self.formula = f"tan⁻¹({value})"
                self.update_display()
                self.result_display()
        except:
            self.current_number = "Error"
            self.result_display()
    
    def log_function(self):
        """상용로그 함수 (밑이 10)"""
        try:
            if self.current_number != "0" and self.current_number != "Error":
                value = float(self.current_number)
                if value > 0:
                    result = math.log10(value)
                    self.current_number = str(round(result, 6))
                    self.formula = f"log({value})"
                    self.update_display()
                    self.result_display()
                else:
                    self.current_number = "Error"
                    self.result_display()
        except:
            self.current_number = "Error"
            self.result_display()
    
    def ln_function(self):
        """자연로그 함수 (밑이 e)"""
        try:
            if self.current_number != "0" and self.current_number != "Error":
                value = float(self.current_number)
                if value > 0:
                    result = math.log(value)
                    self.current_number = str(round(result, 6))
                    self.formula = f"ln({value})"
                    self.update_display()
                    self.result_display()
                else:
                    self.current_number = "Error"
                    self.result_display()
        except:
            self.current_number = "Error"
            self.result_display()
    
    def sqrt_function(self):
        """제곱근 함수"""
        try:
            if self.current_number != "0" and self.current_number != "Error":
                value = float(self.current_number)
                if value >= 0:
                    result = math.sqrt(value)
                    self.current_number = str(round(result, 6))
                    self.formula = f"√({value})"
                    self.update_display()
                    self.result_display()
                else:
                    self.current_number = "Error"
                    self.result_display()
        except:
            self.current_number = "Error"
            self.result_display()
    
    def pow_function(self):
        """거듭제곱 함수 (x^y)"""
        self.formula += '^'
        self.update_display()
    
    def square_function(self):
        """제곱 함수 (x²)"""
        try:
            if self.current_number != "0" and self.current_number != "Error":
                value = float(self.current_number)
                result = value ** 2
                self.current_number = str(round(result, 6))
                self.formula = f"({value})²"
                self.update_display()
                self.result_display()
        except:
            self.current_number = "Error"
            self.result_display()
    
    def cube_function(self):
        """세제곱 함수 (x³)"""
        try:
            if self.current_number != "0" and self.current_number != "Error":
                value = float(self.current_number)
                result = value ** 3
                self.current_number = str(round(result, 6))
                self.formula = f"({value})³"
                self.update_display()
                self.result_display()
        except:
            self.current_number = "Error"
            self.result_display()
    
    def pi_function(self):
        """파이 상수"""
        self.current_number = str(math.pi)
        self.formula += str(math.pi)
        self.update_display()
        self.result_display()
    
    def e_function(self):
        """자연상수 e"""
        self.current_number = str(math.e)
        self.formula += str(math.e)
        self.update_display()
        self.result_display()
    
    def factorial_function(self):
        """팩토리얼 함수 (n!)"""
        try:
            if self.current_number != "0" and self.current_number != "Error":
                value = float(self.current_number)
                if value == int(value) and value >= 0 and value <= 170:  # 170!이 float 한계
                    result = math.factorial(int(value))
                    self.current_number = str(result)
                    self.formula = f"{int(value)}!"
                    self.update_display()
                    self.result_display()
                else:
                    self.current_number = "Error"
                    self.result_display()
        except:
            self.current_number = "Error"
            self.result_display()
    
    def abs_function(self):
        """절댓값 함수 (|x|)"""
        try:
            if self.current_number != "0" and self.current_number != "Error":
                value = float(self.current_number)
                result = abs(value)
                self.current_number = str(round(result, 6))
                self.formula = f"|{value}|"
                self.update_display()
                self.result_display()
        except:
            self.current_number = "Error"
            self.result_display()
    
    def ceil_function(self):
        """올림 함수 (⌈x⌉)"""
        try:
            if self.current_number != "0" and self.current_number != "Error":
                value = float(self.current_number)
                result = math.ceil(value)
                self.current_number = str(int(result))
                self.formula = f"⌈{value}⌉"
                self.update_display()
                self.result_display()
        except:
            self.current_number = "Error"
            self.result_display()
    
    def floor_function(self):
        """내림 함수 (⌊x⌋)"""
        try:
            if self.current_number != "0" and self.current_number != "Error":
                value = float(self.current_number)
                result = math.floor(value)
                self.current_number = str(int(result))
                self.formula = f"⌊{value}⌋"
                self.update_display()
                self.result_display()
        except:
            self.current_number = "Error"
            self.result_display()
    
    def one_over_x_function(self):
        """역수 함수 (1/x)"""
        try:
            if self.current_number != "0" and self.current_number != "Error":
                value = float(self.current_number)
                if value != 0:
                    result = 1 / value
                    self.current_number = str(round(result, 6))
                    self.formula = f"1/({value})"
                    self.update_display()
                    self.result_display()
                else:
                    self.current_number = "Error"
                    self.result_display()
        except:
            self.current_number = "Error"
            self.result_display()
    
    def ten_pow_function(self):
        """10의 거듭제곱 함수 (10^x)"""
        try:
            if self.current_number != "0" and self.current_number != "Error":
                value = float(self.current_number)
                result = 10 ** value
                self.current_number = str(round(result, 6))
                self.formula = f"10^({value})"
                self.update_display()
                self.result_display()
        except:
            self.current_number = "Error"
            self.result_display()
    
    def e_pow_function(self):
        """자연상수의 거듭제곱 함수 (e^x)"""
        try:
            if self.current_number != "0" and self.current_number != "Error":
                value = float(self.current_number)
                result = math.e ** value
                self.current_number = str(round(result, 6))
                self.formula = f"e^({value})"
                self.update_display()
                self.result_display()
        except:
            self.current_number = "Error"
            self.result_display()
    
    def two_pow_function(self):
        """2의 거듭제곱 함수 (2^x)"""
        try:
            if self.current_number != "0" and self.current_number != "Error":
                value = float(self.current_number)
                result = 2 ** value
                self.current_number = str(round(result, 6))
                self.formula = f"2^({value})"
                self.update_display()
                self.result_display()
        except:
            self.current_number = "Error"
            self.result_display()
    
    # 추가 공학용 함수들
    def sinh_function(self):
        """쌍곡사인 함수"""
        try:
            if self.current_number != "0" and self.current_number != "Error":
                value = float(self.current_number)
                result = math.sinh(value)
                self.current_number = str(round(result, 6))
                self.formula = f"sinh({value})"
                self.update_display()
                self.result_display()
        except:
            self.current_number = "Error"
            self.result_display()
    
    def cosh_function(self):
        """쌍곡코사인 함수"""
        try:
            if self.current_number != "0" and self.current_number != "Error":
                value = float(self.current_number)
                result = math.cosh(value)
                self.current_number = str(round(result, 6))
                self.formula = f"cosh({value})"
                self.update_display()
                self.result_display()
        except:
            self.current_number = "Error"
            self.result_display()
    
    def tanh_function(self):
        """쌍곡탄젠트 함수"""
        try:
            if self.current_number != "0" and self.current_number != "Error":
                value = float(self.current_number)
                result = math.tanh(value)
                self.current_number = str(round(result, 6))
                self.formula = f"tanh({value})"
                self.update_display()
                self.result_display()
        except:
            self.current_number = "Error"
            self.result_display()
    
    def toggle_angle_mode(self):
        """각도 모드 전환 (DEG/RAD)"""
        if self.angle_mode == "DEG":
            self.angle_mode = "RAD"
            self.btn_angle_mode.setText("RAD")
        else:
            self.angle_mode = "DEG"
            self.btn_angle_mode.setText("DEG")
    
    def random_function(self):
        """0과 1 사이의 난수 생성"""
        result = random.random()
        self.current_number = str(round(result, 6))
        self.formula = "RAND"
        self.update_display()
        self.result_display()
    
    def mod_function(self):
        """나머지 연산자"""
        self.formula += '%'
        self.update_display()
    
    # 메모리 기능들
    def memory_clear(self):
        """메모리 초기화"""
        self.memory = 0
    
    def memory_recall(self):
        """메모리에서 값 불러오기"""
        self.current_number = str(self.memory)
        self.formula = str(self.memory)
        self.update_display()
        self.result_display()
    
    def memory_store(self):
        """현재 값을 메모리에 저장"""
        try:
            self.memory = float(self.current_number)
        except:
            self.memory = 0
    
    def memory_add(self):
        """메모리에 현재 값 더하기"""
        try:
            self.memory += float(self.current_number)
        except:
            pass
    
    def memory_subtract(self):
        """메모리에서 현재 값 빼기"""
        try:
            self.memory -= float(self.current_number)
        except:
            pass
    
    def clear_entry(self):
        """현재 입력만 지우기 (C와 다름)"""
        self.current_number = "0"
        self.formula = ""
        self.update_display()
        self.result_display()

    def showEvent(self, event):
        """윈도우가 표시될 때 호출되는 이벤트 핸들러"""
        super().showEvent(event)
        self.activateWindow()
        self.raise_()
    
    def closeEvent(self, event):
        """윈도우가 닫힐 때 호출되는 이벤트 핸들러"""
        self.hide()
        event.accept()


def main():
    app = QApplication(sys.argv)
    
        # 애플리케이션 스타일 설정
    app.setStyle('Fusion')  # 또는 'Windows', 'WindowsVista' 등

    app.setApplicationName("Engineering Calculator")
    app.setApplicationVersion("1.0")
    
    calculator = Calculator()
    calculator.setFixedSize(400, 700)

        # 윈도우 상태 강제 설정
    calculator.setWindowState(calculator.windowState() & ~Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
    
    # 윈도우를 화면 중앙에 위치시키기
    calculator.setGeometry(
        QStyle.alignedRect(
            Qt.LayoutDirection.LeftToRight,
            Qt.AlignmentFlag.AlignCenter,
            calculator.size(),
            app.primaryScreen().availableGeometry()
        )
    )
    
    calculator.show()
    
    calculator.activateWindow()
    calculator.raise_()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()