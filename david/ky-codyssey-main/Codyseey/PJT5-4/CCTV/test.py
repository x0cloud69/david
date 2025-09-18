import numpy as np
arry = np.array([[1,2,3],[4,15,6],[7,8,9]])
arry_t = arry.T
print(arry)
print("--"*30)
print(arry_t)
print(np.max(arry_t[:3]))
print(np.argmax(arry_t[:2]))