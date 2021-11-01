class TreeNode(object):#创建线索链表的结点
    def __init__(self,val=None):
        self.val = val
        self.left = None
        self.right = None
        """
        在树结点的基础上增加类型指针
        如果left_type==0 表示指向该结点的左孩子;如果是1，则表示指向该结点的前驱结点
        如果right_type==0 表示指向该结点的右孩子;如果是1，则表示指向该结点的后继结点
        初始化每个结点的左右标志left_type、right_type为0
        """
        self.left_type = 0
        self.right_type = 0

class ThreadedBinaryTree(object):  # 创建中序线索二叉树
    def __init__(self):
        self.root=None
        # 在递归进行线索化，总是保留前一个结点

        self.pre = None  # 为实现线索化，需要创建给指向当前结点的前驱结点指针

    # 中序线索二叉树结点
    def threaded_node(self, node):  # node:就是当前需要线索化的结点
        if node is None:
            return
        # 先线索化左子树
        self.threaded_node(node.left)

        # 线索化当前结点，处理当前结点的前驱结点
        if node.left is None:  # 如果当前结点没有左孩子即左子结点为空
            node.left = self.pre  # 让当前结点的左指针指向前驱结点
            node.left_type = 1  # 修改当前结点的左指针类型为1

        # 处理当前结点的后继结点
        if self.pre and self.pre.right is None:
            self.pre.right = node  # 让前驱结点的右指针指向当前指针
            self.pre.right_type = 1  # 修改前驱结点的右指针类型为1
        self.pre = node  # 每处理一个结点后，保证当前结点是下一个结点的前驱结点

        # 线索化右子树
        self.threaded_node(node.right)

    # 中序遍历测试
    def inorder(self,node):
        """用递归实现中序遍历"""
        if node is None:
            return
        self.inorder(node.left)
        print(node.val, end=" ")
        self.inorder(node.right)
if __name__ == '__main__':
   # 验证中序线索化是否成功
   # 手动创建一个二叉树
   t=ThreadedBinaryTree()
   t1 = TreeNode(2)
   t2 = TreeNode(3)
   t3 = TreeNode(6)
   t4 = TreeNode(8)
   t5 = TreeNode(10)
  
   t1.left = t2
   t1.right = t3
   t2.left = t4
   t2.right = t5
  
   print("原来的二叉树中序遍历为：")
   t.inorder(t1)
   # 线索化二叉树
   t.threaded_node(t1)
   # 测试：以值为10 的结点来测试
   left_node = t5.left
   print()
   print("10 的前驱结点是：%d" % left_node.val)  
   right_node = t5.right
   print("10 的后继结点是：%d" % right_node.val)