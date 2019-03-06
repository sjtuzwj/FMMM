import Setting as ST
class Rect(object):
    def __init__(self,left,right,top,bottom):
            self.left=left
            self.right=right
            self.top=top
            self.bot=bottom
            self.midx=(left+right)/2
            self.midy=(top+bottom)/2

class Node(object):
    def __init__(self, rect=0):
        self.trueparent=0
        self.parent=0
        self.E=set()
        self.R=set()
        self.D1=set()
        self.D2=set()
        self.D3=set()
        self.K=set()
        self.I=set()
        self.Sm=self
        self.Lp=0
        self.Mp=0
        self.rect=rect
        self.sub=[0,0,0,0]
        self.points=set()
        self.Flocal=0
        self.Direct=0
        self.Fmulti=0
        self.Ffinal=0
        
LB=0
RB=1
LT=2
RT=3
class tree(object):
    def __init__(self,rect):
        self.leaves=set()
        self.root=Node(rect)
        self.nodes=set()
        self.depth=0 
    def QuadCreateBranch(self, n, depth,rect,pre ):
        if ( depth!=0 ):
            n = Node(rect)
            self.nodes.add(n)
            n.parent=n.trueparent=pre
            rectLB=Rect(rect.left,rect.midx,rect.midy,rect.bot)
            rectRB=Rect(rect.midx,rect.right,rect.midy,rect.bot)
            rectLT=Rect(rect.left,rect.midx,rect.top,rect.midy)
            rectRT=Rect(rect.midx,rect.right,rect.top,rect.midy)
            self.QuadCreateBranch ( n.sub[LB], depth-1, rectLB,n )
            self.QuadCreateBranch ( n.sub[RB], depth-1, rectRB,n )
            self.QuadCreateBranch ( n.sub[LT], depth-1, rectLT,n )
            self.QuadCreateBranch ( n.sub[RT], depth-1, rectRT,n )
    def QuadTreeShrink(self,this):
        #shirnked
        #single node
        if(this.sub.count(0)==3):
            for n in this.sub:
                if n !=0 :
                    this=n
                    break
        #为空节点或叶子节点
        elif(this.sub.count(0)==4):
            if(this.points==set()):
                this=0
            else:
                self.leaves.add(this)
            return
        #对子节点继续递归
        for n in this.sub:
            if n!=0:
                self.QuadTreeShrink(n)
    def QuadTreeBuild ( self,depth, rect ):
        self.depth=depth
        self.QuadCreateBranch (self.root, depth, rect,0)
    def QuadtreeBuild(self,T):
        for t in T:
            self.QuadInsert(t, self.root)
    def QuadInsert(self,i,n):  
        if n.sub !=[0,0,0,0]:
            if n.rect.left<=i.p.x<=n.rect.midx:
                if n.rect.top>=i.p.y>=n.rect.midy:
                    c=LT
                else:
                    c=LB
            elif n.rect.top>=i.p.y>=n.rect.midy: 
                    c=RT
            else:
                    c=RB
            self.QuadInsert(i,n.sub[c])
        elif len(n.points)==ST.MAXSIZE:
            rect=n.rect
            n.sub=[Node(Rect(rect.left,rect.midx,rect.midy,rect.bot)),
                   Node(Rect(rect.midx,rect.right,rect.midy,rect.bot)),
                   Node(Rect(rect.left,rect.midx,rect.top,rect.midy)),
                   Node(Rect(rect.midx,rect.right,rect.top,rect.midy))]
            self.nodes.update(n.sub)
            for sub in n.sub:
                sub.parent=sub.trueparent=n
            n.points.add(i)
            for node in n.points:
                if (n.rect.left<=node.p.x<=n.rect.midx):
                    if(n.rect.top>=node.p.y>=n.rect.midy):
                        c=LT
                    else:
                        c=LB
                elif(n.rect.top>=node.p.y>=n.rect.midy):
                        c=RT
                else:
                        c=RB
                self.QuadInsert(node,n.sub[c])
            n.points=set()
        elif len(n.points)<ST.MAXSIZE:
            n.points.add(i)