#encoding:utf-8
class Node:
    def __init__(self, val):
      self.next = None
      self.val = val

#链栈实际上就是一个只能采用头插法插入或删除数据的链表。
class Chain_stack:
    def __init__(self):
      self.head = None

    def push(self,val):
        node = Node(val)
        cur = self.head
        if cur is None:
            cur = node
            self.head = cur
        #这里就很精髓的展示出了头指针的用处。1.如果是第一个元素的插入，那么使用头指针直接push即可。2.如果不是，头指针直
        #接变成节点结构赋值给cur，便于cur的遍历寻找
        #注意这里与链表不同，头指针指向的是栈顶，这样可以避免在实现数据 "入栈" 和 "出栈" 操作时做大量遍历链表的耗时操作。
        else:
            self.head = node
            node.next = cur

    def pop(self):
        cur = self.head
        if cur is None:
            print("No elements,cannot be poped")
        else:
            #头指针指向他的下一个栈
            self.head = cur.next
        #返回当前栈里的元素
        return cur.val

    def get_length(self):
        cur = self.head
        length = 0
        while cur is not None:
            cur = cur.next
            length += 1
        print(length)

    def jug_empty(self):
        if self.get_length:
            print("It is not an empty stack")
        else:
            print("It is an empty stack")

    def clear_stack(self):
        self.head = None

    def walk_through(self):
        cur = self.head
        if cur is None:
            print("There is no element")
        while cur is not None:
            print(cur.val)
            cur = cur.next

test = Chain_stack()
test.push(1)
test.push(2)
test.push(3)
test.push(4)
test.pop()
test.get_length()
test.jug_empty()
test.walk_through()
print("------clead stack------")
test.clear_stack()
test.walk_through()