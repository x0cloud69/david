list1 = [[1,4,8],[3,5,19],[8,16,3]]
list2 = [[2,8,3],[18,5,3],[7,5,12]]

add_list= []

for i in range(len(list1)):
    temp =[]
    for j in range(len(list1[i])):
        temp.append(list1[i][j] + list2[i][j])
    add_list.append(temp)
    
print(list1)
print(list2)
print(add_list) 