#encoding:utf-8
#十进制转为二进制
import sys
sys.path.append('/home/zhaowentao/桌面/python_program/和鲸社区/data_structure/Stack_and_queue/')
import Sequential_stack
stack = Sequential_stack.sequential_stack()
test = [200, 254, 153, 29, 108, 631, 892]
flag = 1
for i in test:
    cur = i
    while flag:
        #将其对2求余得到的二进制数的各位依次进栈，计算完毕后将栈中的二
        #进制数依次出栈输出，输出结果就是待求得的二进制数
        stack.push(cur%2)
        cur = int(cur/2)
        if cur < 1:
            flag = 0
        else:
            continue
    print(i,"的二进制为",end=" ")
    stack.walk_through()
    print("\n",end="")
    stack.clear_stack()
    flag = 1