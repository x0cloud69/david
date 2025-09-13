import sys
import os
import subprocess
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt6.QtCore import Qt


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()

        # UI 파일 로드
        ui_file = os.path.join(os.path.dirname(__file__), 'calculator_designer_test_2.ui')
        uic.loadUi(ui_file, self)

        # 계산기 상태 변수
        self.current_number = "0"
        self.previous_number = None
        self.operator = None
        self.waiting_for_operand = False
        self.display_text = "0"
        self.formula = ""  # 공식식

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
        
        # 공학용 계산기 버튼
        self.label_science.clicked.connect(self.open_engineering_calculator)
        
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
            
            # % 연산자를 비율 계산으로 변환 (예: 100 % 10 -> 100 * 10 / 100)
            expression = re.sub(r'(\d+(?:\.\d+)?)\s*%\s*(\d+(?:\.\d+)?)', r'(\1 * \2 / 100)', expression)
            
            # Python의 eval을 사용하여 연산자 우선순위 자동 처리
            result = round(eval(expression), 6)
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
        
        # 연속된 연산자 체크 (+, -, *, /, %)
        if re.search(r'[+\-*/%]{2,}', expression):
            return False
        
        # 연산자로 시작하거나 끝나는지 체크 (단, -는 음수로 시작 가능)
        if re.match(r'^[+*/%]', expression):
            return False
        if re.search(r'[+\-*/%]$', expression):
            return False
        
        # 괄호 쌍 체크
        open_count = expression.count('(')
        close_count = expression.count(')')
        if open_count != close_count:
            return False
        
        # 숫자나 연산자, 괄호, 소수점만 포함하는지 체크
        if not re.match(r'^[0-9+\-*/%(.).\s]+$', expression):
            return False
        
        return True

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
                self.formula += '%'
                self.update_display()
            except:
                self.current_number = "Error"
                self.update_display()
 
                
                

    def update_display(self):
       self.display_process.setText(self.formula)
        
    def result_display(self):
        self.display_result.setText(self.current_number)
    
    def open_engineering_calculator(self):
        """공학용 계산기 실행"""
        try:
            # engineering_calculator.py 파일의 절대 경로
            engineering_calc_path = os.path.join(os.path.dirname(__file__), 'engineering_calculator.py')
            
            # Python으로 engineering_calculator.py 실행
            subprocess.Popen([sys.executable, engineering_calc_path])
        except Exception as e:
            print(f"공학용 계산기 실행 오류: {e}")


def main():
    app = QApplication(sys.argv)
    
    app.setApplicationName("Calculator")
    app.setApplicationVersion("1.0")
    
    calculator = Calculator()
    calculator.setFixedSize(370, 540)
    calculator.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()