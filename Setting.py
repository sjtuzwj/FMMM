#存在bug：栈溢出
#出现情景：时间间隔大或者力比较大，造成v很大
#怀疑是越界之后无法assign给正确的节点导致不断递归，但是没找到哪里越界了，按理来说做了边界检查
#斥力 F=k/x^2
Repusion=1
#力的最大值，防止过大的力
MAXFORCE=100
#力的最大值，防止过大的速度
MAXV=100
#引力系数 F=kx， 设太小了容易被弹开…… 理论上距离应该在1，已经算很大了……不知道怎么再调
Stiffness=1
#向心系数 F=kr向心
Tocentre=0.03
#阻尼系数 v'=kv
DAMP=0.8
#Multilevel停止时节点最小数 
MINPOINTS=5
#Multilevel最大级别
MAXLEVEL=5
#Multipole bucket 容量
MAXSIZE=10
#总迭代秒数
TIME=100
#每次迭代时间，不知道为啥大了容易报错,是移动除了边界么
ITERATIONTIME=0.1
#边界
MINX=0
MINY=0
MAXX=1024
MAXY=1024
