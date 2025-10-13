# 디버깅 테스트 파일
def test_function():
    x = 10
    y = 20
    result = x + y
    print(f"결과: {result}")
    return result

# 메인 실행
if __name__ == "__main__":
    print("디버깅 테스트 시작")
    result = test_function()
    print(f"최종 결과: {result}")
    print("디버깅 테스트 완료")
