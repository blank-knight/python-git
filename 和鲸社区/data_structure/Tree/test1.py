class TreeNode():#二叉树节点
    def __init__(self,val,lchild=None,rchild=None):
        self.val=val		#二叉树的节点值
        self.lchild=lchild		#左孩子
        self.rchild=rchild		#右孩子

def Creat_Tree(Root,val):
    #这里的vals是外面的全局变量
    if len(vals)==0:#终止条件：val用完了
        return Root
    if vals[0]!='#':#本层需要干的就是构建Root、Root.lchild、Root.rchild三个节点。
        Root = TreeNode(vals[0])
        vals.pop(0)
        #Root.lchild变成Root本身进行传递
        Root.lchild = Creat_Tree(Root.lchild,val)
        Root.rchild = Creat_Tree(Root.rchild,val)
        return Root#本次递归要返回给上一次的本层构造好的树的根节点
    else:
        Root=None
        vals.pop(0)
        return Root#本次递归要返回给上一次的本层构造好的树的根节点

def preorder_traversal(root):
        if root is None:
            return
        else:
            print(root.val,end=" ")
            #对自身的调用，这里有两种方式，都是可以的
            preorder_traversal(root.lchild)
            preorder_traversal(root.rchild)

#这里写if __name__=='__main__'的目的是为了自己在模块内的测试，当别的模块调用此模块时，不会调用这里的代码。
#给别人提供一些便利，为了不让别人一导入你的模块就直接运行整个脚本那么使用
if __name__ == '__main__':
    Root = None
    strs="abc##d##e##"#前序遍历扩展的二叉树序列
    vals = list(strs)
    Roots=Creat_Tree(Root,vals)#Roots就是我们要的二叉树的根节点。
    preorder_traversal(Roots)