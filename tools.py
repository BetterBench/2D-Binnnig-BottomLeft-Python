
from matplotlib.pyplot import axis
import numpy as np

def Horizontal_Lines_Intersect(line1,line2):
    # 判断两条水平线段经过竖直移动后是否会相交，如果相交，计算两条水平线段竖直距离是多少
    # 思路：分5种情况：1）左方不相交；2）左方相交；3）右方相交；4）右方不相交；5）line1完全包含line2
    # 输入line1：  第一条线段[x1,y1,x2,y2]
    # 输入line2：  第二条线段[x1,y1,x2,y2]
    # 输出flag：  判断两条水平线段经过竖直移动后是否会相交，flag=1相交，flag=0不相交
    # 输出HD：  两条竖直线段距离是多少，如果平移动后相交，HD为正数，反之为负数
    #第一种情况，line1完全在line2左方，即line1右端顶点x坐标小于等于line2左端顶点x坐标，且两条线段经过竖直移动后不会相交
    if line1[2]<=line2[0]:
        flag=0
        HD=line1[1]-line2[1]
    #第二种情况，line1在line2左方，即line1右端顶点x坐标大于line2左端顶点x坐标且小于等于且line2右端顶点x坐标，但两条线段经过竖直移动后会相交
    elif (line1[2]>line2[0]) and (line1[2]<=line2[0]):
        flag=1
        HD=line1[1]-line2[1]
    #第三种情况，line1在line2右方，即line1左端顶点x坐标大于等于line2左端顶点x坐标且小于且line2右端顶点x坐标，但两条线段经过竖直移动后会相交
    elif (line1[0]>=line2[0]) and (line1[0]<line2[2]):
        flag=1
        HD=line1[1]-line2[1]
    #第四种情况，line1完全在line2右方，即line1左端顶点x坐标大于等于line2右端顶点x坐标，且两条线段经过竖直移动后不会相交
    elif line1[0]>=line2[2]:
        flag=0
        HD=line1[1]-line2[1]
    #第五种情况，line1完全包含line2，即line1左端顶点x坐标小于等于line2左端顶点x坐标，
    #line1右端顶点x坐标大于等于line2右端顶点x坐标，且两条线段经过竖直移动后会相交
    else:
        flag=1
        HD=line1[1]-line2[1]
    return flag,HD

######################################
# 根据物品右上角顶点坐标和物品宽度和高度，求出物品下端水平线段左右两端坐标[leftx,lefty,rightx,righty]
# 输入item：  物品[宽度，高度]
# 输入RPXY：物品右上角顶点坐标[x,y]
# 输出leftLine：  物品下端水平线段左右两端坐标[leftx,lefty,rightx,righty]
def Point_Horizontal_Line(item,RPXY):
    RBPXY=[RPXY[0],RPXY[1]-item[1]]#  物品右下角顶点坐标
    LBPXY=[RPXY[0]-item[0],RPXY[1]-item[1]]  #物品左下角顶点坐标
    bottomLine=[]
    bottomLine.extend(LBPXY)
    bottomLine.extend(RBPXY)
    return bottomLine

# 计算在当前箱子中，物品item在箱子内任意位置可以下降的最大高度
# 输入item：   物品[宽度，高度]
# 输入AllItem：   各个物品[宽度，高度]
# 输入itemRP： 此时物品右上角顶点坐标[x,y]
# 输入RPNXY：  当前箱子中所有物品右上角顶点坐标数组
# 输出downH：  物品item在箱子内任意位置可以下降的最大高度（如果能装入当前箱子，则downH为正数；如果不能装入当前箱子，则为负数）
def downHAtPoint(item,AllItem,itemRP,RPNXY):
    bottomLine=Point_Horizontal_Line(item,itemRP)  #物品下端水平线段左右两端坐标[leftx,lefty,rightx,righty]
    RP_NUM=len(RPNXY) #箱子内物品数目
    if RP_NUM!=0:
        sRPNXY=np.array(sorted(list(RPNXY), key=lambda x:x[2],reverse=True))#将RPNXY按照Y坐标降序排列
        sRBPNXY=sRPNXY.copy()
        sRBPNXY[:,1]=sRPNXY[:,1]-AllItem[sRPNXY[:,0],0]  #将RPNXY按照Y坐标降序排列后的左上角顶点坐标
        
        topLine=np.concatenate((sRBPNXY[:,1:3],sRPNXY[:,1:3]),axis=1)  #物品按照Y坐标降序排列后，物品上端水平线段左右两端坐标[leftx,lefty,rightx,righty]
        # 逐个遍历sRPNXY中的物品
        alldownH=[]  # 储存所有满足相交条件的下降距离
        for i in range(RP_NUM):
            #判断两条水平线段经过竖直移动后是否会相交，flag=1相交，flag=0不相交
            #两条水平线段距离是多少，如果竖直移动后相交，HD为正数，反之为负数
            flag,HD=Horizontal_Lines_Intersect(bottomLine,topLine[i,:])
            if (flag==1) and (HD>=0):
                alldownH.append(HD)
        # 如果不存在满足相交条件的物品，则直接下降到箱子最底端
        if len(alldownH)==0:
            downH=itemRP[1]-item[1]
        else:  # 如果存在满足相交条件的物品，则下降距离为alldownH中的最小值
            downH=min(alldownH)
    else:
        downH=itemRP[1]-item[1]  #此时箱子没有物品，物品直接下降到箱子底端
    return downH

# 判断两条竖直线段经过水平移动后是否会相交，如果相交，计算两条竖直线段水平距离是多少
# 思路：分5种情况：1）上方不相交；2）上方相交；3）下方相交；4）下方不相交；5）line1完全包含line2
# 输入line1：  第一条线段[topx,topy,bottomx,bottomy]
# 输入line2：  第二条线段[topx,topy,bottomx,bottomy]
# 输出flag：  判断两条竖直线经过水平移动后是否会相交，flag=1相交，flag=0不相交
# 输出HD：  两条竖直线段距离是多少，如果平移动后相交，HD为正数，反之为负数
def Vertical_Lines_Intersect(line1,line2):
    # 第一种情况，line1完全在line2上方，且两条线段经过平移后不会相交
    if line1[3]>=line2[1]:
        flag=0
        HD=line1[0]-line2[0]
    # 第二种情况，line1在line2上方，但两条线段经过平移后会相交
    elif (line1[3]<line2[1])and (line1[3]>=line2[3]):
        flag=1
        HD=line1[0]-line2[0]
    # 第三种情况，line1在line2下方，但两条线段经过平移后会相交
    elif (line1[1]<=line2[1]) and (line1[1]>line2[3]):
        flag=1
        HD=line1[0]-line2[0]
    # 第四种情况，line1完全在line2下方，且两条线段经过平移后不会相交
    elif line1[1]<=line2[3]:
        flag=0
        HD=line1[0]-line2[0]
    else:
        flag=1
        HD=line1[0]-line2[0]
    return flag,HD

# 根据物品右上角顶点坐标和物品宽度和高度，求出物品左端竖直线段上下两端坐标[topx,topy,bottomx,bottomy]
# 输入item：  物品[宽度，高度]
# 输入RPXY：物品右上角顶点坐标[x,y]
# 输出leftLine：  物品左端竖直线段上下两端坐标[topx,topy,bottomx,bottomy]
def Point_Vertical_Line(item,RPXY):
    LUPXY=[RPXY[0]-item[0],RPXY[1]]  #物品左上角顶点坐标
    LBPXY=[RPXY[0]-item[0],RPXY[1]-item[1]] #物品左下角顶点坐标
    leftLine=[]
    leftLine.extend(LUPXY)
    leftLine.extend(LBPXY)
    return leftLine

# 计算在当前箱子中，物品item在箱子内任意位置可以向左移动的最大距离
# 输入item：   物品[宽度，高度]
# 输入Item：   各个物品[宽度，高度]
# 输入itemRP： 此时物品右上角顶点坐标[x,y]
# 输入RPNXY：  当前箱子中所有物品右上角顶点坐标数组
# 输出leftW：  物品item在箱子内任意位置可以向左移动的最大距离
def leftWAtPoint(item,Item,itemRP,RPNXY):
    leftLine=Point_Vertical_Line(item,itemRP)  #物品左端竖直线段上下两端坐标[topx,topy,bottomx,bottomy]
    RP_NUM=len(RPNXY)#箱子内物品数目
    if RP_NUM!=0:
        sRPNXY=np.array(sorted(list(RPNXY), key=lambda x:x[0]))  #将RPNXY按照X坐标降序排列
        sRBPNXY=sRPNXY.copy()
        sRBPNXY[:,2]=sRPNXY[:,2]-Item[sRPNXY[:,0],1] #将RPNXY按照X坐标降序排列后的右下角顶点坐标
        rightLine=np.concatenate((sRPNXY[:,1:3],sRBPNXY[:,1:3]),axis=1)#物品按照X坐标降序排列后，右端线段上下两端坐标[topx,topy,bottomx,bottomy]
        #逐个遍历sRPNXY中的物品
        allLeftW=[]  #储存所有满足相交条件的左移距离
        for i in range(RP_NUM):
            #判断两条竖直线经过水平移动后是否会相交，flag=1相交，flag=0不相交
            #两条竖直线段距离是多少，如果平移动后相交，HD为正数，反之为负数
            flag,HD=Vertical_Lines_Intersect(leftLine,rightLine[i,:])
            if (flag==1) and (HD>=0):
                allLeftW.append(HD)
        # 如果不存在满足相交条件的物品，则直接移动箱子最左端
        if len(allLeftW)==0:
            leftW=itemRP[0]-item[0]
        else: #如果存在满足相交条件的物品，则左移距离为allLeftW中的最小值
            leftW=min(allLeftW)
    else:
        leftW=itemRP[0]-item[0]
    return leftW

# 计算物品在箱子中从右上角下降downH又向左移动leftW后，右上角顶点的坐标
# 输入itemRP： 此时物品右上角顶点坐标[x,y]
# 输入downH：  物品item从右上角可以下降的最大高度
# 输入leftW：  物品item从右上角下降最大高度以后，可以向左移动的最大距离
# 输出itRPXY： 物品item在箱子中下降downH又向左移动leftW后，右上角顶点的坐标
def Update_itemRP(itemRP,downH,leftW):
    h=itemRP[1]-downH  #y坐标
    w=itemRP[0]-leftW   #x坐标
    return [w,h]
# 矩形类，[x,y,width,height]左下角坐标、长和宽
class Rectangle:
    def __init__(self, x, y,w,h):
      self.x = x
      self.y = y
      self.width = w
      self.height = h
# 计算物品从当前位置向下向左移动后到最终位置后右上角顶点坐标
# 输入item：   物品[宽度，高度]
# 输入Item：   各个物品[宽度，高度]
# 输入itemRP： 此时物品右上角顶点坐标[x,y]
# 输入RPNXY：  当前箱子中所有物品右上角顶点坐标数组
# 输出finalRP：物品item在箱子内任意位置向下向左移动后到最终位置后右上角顶点坐标
def finalPos(item,Item,itemRP,RPNXY):
    # 当物品item不能再继续下降或不能继续左移的时候，跳出循环
    while 1:
        downH=downHAtPoint(item,Item,itemRP,RPNXY) #计算物品item在箱子内itemRP位置处可以下降的最大高度
        leftW=0
        itemRP=Update_itemRP(itemRP,downH,leftW) #更新物品item当前位置右上角顶点坐标
        downH=0
        leftW=leftWAtPoint(item,Item,itemRP,RPNXY) #计算物品item在箱子内itemRP位置处可以向左移动的最大距离
        itemRP=Update_itemRP(itemRP,downH,leftW) #更新物品item当前位置右上角顶点坐标
        if (downH==0)and (leftW==0):
            finalRP=itemRP
            break
    return finalRP

# 判断物品item在当前位置itemRP与箱子中其他物品是否有重合
# 输入item：   物品[宽度，高度]
# 输入Item：   各个物品[宽度，高度]
# 输入itemRP： 此时物品右上角顶点坐标[x,y]
# 输入RPNXY：  当前箱子中所有物品右上角顶点坐标数组
# 输出flagOL： 如果重合flagOL=1；反之flagOL=0
def overlap(item,Item,itemRP,RPNXY):
    flagOL=0  # 初始化不存在重合情况
    itemLBP=[itemRP[0]-item[0],itemRP[1]-item[1]] #左下角顶点坐标
    A = Rectangle(itemLBP[0],itemLBP[1],item[0],item[1])
    num=len(RPNXY) # 箱子中物品数目
    if num>0:
        for i in range(num):
            width=Item[RPNXY[i][0],0]  #Item(RPNXY(i,1),:)宽度
            height=Item[RPNXY[i][0],1]  #Item(RPNXY(i,1),:)高度
            LBPXY=[RPNXY[i][1]-width,RPNXY[i][2]-height]  #在箱子中的当前矩形Item(RPNXY(i,1),:)的左下角顶点坐标
            B = Rectangle(LBPXY[0],LBPXY[1],width,height)
            area=rectint(A,B)#计算物品A与B相交的面积
            #如果AB相交，则满足下列关系
            if area>0:
                flagOL=1
                break
    return flagOL
# 计算两个矩形相交的面积，和MATLAB中rectint函数作用一样
def rectint(rect1, rect2):
    xl1, yb1, xr1, yt1 = rect1.x,rect1.y,rect1.x+rect1.width,rect1.y+rect1.height # （xl1, yb1）为矩形左下角坐标， （xr1, yt1）为右上角坐标
    xl2, yb2, xr2, yt2 = rect2.x,rect2.y,rect2.x+rect2.width,rect2.y+rect2.height # （xl2, yb2）为矩形左下角坐标， （xr2, yt2）为右上角坐标
    xmin = max(xl1, xl2)
    ymin = max(yb1, yb2)
    xmax = min(xr1, xr2)
    ymax = min(yt1, yt2)
    width = xmax - xmin
    height = ymax - ymin
    if width <= 0 or height <= 0:
        return 0
    cross_square = width * height
    return cross_square