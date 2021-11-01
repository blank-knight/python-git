#定义顶点类
class Vertex:
    #顶点结构由当前顶点值（键）与跟其相连边构成
    def __init__(self,key) -> None:
        self.id = key
        self.connectedTo = {}

    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight

    """__str__魔法方法，返回一个对象的描述信息"""
    #查看当前顶点与其相连的边
    def __str__(self) -> str:
        print(x.id for x in self.connectedTo)
        return str(self.id)+'connectedTo:'+str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self,nbr):
        return self.connectedTo[nbr]

#定义图类
class Graph:
    def __init__(self) -> None:
        self.vertList = {}
        self.numVertices = 0

    #添加顶点到verList里面去
    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    #判断键是否在vertList里面
    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    #判断n是否在类里面,可以,a = Graph(),print('b' in a)，这样写来看
    def __contains__(self,n):
        return n in self.vertList

    #添加有向权重边。若顶点不存在，则先添加
    #若顶点存在，则调用顶点类方法
    def addEdge(self,f_Vert,t_Vert,weight=0):
        if f_Vert not in self.vertList:
            nv = self.addVertex(f_Vert)
        if t_Vert not in self.vertList:
            nv = self.addVertex(t_Vert)
        self.vertList[f_Vert].addNeighbor(self.vertList[t_Vert],weight)

    def getVertices(self):
        return self.vertList.keys()

    #生成迭代对象，必须是对象自己的属性，只在实例化x时调用一次，这里就是将
    # sel.verList.values()变成一个可迭代对象
    #通常还会定义一个__next__魔法方法，之后遍历调用实例对象都会调用此方法
    def __iter__(self):
      return iter(self.vertList.values())
        
    
g = Graph()
for i in range(6):
    g.addVertex(i)
print(g.vertList)

