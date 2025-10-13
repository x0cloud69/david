
print(range(10))
print(enumerate(['body','food','love','fun','happy','sad','angry','fear','surprise']))
for i, item in enumerate(['body','food','love','fun','happy','sad','angry','fear','surprise']):
    print(i, item)
    
sum = lambda a,b : a+b
sum(3,4)
print(sum(13,4))

def two_time(x):
    return x*2
result = ()
result = tuple(map(two_time,[1,2,32,5,19]))   
print(result)


abc = tuple(zip([1,2,3,5],[4,5,4,36],[1,8,39,23]))
print(abc)
