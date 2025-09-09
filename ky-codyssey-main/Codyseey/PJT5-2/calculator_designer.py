#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Designer로 생성된 계산기
.ui 파일을 사용하여 GUI 구성
"""

import sys
import os
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt6.QtCore import Qt

class CalculatorDesigner(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # UI 파일 로드
        ui_file = os.path.join(os.path.dirname(__file__), 'calculator_designer.ui')
        uic.loadUi(ui_file, self)
        
        # 계산기 상태 변수
        self.current_number = '0'
        self.previous_number = None
        self.operator = None
        self.waiting_for_operand = False
        
        # 버튼 이벤트 연결
        self.connect_buttons()
        
    def connect_buttons(self):
        """모든 버튼에 이벤트 연결"""
        # 숫자 버튼들
        number_buttons = [
            self.btn_0, self.btn_1, self.btn_2, self.btn_3, self.btn_4,
            self.btn_5, self.btn_6, self.btn_7, self.btn_8, self.btn_9
        ]
        
        for button in number_buttons:
            button.clicked.connect(self.number_clicked)
        
        # 소수점 버튼
        self.btn_decimal.clicked.connect(self.decimal_clicked)
        
        # 연산자 버튼들
        self.btn_add.clicked.connect(lambda: self.operator_clicked('+'))
        self.btn_subtract.clicked.connect(lambda: self.operator_clicked('-'))
        self.btn_multiply.clicked.connect(lambda: self.operator_clicked('×'))
        self.btn_divide.clicked.connect(lambda: self.operator_clicked('÷'))
        
        # 기능 버튼들
        self.btn_clear.clicked.connect(self.clear_clicked)
        self.btn_plus_minus.clicked.connect(self.plus_minus_clicked)
        self.btn_percent.clicked.connect(self.percent_clicked)
        self.btn_equals.clicked.connect(self.equals_clicked)
    
    def number_clicked(self):
        """숫자 버튼 클릭 처리"""
        button = self.sender()
        digit = button.text()
        
        if self.waiting_for_operand:
            self.current_number = digit
            self.waiting_for_operand = False
        else:
            if self.current_number == '0':
                self.current_number = digit
            else:
                self.current_number += digit
        
        self.update_display()
    
    def decimal_clicked(self):
        """소수점 버튼 클릭 처리"""
        if self.waiting_for_operand:
            self.current_number = '0.'
            self.waiting_for_operand = False
        elif '.' not in self.current_number:
            self.current_number += '.'
        
        self.update_display()
    
    def operator_clicked(self, op):
        """연산자 버튼 클릭 처리"""
        if self.operator and not self.waiting_for_operand:
            self.calculate()
        
        self.previous_number = float(self.current_number)
        self.operator = op
        self.waiting_for_operand = True
    
    def equals_clicked(self):
        """등호 버튼 클릭 처리"""
        if self.operator and not self.waiting_for_operand:
            self.calculate()
            self.operator = None
            self.waiting_for_operand = True
    
    def clear_clicked(self):
        """C 버튼 클릭 처리"""
        self.current_number = '0'
        self.previous_number = None
        self.operator = None
        self.waiting_for_operand = False
        self.update_display()
    
    def plus_minus_clicked(self):
        """± 버튼 클릭 처리"""
        if self.current_number != '0':
            if self.current_number.startswith('-'):
                self.current_number = self.current_number[1:]
            else:
                self.current_number = '-' + self.current_number
            self.update_display()
    
    def percent_clicked(self):
        """% 버튼 클릭 처리"""
        self.current_number = str(float(self.current_number) / 100)
        self.update_display()
    
    def calculate(self):
        """계산 수행"""
        if self.operator and self.previous_number is not None:
            try:
                if self.operator == '+':
                    result = self.previous_number + float(self.current_number)
                elif self.operator == '-':
                    result = self.previous_number - float(self.current_number)
                elif self.operator == '×':
                    result = self.previous_number * float(self.current_number)
                elif self.operator == '÷':
                    if float(self.current_number) != 0:
                        result = self.previous_number / float(self.current_number)
                    else:
                        self.current_number = 'Error'
                        self.update_display()
                        return
                
                # 결과를 정수로 표시할 수 있으면 정수로, 아니면 소수로
                if result == int(result):
                    self.current_number = str(int(result))
                else:
                    self.current_number = str(result)
                
                self.update_display()
                
            except Exception as e:
                self.current_number = 'Error'
                self.update_display()
    
    def update_display(self):
        """디스플레이 업데이트"""
        # 너무 긴 숫자는 표시 제한
        display_text = self.current_number
        if len(display_text) > 12:
            try:
                # 과학적 표기법으로 변환
                num = float(display_text)
                display_text = f"{num:.6e}"
            except:
                display_text = "Error"
        
        self.display.setText(display_text)

def main():
    app = QApplication(sys.argv)
    
    # 애플리케이션 정보 설정
    app.setApplicationName("Calculator Designer")
    app.setApplicationVersion("1.0")
    
    # 메인 윈도우 생성 및 표시
    calculator = CalculatorDesigner()
    calculator.setFixedSize(320, 480)  # 창 크기 고정
    calculator.show()
    
    # 이벤트 루프 시작
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
