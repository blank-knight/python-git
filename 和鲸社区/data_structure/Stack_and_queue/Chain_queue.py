#encoding:utf-8
from __future__ import print_function
class Node:
    def __init__(self,val):
        self.next = None
        self.val = val

class Chain_queue:
    # init初始化函数只有第一次初始化类时才会调用，之后都不会调用
    def __init__(self):
        self.rear = self.top = Node(None)

    def queue_add(self,val):
        node = Node(val)
        cur = self.rear
        cur.next = node
        self.rear = node

    def queue_pop(self):
        self.top.next = self.top.next.next

    def get_length(self):
        cur = self.top
        length = 0
        while cur.next is not None:
            cur = cur.next
            length += 1
        return length
        
    def jug_empty(self):
        if self.get_length():
            print("It is not an empty queue")
        else:
            print("It is an empty queue")

    def get_top_elem(self):
        return self.top.next.val

    def walk_through(self):
        cur = self.top
        while cur.next is not None:
            cur = cur.next
            print(cur.val,end=" ")

    def clead_queue(self):
        self.top = self.read = Node(None)

test = Chain_queue()
test.queue_add(1)
test.queue_add(2)
test.queue_add(3)
test.walk_through()
print("\n---队列长度---")
print(test.get_length())
print("---获取首元素---")
print(test.get_top_elem())
print("---是否是空队列---")
test.jug_empty()
print("---pop一个后---")
test.queue_pop()
test.walk_through()
print("\n---清空队列后---")
test.clead_queue()
test.walk_through()