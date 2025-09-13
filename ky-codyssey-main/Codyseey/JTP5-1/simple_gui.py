#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyQt6를 사용한 간단한 GUI 예제
Designer 없이 코드로 GUI 생성
"""

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                             QTextEdit, QMessageBox, QFileDialog)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        # 메인 윈도우 설정
        self.setWindowTitle("PyQt6 GUI 예제")
        self.setGeometry(100, 100, 600, 400)
        
        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 제목
        title_label = QLabel("PyQt6 GUI 애플리케이션")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # 입력 섹션
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("텍스트를 입력하세요...")
        input_layout.addWidget(QLabel("입력:"))
        input_layout.addWidget(self.input_field)
        
        main_layout.addLayout(input_layout)
        
        # 버튼 섹션
        button_layout = QHBoxLayout()
        
        self.show_button = QPushButton("텍스트 표시")
        self.show_button.clicked.connect(self.show_text)
        button_layout.addWidget(self.show_button)
        
        self.clear_button = QPushButton("지우기")
        self.clear_button.clicked.connect(self.clear_text)
        button_layout.addWidget(self.clear_button)
        
        self.file_button = QPushButton("파일 열기")
        self.file_button.clicked.connect(self.open_file)
        button_layout.addWidget(self.file_button)
        
        main_layout.addLayout(button_layout)
        
        # 텍스트 출력 영역
        self.text_output = QTextEdit()
        self.text_output.setPlaceholderText("결과가 여기에 표시됩니다...")
        main_layout.addWidget(self.text_output)
        
        # 상태 표시
        self.status_label = QLabel("준비됨")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # 타이머 설정 (자동 업데이트)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(1000)  # 1초마다 업데이트
        
    def show_text(self):
        """입력된 텍스트를 출력 영역에 표시"""
        text = self.input_field.text()
        if text:
            self.text_output.append(f"입력된 텍스트: {text}")
            self.status_label.setText("텍스트가 표시되었습니다.")
        else:
            QMessageBox.warning(self, "경고", "텍스트를 입력해주세요!")
            
    def clear_text(self):
        """텍스트 영역 지우기"""
        self.text_output.clear()
        self.input_field.clear()
        self.status_label.setText("텍스트가 지워졌습니다.")
        
    def open_file(self):
        """파일 열기 대화상자"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "파일 열기", "", "모든 파일 (*);;텍스트 파일 (*.txt);;Python 파일 (*.py)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_output.append(f"파일 내용 ({file_path}):\n{content}")
                self.status_label.setText(f"파일을 열었습니다: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"파일을 읽을 수 없습니다: {str(e)}")
                
    def update_status(self):
        """상태 업데이트 (타이머용)"""
        # 여기에 주기적으로 실행할 코드를 추가할 수 있습니다
        pass
        
    def closeEvent(self, event):
        """프로그램 종료 시 실행"""
        reply = QMessageBox.question(
            self, "종료 확인", "정말로 종료하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    
    # 애플리케이션 정보 설정
    app.setApplicationName("PyQt6 GUI 예제")
    app.setApplicationVersion("1.0")
    
    # 메인 윈도우 생성 및 표시
    window = MainWindow()
    window.show()
    
    # 이벤트 루프 시작
    sys.exit(app.exec())

if __name__ == "__main__":
    main()



