#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.ui 파일을 Python 코드로 변환하는 도구
"""

import sys
import os
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel

def convert_ui_to_py(ui_file, output_file=None):
    """UI 파일을 Python 코드로 변환"""
    if not os.path.exists(ui_file):
        print(f"오류: {ui_file} 파일을 찾을 수 없습니다.")
        return False
    
    if output_file is None:
        output_file = ui_file.replace('.ui', '_ui.py')
    
    try:
        # UI 파일을 Python 코드로 변환
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f'# -*- coding: utf-8 -*-\n')
            f.write(f'# 이 파일은 {ui_file}에서 자동 생성되었습니다.\n\n')
            f.write(f'from PyQt6.QtWidgets import *\n')
            f.write(f'from PyQt6.QtCore import *\n')
            f.write(f'from PyQt6.QtGui import *\n\n')
            f.write(f'class Ui_MainWindow(object):\n')
            f.write(f'    def setupUi(self, MainWindow):\n')
            f.write(f'        # UI 파일 로드\n')
            f.write(f'        uic.loadUi("{ui_file}", self)\n\n')
            f.write(f'if __name__ == "__main__":\n')
            f.write(f'    app = QApplication(sys.argv)\n')
            f.write(f'    window = QMainWindow()\n')
            f.write(f'    ui = Ui_MainWindow()\n')
            f.write(f'    ui.setupUi(window)\n')
            f.write(f'    window.show()\n')
            f.write(f'    sys.exit(app.exec())\n')
        
        print(f"✅ {ui_file} → {output_file} 변환 완료!")
        return True
        
    except Exception as e:
        print(f"❌ 변환 중 오류 발생: {str(e)}")
        return False

def main():
    if len(sys.argv) < 2:
        print("사용법: python ui_to_py_converter.py <ui_file> [output_file]")
        print("예시: python ui_to_py_converter.py my_ui.ui")
        return
    
    ui_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    convert_ui_to_py(ui_file, output_file)

if __name__ == "__main__":
    main()









