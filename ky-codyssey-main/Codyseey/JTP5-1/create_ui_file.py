#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.ui 파일을 코드로 생성하는 예제
Designer 없이 UI 파일 만들기
"""

def create_ui_file():
    """간단한 .ui 파일 생성"""
    ui_content = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>400</width>
    <height>300</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>PyQt6 GUI</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QVBoxLayout" name="verticalLayout">
    <item>
     <widget class="QLabel" name="label">
      <property name="text">
       <string>안녕하세요! PyQt6입니다.</string>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QLineEdit" name="lineEdit">
      <property name="placeholderText">
       <string>텍스트를 입력하세요...</string>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QPushButton" name="pushButton">
      <property name="text">
       <string>클릭하세요</string>
      </property>
     </widget>
    </item>
   </layout>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>400</width>
     <height>22</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>'''
    
    with open('simple_ui.ui', 'w', encoding='utf-8') as f:
        f.write(ui_content)
    
    print("simple_ui.ui 파일이 생성되었습니다!")

if __name__ == "__main__":
    create_ui_file()



