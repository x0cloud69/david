import numpy as np
import matplotlib.pyplot as plt

plt.rc('font',family='Malgun Gothic') # 한글 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False # 마이너스 깨짐 방지

x = np.linspace(0,10,100)
y = np.sin(x)

a = np.random.rand(50)
b = a + np.random.normal(0,0.1,50)

history = np.random.normal(0,1,1000)

x = np.array([[1,2,3],
             [4,5,6]], dtype=np.int16,order='C')
x.strides
print(x.strides)
print(x.tobytes('A'))
print(x.__array_interface__)

y = np.frombuffer(x, dtype=np.int8)
y.data
y.base is x
print(y.flags)

# 높은 정밀도 필요
precise = np.array([1.12345678901234567890], dtype=np.float64)
print(precise)  # 15-17자리 정밀도

# 일반적인 용도
normal = np.array([1.12345678901234567890], dtype=np.float32)
print(normal)  # 6-8자리 정밀도



# plt.figure(figsize=(8,6))
# plt.plot(x,y,'r-',label='sin(x)')
# plt.scatter(a,b,alpha=0.5,label='scatter')
# plt.hist(history,bins=30,alpha=0.5,label='hist',color='g')
# plt.title('기본 선 그래프')
# plt.xlabel('x축')
# plt.ylabel('y축')
# plt.legend()
# plt.grid(True)
# plt.show()

# # 이미지 생성
# rng = np.random.default_rng(27446968)
# image = rng.random((30, 30))

# # 그래프 크기 설정
# plt.figure(figsize=(8, 6))

# # 이미지 표시
# im = plt.imshow(image, cmap=plt.cm.hot)

# # 컬러바 추가
# plt.colorbar(im)

# # 제목 추가
# plt.title('열지도 (Heatmap)')

# # 축 레이블 추가
# plt.xlabel('X 축')
# plt.ylabel('Y 축')

# # 그래프 표시
# plt.show()