import random
import math
from Point import Vector
from DF import Naive_Direct_Force
from DF import Get_Pull_Force
from multipole import local_e
from multipole import multi_e
from multipole import multipole

def isNeighbor(v1,v2):
    #v1 bigger than v2
    if(v1.rect.left-v1.rect.midx<v2.rect.left-v2.rect.midx):
        v1,v2=v2,v1
    if(v1.rect.left==v2.rect.right and v1.rect.bot<=v2.rect.bot and v1.rect.top>=v2.rect.top
       or v1.rect.left==v2.rect.right and v1.rect.bot<=v2.rect.bot and v1.rect.top>=v2.rect.top
       or v1.rect.top==v2.rect.bot and v1.rect.left<=v2.rect.left and v1.rect.right>=v2.rect.right
       or v1.rect.bot==v2.rect.top and v1.rect.left<=v2.rect.left and v1.rect.right>=v2.rect.right):
        return True
    #根据空间位置来算,条件好烦啊,先判断size大小,然后左边界=右边界或上边界=下边界,并且小的边内含于大的边(根据left,bot,top,right)
    return False

def Well_Separated(u,v):
    #提升至等大
    while(u.rect.left-u.rect.midx != v.rect.left-v.rect.midx):
        if(u.rect.left-u.rect.midx>v.rect.left-v.rect.midx):
            v=v.trueparent
        else:
            u=u.trueparent
    if(not isNeighbor(u,v)):
        return True
    else:
        return false

def Calculate_Local_Expansions_and_Node_Sets(T,C,v):
    if not isinstance(v,set):
        return 
    if(v.parent.parent==0):
        v.E=set([v.parent])
    else: 
        v.E=v.parent.R|v.parent.D1 
    while(len(v.E)!=0):
        u=random.sample(list(v.E),1)[0]
        v.E.remove(u)
        if(Well_Separated(u,v)):v.I=v.I|set([u])
        elif(v.Sm.rect.left-v1.Sm.rect.midx>u.Sm.rect.left-v2.Sm.rect.midx):v.R=v.R|set([u])
        elif(v not in T.leaves):v.E=v.E|set(u.sub)
        elif(isNeighbor(u.Sm , v.Sm)):v.D1=v.D1|set([u])
        else: v.D2=v.D2|set(u)
    for u in v.I:
        u.Lp=u.Mp("conversion")(complex(v.rect.midx,v.rect.midy))
        v.Lp=v.Lp("sum")(u.Lp("translation")(complex(v.rect.midx,v.rect.midy)))
    for u in v.D2:
        for c in u.Sm:
            u.Mp=multipole(c.points,complex(c.rect.midx,c.rect.midy))
            c.Lp=c.Mp("conversion")(complex(v.rect.midx,v.rect.midy))
            v.Lp=v.Lp("sum")(c.Lp("translation")(complex(v.rect.midx,v.rect.midy)))
    if(v.parent.Lp!=0):
        v.Lp=v.Lp("sum")(v.parent.Lp("translation")(complex(v.rect.midx,v.rect.midy)))
    if(v in T.leaves):
        v.E=v.R
        while(len(v.E)!=0):
            u=random.sample(v.E,1)
            v.E.remove(u)
            if(not isNeighbor(u.Sm , v.Sm)):
                v.K=v.K|set(u)
            elif(isNeighbor(u.Sm , v.Sm) and u in T.leave):
                v.D3=v.D3|set(u)
            else: 
                v.E=v.E|u.children
    if(v not in T.leaves):
        for w in v.sub:
            Calculate_Local_Expansions_and_Node_Sets(T,C,w)

def Multipole_Framework(C,T):
    for c in C.values():
        c.force=Vector(0,0)
    #Trivial Case and Initializations
    for c in C.values():
        Get_Pull_Force(c,C)
    if(T.root.sub==[0,0,0,0]):
        for c in C.values():
            c.force=c.force.add(Naive_Direct_Force(c,C.values()))
        Iteration(C)
        return
    for v in T.nodes:
        v.R=v.D1=v.I=v.D2=set()
    for v in T.leaves:
        v.K=v.D3=set()
    for v in T.leaves:
        v.Mp=multipole(v.Sm.points,complex(v.rect.midx,v.rect.midy))
    for v in T.nodes:
       if (v not in T.leaves):
           prepare=True
           for w in v.sub:
               if w!= 0 and w.Mp==0:
                   prepare=False
           if (prepare):
               for w in v.sub:
                   if v.Mp==0 and w!=0:
                       v.Mp=w.Mp
                   elif w!=0:
                       tmp=w.Mp("translation")(complex(v.rect.midx,v.rect.midy))
                       v.Mp=v.Mp("sum")(tmp)
    for v in T.root.sub:
            Calculate_Local_Expansions_and_Node_Sets(T,C,v)
    for v in T.leaves:
        v.C=v.Sm
        if v.Lp!=0:
            v.Flocal=v.Lp("derivate")
        for p in v.points:
            ls=set()
            for v1 in v.D1|v.D3|set([v.C]):
                ls.update(v1.points)
            p.force=p.force.add(Naive_Direct_Force(p,ls))
        v.Fmulti=sum_Force([x.points.Mp("derivate") for x in v.K if BaseException.points.Mp!=0])
        v.Ffinal=sum_Force([v.Flocal,v.Fmulti])
        for c in v.C.points:
            F=v.Ffinal(c.p.pos)
            c.force=c.force.add(Vector(F.real,F.imag))
    Iteration(C)

def Iteration(C):
    """根据所求的力改变各点状态"""
    for c in C.values():
        c.updateV()
        c.updateP()

def sum_Force(Fs):
    """对一组力进行加和并返回和函数"""
    def F_sum(z):
        F=0
        for x in Fs:
            if x!=0:
                F=F+x(z)
        return F
    return F_sum
