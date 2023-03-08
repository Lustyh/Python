

# 一行if-else 判断

x = 12
print('Test Pass') if x >=13 else print('Test Fail')



# 一行列表推导

test_list = [i for i in range(12)]
print(test_list)
# >>[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]



# 一航字典推导

test_dict = {x:x*x for x in range(5)}
print(test_dict)
# >>{0: 0, 1: 1, 2: 4, 3: 9, 4: 16}




# 合并字典

dict1 = {'a':1, 'b':2}
dict2 = {'c':3, 'd':4}

merged_dict = {**dict1,**dict2}
print(merged_dict)
# >>{'a': 1, 'b': 2, 'c': 3, 'd': 4}  


#删除列表重复元素
list1 = [1,2,3,4,1,2,3,4,1,2,3,4,5,6,7,7,6,5,4,3,123]

print(list(set(list1)))
# >>[1, 2, 3, 4, 5, 6, 7, 123]


# 列表元素筛选

my_list = [10, 11, 12, 13, 14, 15]
# 选出所有偶数
print(list(filter(lambda x: x%2 == 0, my_list )))

# >>[10, 12, 14]

# 优雅列表赋值

info = ['brucepk', 'man', 'python']
name,sex,tech = info
print(name,sex,tech)

# >>brucepk man python