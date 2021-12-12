#encoding:utf-8
from __future__ import print_function
class sequential_queue:
    def __init__(self):
        self.que = []

    #注意，这里列表的开头是队尾，末尾是队头
    def queue_add(self,val):
        self.que.append(val)

    #队列先进先出，所以从第一个位置pop
    def queue_pop(self):
        self.que.pop(0)

    def jug_empty(self):
        if self.que:
            print("It is not a empty queue")
        else:
            print("It is an empty queue")

    def get_length(self):
        print(len(self.que))
    
    def get_top_elem(self):
        print(self.que[-1])

    def walk_through(self):
        if self.que:
            print(self.que[::-1])         
        else:
            print("It is an empty queue")

    def clear_que(self):
        self.que = []

test = sequential_queue()
test.queue_add(1)
test.queue_add(2)
test.queue_add(3)
print("--The elements of queue--")
test.walk_through()
test.jug_empty()
print("--Dequeue an element--")
test.queue_pop()
print("---The length of queue after pop an elements---")
test.get_length()
print("---The elements of queue")
test.walk_through()
print("--Get the top elements of queue")
test.get_top_elem()
test.clear_que()
print("------clear queue------")
test.walk_through()


