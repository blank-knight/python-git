class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Tree:
    def __init__(self) -> None:
        self.root = None
        self.num = 0
        
    #用队列进行层序插入树
    def seq_insert_elem(self,lis_val):
        for i in lis_val:
            node = TreeNode(i)
            if self.root is None:
                self.root = node
                continue
            #通过队列，实现层序插入。因为tree_queue的第一个元素总是self.root，所以每次插入都是从self.root开始遍历检查的
            tree_queue = [self.root]
            #当队列里的元素使用完毕，自动会退出while循环
            while True:
                parent_node = tree_queue.pop(0)
                #从左往右判断并进行插入。如果左子树为None,将其加入左子树。否则将其入队，等待右子树的判断然后加入右子树
                if parent_node.left is None:
                    parent_node.left = node
                    #break跳出while循环进入for的列表循环
                    break
                else:
                    tree_queue.append(parent_node.left)

                #如果右子树为None，将其加入右子树
                if parent_node.right is None:
                    parent_node.right = node
                    break
                else:
                    tree_queue.append(parent_node.right)
        return self.root

    # 递归完成前序插入树       
    def pre_insert_elem(self,root,lis_val):
        if lis_val[0]!='#':
            root = TreeNode(lis_val[0])
            lis_val.pop(0)
            #self.root.left变成self.root本身,进行递归传递，先左子树，后右子树
            root.left = self.pre_insert_elem(root.left,lis_val)
            root.right = self.pre_insert_elem(root.right,lis_val)
            #如何看递归代码：不要进入递归栈去看，看最外层，你就想这里，root是啥，是TreeNode(lis_val[0])，也就是lis_val里的A
            #所以不管内部是怎么递归黑盒，最外层的这里，返回的永远是A节点。而下面外层的else全都是在递归里面进行的，不算是最外层
            #所以不会影响这里root的值
            self.root = root
            return root#本次递归要返回给上一次的本层构造好的树的根节点。
        else:
            #当走到'#'的地方时，self.root设为None并进行返回
            root=None
            lis_val.pop(0)
            return root#返回的root会赋值给root.left或者root.right

    def get_root(self):
        return self.root
    
    def preorder_traversal(self,root):
        if root is None:
            return
        else:
            print(root.val,end=" ")
            #对自身的调用，这里有两种方式，都是可以的
            self.preorder_traversal(root.left)
            Tree.preorder_traversal(self,root.right)
    
    def in_order_travaersal(self,root):
        if root is None:
            return
        else:
            #如何写递归代码，由简入繁，递归想太多会想不清楚，就从最简单的一个二叉树入手
            #想象如果只有一个左右节点和一个根节点的二叉树该如何递归来写就行了
            self.in_order_travaersal(root.left)
            print(root.val,end=" ")
            self.in_order_travaersal(root.right)
    
    def post_order_traversal(self,root):
        if root is None:
            return
        else:
            self.post_order_traversal(root.left)
            self.post_order_traversal(root.right)
            print(root.val,end=" ")
    '''
        1、申请一个栈stack，然后将头节点压入stack中。
        2、从stack中弹出栈顶节点，打印，再将其右孩子节点（不为空的话）先压入stack中，最后将其左孩子节点（不为空的话）压入stack中。
        3、不断重复步骤2，直到stack为空，全部过程结束。
    '''
    def stack_pre_traversal(self):
        stack = [self.root]
        while stack != []:
            cur_node = stack.pop(-1)
            if cur_node is not None:
                print(cur_node.val,end=" ")
                if cur_node.right is not None:
                    stack.append(cur_node.right)
                if cur_node.left is not None:
                    stack.append(cur_node.left)
    '''
        1、申请一个栈stack，初始时令cur=head
        2、先把cur压入栈中，依次把左边界压入栈中，即不停的令cur=cur.left，重复步骤2
        3、不断重复2，直到为null，从stack中弹出一个节点，记为node，打印node的值，并令cur=node.right,注意，不要将其入栈。重复步骤2
        4、当stack为空且cur为空时，整个过程停止。
    '''      
    def stack_in_order_traversal(self):
        stack = []
        cur_node = self.root
        while stack != [] or cur_node is not None:
            if cur_node is not None:
                stack.append(cur_node)
                cur_node = stack[-1].left
            else:
                node = stack.pop(-1)
                print(node.val,end=" ")
                cur_node = node.right
                
    ''' 
        1、申请一个栈s1，然后将头节点压入栈s1中。
        2、从s1中弹出的节点记为cur，然后依次将cur的左孩子节点和右孩子节点压入s1中。
        3、在整个过程中，每一个从s1中弹出的节点都放进s2中。
        4、不断重复步骤2和步骤3，直到s1为空，过程停止。
        5、从s2中依次弹出节点并打印，打印的顺序就是后序遍历的顺序。
    '''
    def stack_post_order_traversal(self):
        stack_1 = [self.root]
        stack_2 = []
        while stack_1 != []:
            cur_node = stack_1.pop(-1)
            stack_2.append(cur_node)
            if cur_node.left is not None:
                stack_1.append(cur_node.left)
            if cur_node.right is not None:
                stack_1.append(cur_node.right)
        for i in stack_2[::-1]:
            print(i.val,end=" ")

    '''
    （1）如果一颗树只有一个结点，它的深度是 1；
    （2）如果根结点只有左子树而没有右子树，那么二叉树的深度应该是其左子树的深度加 1；
    （3）如果根结点只有右子树而没有左子树，那么二叉树的深度应该是其右树的深度加 1；
    （4）如果根结点既有左子树又有右子树，那么二叉树的深度应该是其左右子树的深度较大值加 1。
    '''     
    def get_tree_depth(self,root):
        #这里要return 0,返回深度，不要直接return
        if root is None:
            return 0
        else:
            l_length = self.get_tree_depth(root.left)
            r_length = self.get_tree_depth(root.right)
        if l_length > r_length:
            return l_length+1
        else:
            return r_length+1

    #二叉树的复制
    def copy_tree(self,root):
        if root is None:
            return None
        else:
            #节点的创建复制，和左右子树递归复制
            new_node = TreeNode(root.val)
            new_node.left = self.copy_tree(root.left)
            new_node.right = self.copy_tree(root.right)
        return new_node

    '''
        随便使用一种遍历方式，把里面不是None的节点统计下来即可
    '''
    def num_of_nodes(self,root):
        if root is None:
            return
        else:
            self.num += 1
            #对自身的调用，这里有两种方式，都是可以的
            self.num_of_nodes(root.left)
            Tree.num_of_nodes(self,root.right)
        return self.num

    # 判断是否是二叉搜索树
    '''
        1
    2       3

        1
    2       5
        3       4       
    '''
    def isValidBST(self, root):
        """
        :type root: TreeNode
        :rtype: boo
        """
        if root is None:
            return
        self.isValidBST(root.left)
        if root.left is not None and root > root.left and root.right > root:
            self.isValidBST(root.right)
        else:
            return False
        return True

    '''
    判断树是否对称
    '''
    def isSymmetric(self, root):
        def jug(left,right):
            # 判断左右是否同时为空
            if left is None and right is None:
                return True
            # 若不同时为空，则不对称
            elif left is None or right is None:
                return False
            # 判断左右值是否相同
            elif left.val != right.val:
                return False
            # 进行对称递归
            return jug(left.left,right.right) and jug(left.right,right.left)
        # 进行调用
        return jug(root.left,root.right)

     # 完成BFS遍历
    def BFS_traversal(self,root):
        queue = []
        res = []
        queue.append(root)
        while queue != []:
            cur_node = queue.pop(0)
            res.append(cur_node.val)
            if cur_node.left is not None:
                queue.append(cur_node.left)
            if cur_node.right is not None:
                queue.append(cur_node.right)
        return res

    # 完成层序遍历
    def levelOrder(self, root):
        queue = []
        res = []
        queue.append(root)
        if root is None:
            return []
        while queue != []:
            n = len(queue)
            i = 0
            lis = []
            # 用一个参数i来记录每层到底有多少个元素，从而从BFS变到层序遍历
            while i < n:
                cur_node = queue.pop(0)
                lis.append(cur_node.val)
                if cur_node.left is not None:
                    queue.append(cur_node.left)
                if cur_node.right is not None:
                    queue.append(cur_node.right)
                i += 1
            res.append(lis)
        return res

    # 将数组转换为平衡搜索二叉树
    def sortedArrayToBST(self, nums):
        """
        :type nums: List[int]
        :rtype: TreeNode
        """
        if nums == []:
            return
        length = len(nums)
        mid = length//2
        root = TreeNode(nums[mid])
        root.left = self.sortedArrayToBST(nums[0:mid])
        root.right = self.sortedArrayToBST(nums[mid+1::])
        return root

if __name__ == '__main__':
    test = Tree()
    lis_vals =  ['A','B','C','#','#','D','E','#','G','#','#','F','#','#','#']

    Root = test.seq_insert_elem(lis_vals)
    print("---层序插入的递归前序遍历---\n")
    test.preorder_traversal(Root)
    print('\n')

    lis_vals =  ['A','B','C','#','#','D','E','#','G','#','#','F','#','#','#']
    print("---前序插入的递归前序遍历---\n")
    Root = test.pre_insert_elem(None,lis_vals)
    test.preorder_traversal(Root)
    print('\n')
    print("---前序插入的递归中序遍历---\n")
    test.in_order_travaersal(Root)
    print('\n')
    print("---前序插入的递归后序遍历---\n")
    test.post_order_traversal(Root)
    print('\n')
    #因为列表是可变类型，函数里面对其进行了修改，其全局变量也会被修改
    
    print("---使用栈非递归的方式实现二叉树前序遍历---")
    test.stack_pre_traversal()
    print('\n')

    print("---使用栈非递归的方式实现二叉树中序遍历---")
    test.stack_in_order_traversal()
    print('\n')

    print("---使用栈非递归的方式实现二叉树后序遍历---")
    test.stack_post_order_traversal()
    print('\n')

    print("---获取树的深度---")
    print(test.get_tree_depth(Root))

    print("---复制树后的前序遍历---")
    Root_copy = test.copy_tree(Root)
    test.preorder_traversal(Root_copy)
    print("\n")

    print("---树的节点数---")
    print(test.num_of_nodes(Root))