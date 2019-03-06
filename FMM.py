import Point as Pt
import DF as DF
import QuadTree as QT
import random
import Setting as ST
import matplotlib.pyplot as plt
from multipole_framework import Multipole_Framework


"""
multi_level
"""
def distance(a,b):
    return a.p.subtract(b.p).magnitude()

#only sun and moon
def shrink(P,level):
    newP={}
    for p in P.values():
            p.issun=p.ismoon=False
    while True:
        ok=True
        for p in P.values():
            if not p.issun and not p.ismoon:
                ok=False
        if ok:
            break
        while(True):
            sun=random.sample(list(P.values()),1)[0]
            if not sun.issun and not sun.ismoon:
                break
        sun.storemoon[level-1]=sun.moon
        sun.moon=set()
        for m in sun.link:
            if not m.issun and not m.ismoon:
                sun.moon.add(m)
        sun.storem[level-1]=sun.m
        for m in sun.moon:
            sun.m=sun.m+m.m
            m.storeedge[level-1]=m.edge
            m.edge=distance(m,sun)
            m.ismoon=True
        sun.issun=True
        newP[sun.id]=sun
    for s in newP.values():
        s.storeedgeSun[level-1]=s.edgeSun
        s.storelink[level-1]=s.link
        s.edgeSun={}
        s.link=set()
        for anos in newP.values():
            if s is not anos:
                 tot_edge=0
                 time=0
                 for m in s.moon:
                     if anos in m.link:
                         tot_edge=tot_edge+m.edge+distance(m,anos)
                         time=time+1
                     for anom in anos.moon:
                         if anom in m.link:
                            tot_edge=tot_edge+m.edge+anom.edge+distance(anom,anos)
                            time=time+1
                         if s in anom.link:
                             tot_edge=tot_edge+anom.edge+distance(anom,s)
                             timt=time+1
                 if(time!=0):
                     s.link.add(anos)
                     s.edgeSun[anos.id]=tot_edge/time
    return newP

def singlelevel(Points):
    k=0
    while(k<ST.TIME/ST.ITERATIONTIME):
        Tree=QT.tree(QT.Rect(ST.MINX,ST.MAXX,ST.MAXY,ST.MINY))
        Tree.QuadtreeBuild(Points.values())
        Tree.QuadTreeShrink(Tree.root)
        Multipole_Framework(Points,Tree)
        k=k+1

def refine(P,level):
    if level<0:return P
    newP={}
    for s in P.values():
         for m in s.moon:
                tot_pos=Pt.Vector(0,0)
                time=0
                for anos in P.values():
                    if anos.id not in s.edgeSun:
                        continue
                    if anos is s:
                        continue
                    connect=False
                    if anos in m.link:
                         connect=True
                    for anom in anos.moon:
                         if anom in m.link or s in anom.link:
                            connect=True
                    if connect:
                        tot_pos=tot_pos.add(s.p).add(anos.p.subtract(s.p).multiply(m.edge/s.edgeSun[anos.id]))
                        time=time+1
                #半岛地形,选择随机的位置
                if(tot_pos.x==0 and tot_pos.y==0):
                    m.p=s.p.add((Pt.Vector(random.uniform(-1,1),random.uniform(-1,1))))
                else:
                    m.p=tot_pos.divide(time)
                m.check()
                newP[m.id]=m
                m.edge=m.storeedge[level]
    for s in P.values():  
         s.link=s.storelink[level]
         s.edgeSun=s.storeedgeSun[level]
         s.m=s.storem[level]
         s.moon=s.storemoon[level]
    newP.update(P)
    return newP























#入口,提供对应的id, 以及其srcid的列表
def FMMM(id, des):
    #这里改成输入即可，但是还没修改，因为不确定算法正确性， 输入不作为参数
    Points={id[k]:Pt.Point(Pt.Vector(random.uniform(ST.MINX,ST.MAXX),random.uniform(ST.MINY,ST.MAXY)),id[k],des[k]) for k in range(0,len(id))}
    for point in Points.values():
        point.build(Points)
    level=1
    while(level<ST.MAXLEVEL and len(Points)> ST.MINPOINTS):
        Points=shrink(Points,level)
        level=level+1    
    singlelevel(Points)
    level=level-1
    while(level>0):
        Points=refine(Points,level-1)
        singlelevel(Points)
        level=level-1
    #for p in Points.values():
    #    p.p.show()
    for pt in Points.values():
        plt.scatter(pt.p.x,pt.p.y,s=pt.m)
    for pt in Points.values():
        for nb in pt.to:
            ax = plt.axes()
            ax.arrow(pt.p.x,pt.p.y,nb.p.x-pt.p.x,nb.p.y-pt.p.y, fc='k', ec='k',
                     width=0.000001,facecolor="blue",overhang=0.5)
    plt.show()


def main():
    #演示函数
    #构建初始的点
    id=[str(x) for x in range(0,100)]
    des=[random.sample(id,1) for x in range(0,100)]
    FMMM(id,des)
main()