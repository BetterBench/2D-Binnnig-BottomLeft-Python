from tools import *
import random

#   BL（bottom-up left-justified）法求解二位装箱问题
#   @BetterBench
#   思想：首先将选中的物体放在箱子的右上角，然后尽量向下向左作连续移动，直到不能移动为止
# 输入参数
itemNum=10 #物品数目
AllItem=np.array([[random.randint(1, 5) for j in range(1, 3)] for i in range(1,itemNum+1)])  #随机生成30个物品
Bin=[5,5] #箱子宽度与高度
ran=list(range(itemNum))
random.shuffle(ran) #随机生成装箱序列

ansBXY=np.zeros((itemNum,3))  #[箱子编号，X坐标，Y坐标]
RPNXY=[];
BinNum=1;
flagItem=np.zeros(itemNum) #标记物品是否被装入箱子，0没有装入，1装入
# 开始装箱

for i in range(itemNum):
    if flagItem[ran[i]]==0:
        item=AllItem[ran[i],:]
        itemRP=Bin  #起点全部在箱子右上角顶点
        flagOL=overlap(item,AllItem,itemRP,RPNXY) #如果重合flagOL=1；反之flagOL=0
        if flagOL==0:
            itemRP=finalPos(item,AllItem,itemRP,RPNXY) #更新物品从当前位置向下向左移动后到最终位置后右上角顶点坐标
            print(itemRP)
            if len(itemRP)>0:
                RPNXY.append([ran[i],itemRP[0],itemRP[1]])
                flagItem[ran[i]]=1
print()