# import numpy as np
# from numpy.lib.stride_tricks import as_strided

# def extract_image_patches(image, patch_size=(3, 3)):
#     """이미지에서 겹치는 패치들을 추출"""
#     h, w = image.shape
#     stride_h, stride_w = image.strides
#     print(stride_h)
#     print(stride_w)
    
#     patches = as_strided(image,
#                         shape=(h-patch_size[0]+1, w-patch_size[1]+1, 
#                               patch_size[0], patch_size[1]),
#                         strides=(stride_h, stride_w, stride_h, stride_w))
#     return patches

# # 예시 사용
# image = np.array([[1, 2, 3, 4],
#                   [5, 6, 7, 8],
#                   [9, 10, 11, 12]])

# print(image)

# patches = extract_image_patches(image, (2, 2))
# print("추출된 패치들:")
# print(patches)

import numpy as np

# 1. 기본 배열의 stride 확인
arr = np.array([[1, 2, 3],
                [4, 5, 6]], dtype=np.int32)
print(f"Shape: {arr.shape}")
print(f"Strides: {arr.strides}")  # (12, 4) - 행 이동 12바이트, 열 이동 4바이트

# 2. 다른 데이터 타입의 영향
arr_float = np.array([[1, 2, 3],
                      [4, 5, 6]], dtype=np.float64)
print(f"Float64 Strides: {arr_float.strides}")  # (24, 8) - 더 큰 stride