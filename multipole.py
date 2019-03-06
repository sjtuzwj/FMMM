import cmath
import Setting as ST
#组合数公式
def cni(n,i):
    result = 1
    for j in range(1, i+1):
        result = result * (n-i+j) // j
    return result

#多极展开函数
def multi_e(O_ratio,O_centre):
    ratio=O_ratio
    centre=O_centre
    def e(str):
        def getratio():
            return ratio
        def energy(z):
            res=0
            for k in range(1,5):
                res=res+ratio[k]/pow(z-centre,k)
            return res+a[0]*cmath.log(z-centre)
        def derivate(z):
            e=ratio[0]/(z-centre)
            for k in range(1,5):
                e=e-k*ratio[k]/pow(z-centre,k+1)
            return e
        def sum(e2):
            new_ratio=[ratio[i]+e2("ratio")()[i] for i in range(0,5)]
            return multi_e(new_ratio,centre)
        def translation(z1):
            """迁移中心位置"""
            b=[0,0,0,0,0]
            for l in range(1,5):
                b[l]=-ratio[0]*pow(centre-z1,l)/l
                for k in range(1,l+1):
                    tmp=pow(centre-z1,l-k)*cni(l-1,k-1)
                    b[l]=b[l]+ratio[k]*tmp
            return multi_e(b,z1)
        def conversion(z1):
            """转换为局部展开"""
            b=[0,0,0,0,0]
            a=ratio
            z0=centre
            b[0]=a[0]*cmath.log(z1-z0)
            for k in range(1,5):
                b[0]=b[0]+a[k]/pow(z1-z0,k)
            for l in range(1,5):
                b[l]=pow(-1,l+1)*a[0]/pow(z1-z0,l)/l
                tmp=pow(1/(z0-z1),l)
                b[l]=b[l]/tmp
                tmp=0
                for k in range(1,5):
                    tmp=tmp+cni(l+k-1,k-1)*a[k]/pow(z1-z0,k)
                b[l]=b[l]+tmp/(z0-z1)
            return local_e(b,z1)
        map={"ratio":getratio,"energy":energy,"translation":translation,"derivate":derivate,"sum":sum,"conversion":conversion}
        return map[str]
    return e
    

#局部展开函数
def local_e(O_ratio,O_centre):
    #测试成功
    ratio=O_ratio
    centre=O_centre
    def e(str): 
        def getratio():
            return ratio
        def energy(z):
            e=0
            for k in range(0,5):
               e=e+ratio[k]*pow(z-centre,k)
            return e
        def sum(e2):
            new_ratio=[ratio[i]+e2("ratio")()[i] for i in range(0,5)]
            return local_e(new_ratio,centre)
        def derivate(zz):
            """返回局部展开的导数"""
            e=0
            for k in range(1,5):
                e=e+k*ratio[k]*pow(zz-centre,k-1)
            return e
        def translation(z0):
            """迁移中心位置"""
            z1=centre
            for l in range(0,5):
                a={0,0,0,0,0}
                for k in range(l,5):
                    a[k]=a[k]+cni(k,l)*pow(z1-z0,k-1)*ratio[k]
            return local_e(a,z0)
        map={"ratio":getratio,"energy":energy,"translation":translation,"derivate":derivate,"sum":sum}
        return map[str]    
    return e

#计算多极展开
def multipole(nodes,z0):
    a=[0,0,0,0,0]
    for x in nodes:
        a[0]=a[0]+x.m
        for k in range(1,5):
            a[k]=a[k]-x.m*pow(x.p.pos-z0,1)/k
    for x in a:
        x=x*ST.Repusion
    return multi_e(a,z0)

