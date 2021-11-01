class Node:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
        
class Tree:
    #只在一开始实例化时调用一次
    def __init__(self):
        self.root = None

    def add_element(self,node_value):
        node = Node(node_value)
        #如果root为None。将其初始化为node类型。之后self.root的类型就都是node了，所以后面可以调用left等方法
        if self.root is None:
            self.root = node
            #return后面如果不加参数表示结束程序
            return
        queue = [self.root]
        #从根节点开始遍历，然后添加字节点元素。如果是空，直接插入，然后return结束。
        # 如果非空，将其左节点入队，然后出队进行下一轮检查、遍历和添加元素。右节点同理
        while True:
            pop_node = queue.pop(0)
            if pop_node.left is None:
                pop_node.left = node
                return
            else:
                queue.append(pop_node.left)

            if pop_node.right is None:
                pop_node.right = node
                return
            else:
                queue.append(pop_node.right)
    
    def bfs(self):
        if self.root is None:
            return
        queue = [self.root]
        while queue:
            pop_node = queue.pop(0)
            print(pop_node.val,end=" ")
            if pop_node.left is not None:
                queue.append(pop_node.left)
            if pop_node.right is not None:
                queue.append(pop_node.right)

tree = Tree()
tree.add_element(1)
tree.add_element(2)
tree.add_element(3)
tree.add_element(4)
tree.add_element(5)
tree.add_element(6)
tree.bfs()