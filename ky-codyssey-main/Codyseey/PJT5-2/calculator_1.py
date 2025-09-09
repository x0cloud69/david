import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # 메인 레이아웃 설정
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # 결과 표시 레이블
        self.display = QLabel('0')
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setFont(QFont('Arial', 40))
        self.display.setStyleSheet('''
            QLabel {
                color: white;
                background: #333333;
                padding: 10px;
                margin-bottom: 10px;
            }
        ''')
        main_layout.addWidget(self.display)
        
        # 버튼 그리드 레이아웃
        grid_layout = QGridLayout()
        main_layout.addLayout(grid_layout)
        
        # 버튼 텍스트 배열
        buttons = [
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]
        
        # 버튼 스타일
        number_style = '''
            QPushButton {
                background-color: #505050;
                color: white;
                border-radius: 20px;
                font-size: 20px;
                min-width: 40px;
                min-height: 40px;
            }
            QPushButton:pressed {
                background-color: #707070;
            }
        '''
        
        operator_style = '''
            QPushButton {
                background-color: #FF9500;
                color: white;
                border-radius: 20px;
                font-size: 20px;
                min-width: 40px;
                min-height: 40px;
            }
            QPushButton:pressed {
                background-color: #FFB143;
            }
        '''
        
        function_style = '''
            QPushButton {
                background-color: #D4D4D2;
                color: black;
                border-radius: 20px;
                font-size: 20px;
                min-width: 40px;
                min-height: 40px;
            }
            QPushButton:pressed {
                background-color: #E8E8E8;
            }
        '''
        
        # 버튼 생성 및 배치
        for row, row_buttons in enumerate(buttons):
            for col, button_text in enumerate(row_buttons):
                button = QPushButton(button_text)
                
                # 스타일 적용
                if button_text in ['÷', '×', '-', '+', '=']:
                    button.setStyleSheet(operator_style)
                elif button_text in ['AC', '+/-', '%']:
                    button.setStyleSheet(function_style)
                else:
                    button.setStyleSheet(number_style)
                
                # 0 버튼은 2칸 차지
                if button_text == '0':
                    grid_layout.addWidget(button, row, col, 1, 2)
                else:
                    grid_layout.addWidget(button, row, col)
                
                # 버튼 클릭 이벤트 연결
                button.clicked.connect(self.button_clicked)
    
    def button_clicked(self):
        button = self.sender()
        current_text = self.display.text()
        
        if button.text() == 'AC':
            self.display.setText('0')
        elif button.text() in ['+/-', '%', '÷', '×', '-', '+', '=']:
            # 연산자 버튼은 이 단계에서는 기능 구현하지 않음
            pass
        else:
            # 숫자나 소수점 입력
            if current_text == '0':
                self.display.setText(button.text())
            else:
                self.display.setText(current_text + button.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.setWindowTitle('Calculator')
    calc.setFixedSize(300, 400)  # 창 크기 고정
    calc.setStyleSheet('background-color: #333333;')
    calc.show()
    sys.exit(app.exec_())
