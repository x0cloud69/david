import signal
import time
import sys

def signal_handler(signum, frame):
    print('\nCtrl+C가 감지되었습니다!')
    print('프로그램을 종료합니다...')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    print("Ctrl+C 테스트 프로그램 시작")
    print("Ctrl+C를 눌러보세요...")
    
    try:
        while True:
            print("실행 중... (Ctrl+C로 종료)")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt가 발생했습니다.")
        sys.exit(0)








