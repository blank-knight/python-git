class sequential_stack:
    def __init__(self):
        self.stack = []
    
    def jug_empty(self):
        if self.stack:
            return 1
        else:
            return 0

    def get_top_elem(self):
        return self.stack[-1]

    def get_length(self):
        return len(self.stack)

    def push(self,val):
        self.stack.append(val)

    def pop(self):
        return self.stack.pop()

    def clear_stack(self):
        self.stack = []

    def walk_through(self):
        for i in range(len(self.stack)-1,-1,-1):
            print(self.stack[i],end="")
            
