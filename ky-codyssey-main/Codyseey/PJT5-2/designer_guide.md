# Qt Designer 사용법 가이드

## Designer로 계산기 만드는 방법

### 1. Designer 실행
```bash
# 방법 1: 직접 실행
C:/PyQt/6.9.2/mingw_64/bin/designer.exe

# 방법 2: 배치 파일 실행 (JTP5-1 폴더에 있음)
run_designer.bat
```

### 2. 새 프로젝트 생성
1. Designer 실행
2. **File** → **New** → **Main Window** 선택
3. **Create** 클릭

### 3. 위젯 배치
1. **Widget Box**에서 위젯을 드래그 앤 드롭
2. **Property Editor**에서 속성 설정
3. **Object Inspector**에서 위젯 계층 구조 확인

### 4. 레이아웃 설정
1. 위젯 선택 후 **Layout** 메뉴 사용
2. **Grid Layout** 또는 **Vertical/Horizontal Layout** 선택
3. **Form** → **Lay Out in a Grid** 사용

### 5. 스타일 설정
1. 위젯 선택
2. **Property Editor**에서 **styleSheet** 속성 설정
3. CSS 스타일 문법 사용

### 6. 파일 저장
1. **File** → **Save As**
2. `.ui` 확장자로 저장
3. 예: `calculator_designer.ui`

### 7. Python 코드로 변환
```python
from PyQt6 import uic

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('my_designer.ui', self)
```

## 주요 위젯들

### 기본 위젯
- **QLabel**: 텍스트 표시
- **QPushButton**: 버튼
- **QLineEdit**: 텍스트 입력
- **QTextEdit**: 여러 줄 텍스트

### 레이아웃 위젯
- **QVBoxLayout**: 세로 배치
- **QHBoxLayout**: 가로 배치
- **QGridLayout**: 격자 배치
- **QFormLayout**: 폼 배치

### 컨테이너 위젯
- **QGroupBox**: 그룹 박스
- **QTabWidget**: 탭 위젯
- **QStackedWidget**: 스택 위젯

## 스타일시트 예제

### 버튼 스타일
```css
QPushButton {
    background-color: #ff6b6b;
    color: white;
    border-radius: 25px;
    font-size: 18px;
    font-weight: bold;
    min-width: 60px;
    min-height: 60px;
}
QPushButton:pressed {
    background-color: #ff5252;
}
```

### 레이블 스타일
```css
QLabel {
    color: white;
    background: #1a1a1a;
    padding: 20px;
    margin-bottom: 10px;
    border-radius: 10px;
    font-size: 32px;
    font-weight: bold;
}
```

## 장점과 단점

### Designer 사용 시 장점
✅ **시각적 편집**: 드래그 앤 드롭으로 쉽게 배치
✅ **빠른 프로토타이핑**: UI를 빠르게 만들 수 있음
✅ **일관성**: 표준화된 UI 패턴 사용
✅ **유지보수**: UI 수정이 쉬움

### Designer 사용 시 단점
❌ **제한적 제어**: 복잡한 동적 레이아웃 어려움
❌ **코드 분리**: UI와 로직이 분리됨
❌ **의존성**: .ui 파일에 의존

## 팁과 트릭

1. **이름 규칙**: 위젯 이름을 의미있게 설정 (`btn_1`, `lbl_display`)
2. **그룹화**: 관련 위젯들을 그룹박스로 묶기
3. **스타일 재사용**: 공통 스타일을 변수로 정의
4. **미리보기**: **Form** → **Preview**로 결과 확인
5. **키보드 단축키**: Tab 키로 위젯 간 이동
