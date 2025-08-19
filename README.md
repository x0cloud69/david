## 반달곰 커피 홈페이지
[참조링크](https://반달곰 커피)

### 문구:오디오 출력소스코드
```python
lang = request.args.get('lang', DEFAULT_LANG)
fp = BytesIO()
gTTS(text, "com", lang).write_to_fp(fp)
encoded_audio_data = base64.b64encode(fp.getvalue())
```
### 이미지
![david](./static/david.jpg)




# 예시
[GitHub][1]
[1]: https://github.com "GitHub 홈페이지"

[Google][google]
[google]: https://google.com


## 소개
이 프로젝트는 ...

## 설치 방법
```bash
npm install
