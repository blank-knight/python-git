#encoding:utf-8
#十进制转任意进制数
import sys
sys.path.append('/home/zhaowentao/桌面/python_program/和鲸社区/data_structure/Stack_and_queue/')
import Sequential_stack
stack = Sequential_stack.sequential_stack()
def transfrom(val,num):
    flag = 1
    cur = val
    while flag:
        #将其对各进制求余得到的数的依次进栈，计算完毕后将栈中的
        #进制数依次出栈输出，输出结果就是待求得的进制数
        stack.push(cur%num)
        cur = int(cur/num)
        if cur < 1:
            flag = 0
        else:
            continue
    print("{0}的{1}进制为".format(val,num),end=" ")
    stack.walk_through()
    print("\n",end="")
    stack.clear_stack()
    flag = 1

transfrom(200,8)
transfrom(254,4)
transfrom(153,4)
transfrom(29,4)
transfrom(108,4)
transfrom(631,8)
transfrom(892,4)