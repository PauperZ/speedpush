import time
import json
import os
import random

daynum = 6               #每日测速的订阅数量
lsA = []
lsB = []
lsC = []
lsD = []
baseA = 2                #A、B、C三组的基本个数，总个数 = 基本个数 + 随机个数（随机个数作用是贴合比例，基本个数保证每日必测某组固定数量订阅）
baseB = 1
baseC = 1
rateA = (4/10 - baseA / daynum) * daynum             #各组的随机率，用于按此比例随机生成随机个数订阅
rateB = (3/10 - baseB / daynum) * daynum
rateC = (2/10 - baseC / daynum) * daynum
rateD = 1/10 * daynum
numspeed = ['0','0','0','0']

def getnum(group):   #函数：按行数获取测速文件中机场的个数,并将机场数据读入列表                  
    count = 0
    with open(group,'rb') as groupname:
        for line in groupname:
            count += 1
            if group[0] == 'A':
                lsA.append(line)
            elif group[0] == 'B':
                lsB.append(line)
            elif group[0] == 'C':
                lsC.append(line)
            else:
                lsD.append(line)                
        return count

def getlist(ls,group,lsnum,num = 1):    #函数：用于生成ls组(第group组)的num个机场并保存在测速文件内，lsnum为本组订阅个数，用getnum获取
    i = 0
    target = 0
    numgroup = [0,0,0,0]
    with open('speednum by group.txt','r+',encoding="utf-8") as speednum:             #在speednum by group文件中获取每组当前测速的首组序，并更新下次测速的首组序
        for line in speednum:                                                         #获取组序并保存，便于对应输出测速订阅
            t = int(line[0:-1])
            numgroup[i] = t
            i += 1
            if group == i:
                if numgroup[i-1] + num <= lsnum - 1:
                    numspeed[i-1] = str(numgroup[i-1] + num)
                    result = numgroup[i-1] + num
                else:
                    numspeed[i-1] = str(numgroup[i-1] + num - lsnum)
                    result = numgroup[i-1] + num - lsnum
                target = int(numgroup[i-1])
            else:
                numspeed[i-1] = line[0:-1]
        speednum.close()
        os.remove("speednum by group.txt")                       
        with open('speednum by group.txt','w+',encoding="utf-8") as speednum:
            for i in range(4):
                speednum.write(numspeed[i] + '\n')     
        speednum.close()
        daytime = time.strftime("%Y-%m-%d",time.localtime())
        with open("今日测速 {}.txt".format(daytime),'a') as speedls:                 #获取对应组序的订阅保存在测速文件内
            if target + num <= lsnum:
                for i in range(num):
                    if i + target == lsnum - 1:
                        speedls.write(ls[i + target][0:].decode('utf-8'))
                        speedls.write('\n')
                    else:
                        speedls.write(ls[i + target][:-1].decode('utf-8'))
            else:
                for i in range(lsnum -num + result,lsnum):
                    speedls.write(ls[i][0:].decode('utf-8'))
                    if i == lsnum - 1:
                        speedls.write('\n')
                for i in range(0,result):
                    speedls.write(ls[i][:-1].decode('utf-8'))
            speedls.close()        
    
numA = getnum('A.txt')         #求各组文件中机场个数
numB = getnum('B.txt')
numC = getnum('C.txt')
numD = getnum('D.txt')

getlist(lsA,1,numA,baseA)      #输出基本测速订阅到文件
getlist(lsB,2,numB,baseB)
getlist(lsC,3,numC,baseC)
for i in range(daynum - baseA - baseB - baseC):                #输出随机测速订阅到文件，采用系统时间随机数取法
    t = random.uniform(0,daynum - baseA - baseB - baseC)
    if t <= rateA:
        getlist(lsA,1,numA)
    elif t <= rateA + rateB:
        getlist(lsB,2,numB)
    elif t <= rateA + rateB + rateC:
        getlist(lsC,3,numC)
    else:
        getlist(lsD,4,numD)
