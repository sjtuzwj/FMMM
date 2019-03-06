import math
import Setting as ST
class Vector(object):
    """辣鸡python没有移动构造，这开销浪费死了"""
    def __init__(self,x, y):
        self.x = x
        self.y = y
    def show(self):
        print(self.x)
        print(self.y)
    def add(self,v2):
        return Vector(self.x + v2.x, self.y + v2.y)
    def subtract(self,v2): 
        return Vector(self.x - v2.x, self.y - v2.y)
    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    def divide(self,n):
        if(n==0):
            return Vector(0,0)
        else:
            return Vector((self.x / n), (self.y / n))
    def normalise(self):
        return self.divide(self.magnitude())
    def multiply(self,n):
        return Vector(self.x * n, self.y * n)
    @property
    def pos(self):
        """返回坐标的复数表示"""
        return complex(self.x,self.y)

class Point(object):
    #这里是实体的node
    """如名字所说, store目的是multi_level在备份"""
    def __init__(self,position,id,des,mass=1):
        self.issun=False
        self.ismoon=False
        self.storemoon=[set()]*ST.MAXLEVEL
        self.moon=set()
        self.storeedgeSun=[{}]*ST.MAXLEVEL
        self.edgeSun={}
        self.storeedge=[0]*ST.MAXLEVEL
        self.edge=0
        self.p = position
        self.storem=[0]*ST.MAXLEVEL
        self.m = mass
        self.force=Vector(0,0)
        self.v = Vector(0, 0)
        self.id = id
        self.des=des
        self.storelink=[set()]*ST.MAXLEVEL
        self.link=set()
        self.to=set()
    def build(self,S):
        for s in S.values():
            if s.id in self.des and s is not self:
                self.to.add(s)
                self.link.add(s)
                s.link.add(self)
    def updateV(self):
        self.v = self.v.add(self.force.divide(self.m).multiply(ST.ITERATIONTIME)).multiply(ST.DAMP)
    def updateP(self):
        self.p=self.p.add(self.v.multiply(ST.ITERATIONTIME))
        self.check()
    def check(self):
        if(self.v.magnitude()>ST.MAXV):
            self.v=self.v.normalise().multiply(ST.MAXV)
        if self.p.x<ST.MINX:
            self.p.x=ST.MINX+1
        elif self.p.x>ST.MAXX:
            self.p.x=ST.MAXX-1
        if self.p.y<ST.MINY:
            self.p.y=ST.MINY+1
        elif self.p.y>ST.MAXY:
            self.p.y=ST.MAXY-1
