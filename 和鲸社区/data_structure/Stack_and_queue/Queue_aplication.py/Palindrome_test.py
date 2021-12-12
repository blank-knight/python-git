#encoding:utf-8
#回文词检测
import sys
sys.path.append('/home/zhaowentao/桌面/python_program/和鲸社区/data_structure/Stack_and_queue/')
import Sequential_deque
deque = Sequential_deque.sequential_deque()
test = ["abcgcba","refer","reference"]
flag = 1
for i in test:
    #进入队列
    for j in i:
        deque.queue_add(j)
    fre = int(len(i)/2)
    while fre > 0:
        #判断是否头尾字母相同
        if deque.top_pop() != deque.rear_pop():
            print("不是回文词！")
            flag = 0
            break
        else:
            fre -= 1
    if flag:
        print("是回文词！")
    #清空队列，不然队列中可能会有遗留字母
    deque.clear_que()
    