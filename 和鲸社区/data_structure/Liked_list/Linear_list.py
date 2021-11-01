# 定义节点
class Node:
    def __init__(self,data) -> None:
        self.data = data
        self.next = None

class Liner_list:
    # 定义头指针
    def __init__(self) -> None:
        self.head = None

    #头插法
    def head_add(self,data):
        #生成插入的节点对象
        node = Node(data)
        #进行头插
        node.next = self.head
        #新插入的节点变成了头节点
        self.head = node

    #尾插法
    def tail_add(self,data):
        node = Node(data)
        #找到头节点
        cur = self.head
        #如果头节点是None，尾插等于头叉
        if cur == None:
            self.head_add(data)
        #反之，寻找尾节点
        #cur为啥有cur.next方法：这里就很精髓的展示出了头指针的用处。1.如果是第一个元素的插入，那么使用头指针直接push即可。2.如果不是，头指针直
        #接变成节点结构赋值给cur，便于cur的遍历寻找
        else:
            while cur.next is not None:
                cur = cur.next
            #找到后将其指针指向新加入的节点
            cur.next = node

    #计算链表长度
    def get_length(self):
        length = 0
        cur = self.head
        while cur is not None:
            cur = cur.next
            length += 1
        return length

    #指定位置插入
    def mid_add(self,data,loc):
        try:  
            #如果位置没有问题，进行遍历寻找loc位置
            #如果是末尾，直接调用尾插
            if loc == self.get_length():
                self.tai_add(data)
            #如果是开头，直接调用头插
            elif loc == 1:
                self.head_add(data)
            #其他情况，写上面两个主要是为了处理空链表直接调用mid_add导致cur.next未知
            else:
                cur = self.head
                position = 0
                while position != loc:
                    cur = cur.next
                #找到后进行插入
                node = Node(data)
                cur.next = node
                cur_next = cur.next
                node.next = cur_next
        except:
             #判断位置是否出错
            if loc <= 0 or loc > self.get_length():
                print("位置错误")

    #链表输出
    def walk_through(self):
        cur = self.head
        while cur is not None:
            print(cur.data)
            cur = cur.next

    #删除指定位置的数据,跟指定位置插入一样
    def del_data(self,loc):
        try:
           cur = self.head
           position = 1
           # 判断是否是第一个的位置
           #注意：self.head是对整个类而言的，只要实例化了，self.head就是整个链表的头节点
           if loc == 1:
               self.head = cur.next
               #预防野指针
               cur.next = None
           else:
                #找到当前位置的上一个节点
                while position != loc-1:
                    cur = cur.next
                    position += 1
                cur.next = cur.next.next
        except:
            if loc <= 0 or loc > self.get_length():
                print("位置错误")










