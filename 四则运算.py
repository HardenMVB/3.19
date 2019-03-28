import random
import operator
import argparse
import time
from fractions import Fraction

j,k=0,0
start =time.clock()     #用于计算运行时间


def get_Parameter():#命令行控制模块
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', help='设定题目数量',type=int)
    parser.add_argument('-r', help='设定数值范围',type=int)
    return parser.parse_args()

def get_num_sym(i,r):#获取数值列表和符号列表
    nlist=[]            #数值列表
    slist=[]            #符号列表
    kh=0                #判断怎么加括号
    jian=0                 #判断是否是减数运算
    for m in range(i+1):         #根据i的值遍历输出数值列表
        nlist.append(Fraction(random.randint(1, r), random.randint(1, r)))  
    for x in range(i):
        sy=random.choice(['+','-','×','÷'])
        if sy=='+'or sy=='-':
            kh +=10**(i-x-1)
        else :
            kh += 2 * (10 ** (i - x - 1))
        slist.append(sy)
        if sy=='-':
            l=1
    return nlist,slist,kh,i,jian

def fens(f):#分数的转换
    a=f.numerator
    b=f.denominator
    if a%b==0:         #为整数
        return '%d'%(a/b)
    elif a<b:          #为真分数
        return '%d%s%d' % (a,'/',b)
    else:              #为带分数
        c=int(a/b)
        a = a - c * b
        return '%d%s%d%s%d' % (c,'’',a,'/',b)
   
def calculate(a,b,s):#计算单元，a，b是数，s是符号
    ans=0
    if s=='+':        #加法运算
        ans=a+b
    elif s=='-':      #减法运算
        a,b=max(a,b),min(a,b)     #防止结果为负数
        ans=a-b
    elif s=='×':      #乘法运算
        ans=a*b
    else:ans=a/b      #除法运算
    return ans

def writet(slist,num,kh):#生成算术表达式
    global j,k
    s=''
    if kh>100:            #符号数为3
        if j==1 and k==0:
            s = '%s %s (%s %s %s) %s %s = ' % (fens(num[0]), slist[0],
            fens(num[1]),slist[1], fens(num[2]), slist[2], fens(num[3]))
        elif j==1 and k==1:
            s = '%s %s (%s %s (%s %s %s)) = ' % (fens(num[0]), slist[0],
            fens(num[1]),slist[1], fens(num[2]), slist[2], fens(num[3]))
        elif j==0 and k==1:
            s = '%s %s (%s %s %s %s %s) = ' % (fens(num[0]), slist[0],
            fens(num[1]),slist[1], fens(num[2]), slist[2], fens(num[3]))
        if kh == 112 or kh ==212:          
            s = '(%s %s %s %s %s) %s %s = ' % (fens(num[0]), slist[0],
            fens(num[1]),slist[1], fens(num[2]), slist[2], fens(num[3]))
        elif kh == 121 or kh ==122:
            s = '(%s %s %s) %s %s %s %s = ' % (fens(num[0]), slist[0],
            fens(num[1]),slist[1], fens(num[2]), slist[2], fens(num[3]))
        else:
            s = '%s %s %s %s %s %s %s = ' % (fens(num[0]), slist[0],
            fens(num[1]),slist[1], fens(num[2]), slist[2], fens(num[3]))
    elif kh>10:          #符号数为2
        if j==1 :
            s = '%s %s (%s %s %s) = ' % (fens(num[0]), slist[0],
            fens(num[1]), slist[1], fens(num[2]))
        if kh == 12:
            s = '(%s %s %s)%s %s = ' % (fens(num[0]), slist[0],
            fens(num[1]), slist[1], fens(num[2]))
        else:
            s = '%s %s %s %s %s = ' % (fens(num[0]), slist[0],
            fens(num[1]), slist[1], fens(num[2]))
    else :         #符号数为1
        s ='%s %s %s = ' % (fens(num[0]),slist[0],fens(num[1]))
    return s

def gett(n,r):         #用于生成题目和答案列表
    E,A,E1,E2=[],[],[],[]
    global j,k
    x=1
    while x<n+1:       #循环生成题目和答案列表
        i=random.randint(1, 3)       #随机获取符号数目
        num,slist,kh,i,jian=get_num_sym(i,r)
        num1=num
        legal = True
        if jian==1:         #用于防止减法运算出现负数           
            if  num[0]<num[1]:
                num1[0],num1[1]=num[1],num[0]
            if i>=2 and calculate(num[0],num[1],slist[0])<num[2]:
                num1[0],num1[1],num1[2]=num[2],num[0],num[1]
                j=1
            if i>=3 and calculate(calculate(num[0],num[1],slist[0]),num[2],slist[1])<num[3]:
                num1[0],num1[1],num1[2],num1[3]=num[3],num[0],num[1],num[2]
                k=1        
        ans=num1[0]
        for y in range(i):
            cal=calculate(ans,num[y+1],slist[y])
            if cal>=0:
                ans=cal
            else:
                legal=False
                break
        if legal:              #判断算式是否重复
            try:
                num=A.index(ans) #第一个答案的索引

            except ValueError as e:     #可以写入
                A.append(ans)
                E1.append(slist)
                E2.append(num1)
                E.append('%d. %s'%(x,writet(slist,num1,kh)))
                x+=1
        else:pass
    return E,A

def savet(fname, d):#fname为写入文件的路径，d为要写入的数据列表
    file = open(fname,'a')
    file.seek(0)
    file.truncate() #清空
    for i in range(len(d)):#循环写入文件fname
        s = str(d[i]).replace('[','').replace(']','')
        s = s.replace("'",'').replace(',','') +'\n'
        file.write(s)
                  
    file.close()
    print('%s文件已保存'%fname)

def main():#主函数
    args = get_Parameter()
    if args.n:
        n=args.n
        print('共生成%d道题目'%n)
    if args.r:
        r=args.r
        print('均为%d以内的四则运算'%r)
        E, A=gett(n,r)
        for x in range(n):#循环生成答案列表
            A[x]='%d. %s'%(x+1,fens(A[x]))
        savet('Exercises.txt',E)
        savet('Answers.txt',A)

    end = time.clock()
    print('运行时间: %s '%(end-start))
    
if __name__ == '__main__':
    main()
    
