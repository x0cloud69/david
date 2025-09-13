import sys
import os
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
        self.formula = ""
        self.previous_number = None
        self.operator = None
        self.waiting_for_operand = False

        # 버튼 이벤트 연결
        self.connect_buttons()
    
    def connect_buttons(self):
        # 숫자 버튼
        number_buttons = [self.btn_0,self.btn_1,self.btn_2,
                          self.btn_3,self.btn_4,self.btn_5,self.btn_6,
                          self.btn_7,self.btn_8,self.btn_9]
        
        for button in number_buttons:
            button.clicked.connect(self.number_clicked)
        
        # 클리어 버튼 연결
        self.btn_cls.clicked.connect(self.clear_clicked)
        
        # 연산자 버튼 연결
        self.btn_plus.clicked.connect(lambda: self.operator_clicked('+'))
        self.btn_minus.clicked.connect(lambda: self.operator_clicked('-'))
        self.btn_mul.clicked.connect(lambda: self.operator_clicked('*'))
        self.btn_divid.clicked.connect(lambda: self.operator_clicked('/'))
        
        # 기타 버튼 연결
        self.btn_result.clicked.connect(self.equals_clicked)
        self.btn_point.clicked.connect(self.decimal_clicked)
        
    def operator_clicked(self,op):
        # Error 상태인 경우 연산자 클릭 무시
        if self.current_number == 'Error':
            return
            
        # = 결과가 나온 후 연산자 입력 시 이전 결과를 유지
        if '=' in self.formula:
            # = 뒤의 결과값만 추출하여 새로운 계산 시작
            result_part = self.formula.split('=')[-1].strip()
            self.formula = result_part + op
            self.current_number = result_part
        else:
            # 첫 번째 연산자인 경우 현재 숫자를 formula에 추가
            if not self.formula:
                self.formula = self.current_number
            self.formula += op
            
        self.previous_number = float(self.current_number)
        self.operator = op
        self.waiting_for_operand = True
        
        # 연산자 클릭 후 디스플레이 업데이트
        self.update_display()
        
    def calculate(self):
        if self.operator and self.previous_number is not None:
            try:
                if self.operator == '+':
                    result = self.previous_number + float(self.current_number)
                    #self.formula += f' + {self.current_number}'
                elif self.operator == '-':
                    result = self.previous_number - float(self.current_number)
                    #self.formula += f' - {self.current_number}'
                elif self.operator == '*':
                    result = self.previous_number * float(self.current_number)
                    #self.formula += f' * {self.current_number}'
                elif self.operator == '/':
                    if float(self.current_number) != 0:
                        result = self.previous_number / float(self.current_number)
                     #   self.formula += f' / {self.current_number}'
                    else:
                        self.current_number = 'Error'
                        self.update_display()
                        return
                
                if result == int(result):
                    self.current_number = str(int(result))
                else:
                    self.current_number = str(result)
                    
                self.update_display()
                
            except Exception as e:
                self.current_number = 'Error'
                self.update_display()
        

    def number_clicked(self):
        button = self.sender()
        number = button.text()
        
        # = 결과가 나온 후 새로운 숫자 입력 시 초기화
        if '=' in self.formula:
            self.formula = number
            self.current_number = number
            self.previous_number = None
            self.operator = None
            self.waiting_for_operand = False
        else:
            self.formula += number
            # 연산자 입력 후 첫 번째 숫자인 경우
            if self.waiting_for_operand:
                self.current_number = number
                self.waiting_for_operand = False
            else:
                # 기존 숫자에 추가
                if self.current_number == "0":
                    self.current_number = number
                else:
                    self.current_number += number

        self.update_display()
        
    def equals_clicked(self):
        if self.operator and not self.waiting_for_operand:
            # 연산자 우선순위에 따라 계산
            result = self.evaluate_expression(self.formula)
            self.current_number = str(result)
            self.formula += f' = {self.current_number}'
        else:
            # 연산자가 없는 경우 현재 수식 계산
            if self.formula and not self.formula.endswith(('+', '-', '*', '/')):
                result = self.evaluate_expression(self.formula)
                self.current_number = str(result)
                self.formula += f' = {self.current_number}'
        
        self.operator = None
        self.waiting_for_operand = True
        self.update_display()
        
    def evaluate_expression(self, expression):
        """연산자 우선순위를 고려한 수식 계산"""
        try:
            # = 기호가 있으면 = 뒤의 부분만 사용
            if '=' in expression:
                expression = expression.split('=')[-1].strip()
            
            # 앞자리 0이 있는 숫자 처리 (02 -> 2)
            import re
            # 0으로 시작하는 숫자를 찾아서 처리
            expression = re.sub(r'\b0+(\d+)', r'\1', expression)
            
            # Python의 eval을 사용하여 연산자 우선순위 자동 처리
            result = eval(expression)
            return result
        except Exception as e:
            print(f"계산 오류: {expression}, 오류: {e}")
            return 0
        
    def decimal_clicked(self):
        if self.waiting_for_operand:
            self.current_number = "0."
            self.waiting_for_operand = False
        elif "." not in self.current_number:
            self.current_number += "."
        self.update_display()
        
    def clear_clicked(self):
        self.current_number = "0"
        self.formula = ""
        self.display_result.setText(self.current_number)
        self.display_process.setText("공식")

    def update_display(self, text=None):
        if text is not None:
            if self.current_number == "0":
                self.current_number = text
            else:
                self.current_number += text
        
        # UI 파일에서 라벨 이름이 label_result이므로 수정
        self.display_result.setText(self.current_number)
        self.display_process.setText(self.formula)





def main():
    app = QApplication(sys.argv)

    app.setApplicationName("Calculator Designer")
    app.setApplicationVersion("1.0")

    calculation = Calculator()
    calculation.setFixedSize(370, 540)
    calculation.show()

     # 이벤트 루프 시작
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

