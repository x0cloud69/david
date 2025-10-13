import os
import numpy as np

file_dir   = os.path.dirname(os.path.abspath(__file__))
file_001 = 'mars_base_main_parts-001.csv'
file_002 = 'mars_base_main_parts-002.csv'
file_003 = 'mars_base_main_parts-003.csv'

file_name_001 = os.path.join(file_dir,file_001)
file_name_002 = os.path.join(file_dir,file_002)
file_name_003 = os.path.join(file_dir,file_003)


arr1,arr2,arr3 = [],[],[]
parts           = []

arr1 = np.genfromtxt(file_name_001,delimiter=',',skip_header=1,dtype=str,encoding='utf-8')
arr2 = np.genfromtxt(file_name_002,delimiter=',',skip_header=1,dtype=str,encoding='utf-8')
arr3 = np.genfromtxt(file_name_003,delimiter=',',skip_header=1,dtype=str,encoding='utf-8')


parts = np.vstack((arr1,arr2,arr3))
print('---- parts ---')
print(parts)
