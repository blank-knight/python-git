'''
    当用二叉链表作为二叉树的存储结构时，可以很方便地找到某个结点的左右孩子；
    但一般情况下去，无法直接找到该结点在某种遍历序列中的前驱和后继结点。因此便有了线索二叉树的出现
'''
#ltag = 1时，left指针指向前驱节点，反之，指向左孩子。rtag和right同理，只不过right指向后继节点
#ltag和rtag的目的就是区分指针是指向的孩子节点还是前驱、后继节点
class TreeNode:
    def __init__(self,val) -> None:
        self.val = val
        self.ltag = 0
        self.rtag = 0
        self.left = None
        self.right = None

class clue_binary_tree:
    def __init__(self) -> None:
        self.root = None
        #定义self.pre永远指向当前节点的前一个节点，当当前节点的左右节点为None时，便可用
        #self.pre对其进行线索化
        self.pre = None

    def get_root(self):
        return self.root

    #前序插入完成普通的二叉树
    def pre_order_insert(self,root,lis_val):
        if lis_val[0] != '#':
            root = TreeNode(lis_val[0])
            lis_val.pop(0)
            root.left = self.pre_order_insert(root,lis_val)
            root.right = self.pre_order_insert(root,lis_val)
            self.root = root
            return root
        else:
            root = None
            lis_val.pop(0)
            return root 

    #前序遍历
    def preorder_traversal(self,root):
        if root is None:
            return
        else:
            print(root.val,end=" ")
            #对自身的调用，这里有两种方式，都是可以的
            self.preorder_traversal(root.left)
            self.preorder_traversal(root.right)

    #中序遍历
    def in_order_travaersal(self,root):
        if root is None:
            return
        else:
            #如何写递归代码，由简入繁，递归想太多会想不清楚，就从最简单的一个二叉树入手
            #想象如果只有一个左右节点和一个根节点的二叉树该如何递归来写就行了
            self.in_order_travaersal(root.left)
            print(root.val,end=" ")
            self.in_order_travaersal(root.right)

    #后序遍历
    def post_order_traversal(self,root):
        if root is None:
            return
        else:
            self.post_order_traversal(root.left)
            self.post_order_traversal(root.right)
            print(root.val,end=" ")

    '''
        往左子树递归的过程中，先把node赋值给pre，再进行下一步递归，所以pre一直是node的前节点
    '''
    #普通树变前序线索二叉树
    def pre_clue_binary_tree(self,node):
        if node is not None:
            if node.left is None:
                node.left = self.pre
                node.ltag = 1
            if self.pre is not None and self.pre.right is None:
                self.pre.right = node
                self.pre.rtag = 1
            self.pre = node
            #防止递归原地打转
            if node.ltag == 0:
                self.pre_clue_binary_tree(node.left)
            if node.rtag == 0:
                self.pre_clue_binary_tree(node.right)

    '''
        递归一直走到左下角，然后node赋值给pre，之后返回上一层递归，node变成其父节点
        pre为其左孩子，便完成了中序线索话
    '''
    #将普通二叉树变成中序线索二叉树
    def in_clue_binary_tree(self,node):
        if node is not None:
            self.in_clue_binary_tree(node.left)
            if node.left is None:
                node.left = self.pre
                node.ltag = 1
            if self.pre is not None and self.pre.right is None:
                self.pre.right = node
                self.pre.rtag = 1
            self.pre = node
            self.in_clue_binary_tree(node.right)

    #清楚前驱后继指针，取消线索化
    def clear_clue(self,node):
        if node is not None:
            if node.ltag == 1:
                node.ltag = 0
                node.left = None
            if node.rtag == 1:
                node.rtag = 0
                node.right = None
            self.clear_clue(node.left)
            self.clear_clue(node.right)
        self.pre = None
    '''
        node一直走到左下角，然后赋值给pre，之后node返回上一层递归，之后走右孩子
        此时pre为左孩子，node为右孩子，便可完成后序线索化
    '''
    #普通树变后序线索二叉树
    def post_clue_binary_tree(self,node):
        if node is not None:
            self.post_clue_binary_tree(node.left)
            self.post_clue_binary_tree(node.right)
            if node.left is None:
                node.left = self.pre
                node.ltag = 1
            if self.pre is not None and self.pre.right is None:
                self.pre.right = node
                self.pre.rtag = 1
            self.pre = node 
            
if __name__ == '__main__':
    test = clue_binary_tree()
    lis_vals =  ['A','B','C','#','#','D','E','#','G','#','#','F','#','#','#']
    Root = test.get_root()
    Root = test.pre_order_insert(Root,lis_vals)
    print("---前序遍历为---")
    test.preorder_traversal(Root)
    print("\n")
    print("---中序遍历为---")
    test.in_order_travaersal(Root)
    print("\n")
    print("---后序遍历为---")
    test.post_order_traversal(Root)
    print("\n")

    C = Root.left.left

    print("---按照前序遍历化为线索二叉树,C的后继节点为--")
    test.pre_clue_binary_tree(Root)
    print(C.right.val)

    print("---按照中序遍历化为线索二叉树,C的后继节点为---")
    test.clear_clue(Root)
    test.in_clue_binary_tree(Root)
    print(C.right.val)

    print("---按照后序遍历化为线索二叉树,C的后继节点为---")
    test.clear_clue(Root)
    test.post_clue_binary_tree(Root)
    print(C.right.val)