from Point import Vector
from Point import Point
import Setting as ST
Centre=Vector((ST.MAXX-ST.MINX)/2,(ST.MAXY-ST.MINY)/2)

#引力
def Get_Pull_Force(v,V):
    F=Vector(0,0)
    for u in v.link:
        r=u.p.subtract(v.p)
        F=r.multiply(ST.Stiffness*0.5)#为了便于multilevel，实际计算时采取双向关系，画图时采取单向关系, 否则无法确定shrink后的方向
        u.force=u.force.add(F.multiply(-1))
        v.force=v.force.add(F)

#斥力
def Naive_Direct_Force(v,V):
    Fsum=Vector(0,0)
    for u in V:
        F1=Vector(0,0)
        if(u is not v):
            r=v.p.subtract(u.p)
            if r.magnitude() !=0:
                F1=r.multiply(ST.Repusion*v.m*u.m/r.magnitude()/r.magnitude()/r.magnitude())
        Fsum=Fsum.add(F1)
    rc=Centre.subtract(v.p)
    F2=rc.multiply(ST.Tocentre)
    Fsum=Fsum.add(F2)
    if(Fsum.magnitude()>ST.MAXFORCE):
        Fsum=Fsum.normalise().multiply(ST.MAXFORCE)
    return Fsum

