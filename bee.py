import numpy as np
import random, math, copy
import matplotlib.pyplot as plt
from tools import *
import random
 

def fitness(Bin,AllItem,ran):
    # ran 是装箱顺序
    itemNum=AllItem.shape[0] #物品数目
    RPNXY=[];
    flagItem=np.zeros(itemNum) #标记物品是否被装入箱子，0没有装入，1装入
    # 开始装箱

    for i in range(itemNum):
        if flagItem[ran[i]]==0:
            item=AllItem[ran[i],:]
            itemRP=Bin  #起点全部在箱子右上角顶点
            flagOL=overlap(item,AllItem,itemRP,RPNXY) #如果重合flagOL=1；反之flagOL=0
            if flagOL==0:
                itemRP=finalPos(item,AllItem,itemRP,RPNXY) #更新物品从当前位置向下向左移动后到最终位置后右上角顶点坐标
                if len(itemRP)>0:
                    RPNXY.append([ran[i],itemRP[0],itemRP[1]])
                    flagItem[ran[i]]=1
    rect_area = 0
    bin_area = Bin[0]*Bin[1]
    for id in RPNXY:
        width,height = AllItem[id[0]]
        rect_area += width*height
    score = rect_area/bin_area
    print('利用率:{}'.format(score))
    return score
 
class ABSIndividual:
    def __init__(self,bin,item):
        self.score = 0.
        self.invalidCount = 0                      #无效次数（成绩没有更新的累积次数）
        self.bin = bin  #箱子宽度与高度
        self.allitem = item
        self.ran =  list(range(self.allitem.shape[0]))# 装箱顺序
        self.calculateFitness()        
 
    def calculateFitness(self):
        self.score = fitness(self.bin,self.allitem,self.ran)          #计算当前成绩
        
class ArtificialBeeSwarm:
    def __init__(self, foodCount, onlookerCount,Bin, item, maxIterCount=1000, maxInvalidCount=200):
        self.foodCount = foodCount                  #蜜源个数，等同于雇佣蜂数目
        self.onlookerCount = onlookerCount          #观察蜂个数 
        self.item = item                          #各参数上下界
        self.maxIterCount = maxIterCount            #迭代次数
        self.maxInvalidCount = maxInvalidCount      #最大无效次数
        self.Bin = Bin
        self.foodList = [ABSIndividual(self.Bin,self.item) for k in range(self.foodCount)]   #初始化各蜜源
        self.foodScore = [d.score for d in self.foodList]                             #各蜜源最佳成绩
        self.bestFood = self.foodList[np.argmax(self.foodScore)]                      #全局最佳蜜源
 
    def updateFood(self, i):                                                  #更新第i个蜜源
        vi = copy.deepcopy(self.foodList[i])
        order =list(range(vi.allitem.shape[0]))
        random.shuffle(order) #随机生成装箱序列
        vi.ran = order
        vi.calculateFitness()
        if vi.score > self.foodList[i].score:           #如果成绩比当前蜜源好
            self.foodList[i] = vi
            if vi.score > self.foodScore[i]:            #如果成绩比历史成绩好（如重新初始化，当前成绩可能低于历史成绩）
                self.foodScore[i] = vi.score
                if vi.score > self.bestFood.score:      #如果成绩全局最优
                    self.bestFood = vi
            self.foodList[i].invalidCount = 0
        else:
            self.foodList[i].invalidCount += 1
            
    def employedBeePhase(self):
        for i in range(0, self.foodCount):              #各蜜源依次更新
            self.updateFood(i)            
 
    def onlookerBeePhase(self):
        foodScore = [d.score for d in self.foodList]  
        maxScore = np.max(foodScore)        
        accuFitness = [(0.9*d/maxScore+0.1, k) for k,d in enumerate(foodScore)]        #得到各蜜源的 相对分数和索引号
        for k in range(0, self.onlookerCount):
            i = random.choice([d[1] for d in accuFitness if d[0] >= random.random()])  #随机从相对分数大于随机门限的蜜源中选择跟随
            self.updateFood(i)
 
    def scoutBeePhase(self):
        for i in range(0, self.foodCount):
            if self.foodList[i].invalidCount > self.maxInvalidCount:                    #如果该蜜源没有更新的次数超过指定门限，则重新初始化
                self.foodList[i] = ABSIndividual(self.bound)
                self.foodScore[i] = max(self.foodScore[i], self.foodList[i].score)
 
    def solve(self):
        trace = []
        trace.append((self.bestFood.score, np.mean(self.foodScore)))
        for k in range(self.maxIterCount):
            self.employedBeePhase()
            self.onlookerBeePhase()
            self.scoutBeePhase()
            trace.append((self.bestFood.score, np.mean(self.foodScore)))
        print(self.bestFood.score)
        self.printResult(np.array(trace))
 
    def printResult(self, trace):
        x = np.arange(0, trace.shape[0])
        plt.plot(x, [(1-d)/d for d in trace[:, 0]], 'r', label='optimal value')
        plt.plot(x, [(1-d)/d for d in trace[:, 1]], 'g', label='average value')
        plt.xlabel("Iteration")
        plt.ylabel("function value")
        plt.title("Artificial Bee Swarm algorithm for function optimization")
        plt.legend()
        plt.show()
 
if __name__ == "__main__":
    random.seed()
    itemNum = 1000
    AllItem=np.array([[random.randint(1, 5) for j in range(1, 3)] for i in range(1,itemNum+1)])  #随机生成30个物品，[width,height]
    Bin=[100,100] #箱子宽度与高度
    iternum = 100 # 迭代次数
    maxInvalidCount = 50
    abs = ArtificialBeeSwarm(30, 30, Bin,AllItem, iternum, maxInvalidCount)
    abs.solve()
    print()