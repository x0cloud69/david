#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.ui 파일을 Python 코드로 변환하는 예제
"""

import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # .ui 파일 로드
        try:
            uic.loadUi('simple_ui.ui', self)
        except FileNotFoundError:
            print("simple_ui.ui 파일을 찾을 수 없습니다.")
            print("먼저 create_ui_file.py를 실행해주세요.")
            return
        
        # 버튼 클릭 이벤트 연결
        self.pushButton.clicked.connect(self.button_clicked)
        
    def button_clicked(self):
        """버튼 클릭 시 실행"""
        text = self.lineEdit.text()
        if text:
            self.label.setText(f"입력된 텍스트: {text}")
        else:
            self.label.setText("텍스트를 입력해주세요!")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()



