class sequential_deque:
    def __init__(self):
        self.que = []

    def queue_add(self,val):
        self.que.append(val)

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
            print(self.que)         
        else:
            print("It is an empty queue")

    def clear_que(self):
        self.que = []

    def top_insert(self,val):
        self.que.insert(0,val)

    def rear_insert(self,val):
        self.que.insert(-1,val)

    def top_pop(self):
       return self.que.pop(0)

    def rear_pop(self):
        return self.que.pop(-1)

# test = sequential_deque()
# test.top_insert(1)
# test.top_insert(2)
# test.top_insert(3)
# test.walk_through()
# print(test.top_pop())
# test.walk_through()
# print(test.rear_pop())
# test.walk_through()