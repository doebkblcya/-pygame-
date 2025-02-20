#调用pygame库
import pygame
import sys
#调用常用关键字常量
from pygame.locals import QUIT,KEYDOWN
import numpy as np
#初始化pygame
pygame.init()
#获取对显示系统的访问，并创建一个窗口screen
#窗口大小为670x670
screen = pygame.display.set_mode((670,670))
screen_color=[238,154,73]#设置画布颜色,[238,154,73]对应为棕黄色
line_color = [0,0,0]#设置线条颜色，[0,0,0]对应黑色

def check_win(over_pos):#判断五子连心
    mp=np.zeros([15,15],dtype=int)
    for val in over_pos:
        x=int((val[0][0]-27)/44)
        y=int((val[0][1]-27)/44)
        if val[1]==white_color:
            mp[x][y]=2#表示白子
        else:
            mp[x][y]=1#表示黑子

    for i in range(15):
        pos1=[]
        pos2=[]
        for j in range(15):
            if mp[i][j]==1:
                pos1.append([i,j])
            else:
                pos1=[]
            if mp[i][j]==2:
                pos2.append([i,j])
            else:
                pos2=[]
            if len(pos1)>=5:#五子连心
                return [1,pos1]
            if len(pos2)>=5:
                return [2,pos2]

    for j in range(15):
        pos1=[]
        pos2=[]
        for i in range(15):
            if mp[i][j]==1:
                pos1.append([i,j])
            else:
                pos1=[]
            if mp[i][j]==2:
                pos2.append([i,j])
            else:
                pos2=[]
            if len(pos1)>=5:
                return [1,pos1]
            if len(pos2)>=5:
                return [2,pos2]
    for i in range(15):
        for j in range(15):
            pos1=[]
            pos2=[]
            for k in range(15):
                if i+k>=15 or j+k>=15:
                    break
                if mp[i+k][j+k]==1:
                    pos1.append([i+k,j+k])
                else:
                    pos1=[]
                if mp[i+k][j+k]==2:
                    pos2.append([i+k,j+k])
                else:
                    pos2=[]
                if len(pos1)>=5:
                    return [1,pos1]
                if len(pos2)>=5:
                    return [2,pos2]
    for i in range(15):
        for j in range(15):
            pos1=[]
            pos2=[]
            for k in range(15):
                if i+k>=15 or j-k<0:
                    break
                if mp[i+k][j-k]==1:
                    pos1.append([i+k,j-k])
                else:
                    pos1=[]
                if mp[i+k][j-k]==2:
                    pos2.append([i+k,j-k])
                else:
                    pos2=[]
                if len(pos1)>=5:
                    return [1,pos1]
                if len(pos2)>=5:
                    return [2,pos2]
    return [0,[]]

def find_pos(x,y):#找到显示的可以落子的位置
    for i in range(27,670,44):
        for j in range(27,670,44):
            L1=i-22
            L2=i+22
            R1=j-22
            R2=j+22
            if x>=L1 and x<=L2 and y>=R1 and y<=R2:
                return i,j
    return x,y

def check_over_pos(x,y,over_pos):#检查当前的位置是否已经落子
    for val in over_pos:
        if val[0][0]==x and val[0][1]==y:
            return False
    return True#表示没有落子
flag=False
tim=0

over_pos=[]#表示已经落子的位置
white_color=[255,255,255]#白棋颜色
black_color=[0,0,0]#黑棋颜色

while True:#不断训练刷新画布

    for event in pygame.event.get():#获取事件，如果鼠标点击右上角关闭按钮，关闭
        if event.type in (QUIT,KEYDOWN):
            sys.exit()

    screen.fill(screen_color)#清屏
    for i in range(27,670,44):
        #先画竖线
        if i==27 or i==670-27:#边缘线稍微粗一些
            pygame.draw.line(screen,line_color,[i,27],[i,670-27],4)
        else:
            pygame.draw.line(screen,line_color,[i,27],[i,670-27],2)
        #再画横线
        if i==27 or i==670-27:#边缘线稍微粗一些
            pygame.draw.line(screen,line_color,[27,i],[670-27,i],4)
        else:
            pygame.draw.line(screen,line_color,[27,i],[670-27,i],2)

    #在棋盘中心画个小圆表示正中心位置
    pygame.draw.circle(screen, line_color,[27+44*7,27+44*7], 8,0)

    for val in over_pos:#显示所有落下的棋子
        pygame.draw.circle(screen, val[1],val[0], 20,0)

    #判断是否存在五子连心
    res=check_win(over_pos)
    if res[0]!=0:
        for pos in res[1]:
            pygame.draw.rect(screen,[238,48,167],[pos[0]*44+27-22,pos[1]*44+27-22,44,44],2,1)
        pygame.display.update()#刷新显示
        continue#游戏结束，停止下面的操作
    #获取鼠标坐标信息
    x,y = pygame.mouse.get_pos()

    x,y=find_pos(x,y)
    if check_over_pos(x,y,over_pos):#判断是否可以落子，再显示
        pygame.draw.rect(screen,[0 ,229 ,238 ],[x-22,y-22,44,44],2,1)

    keys_pressed = pygame.mouse.get_pressed()#获取鼠标按键信息
    #鼠标左键表示落子,tim用来延时的，因为每次循环时间间隔很断，容易导致明明只按了一次左键，却被多次获取，认为我按了多次
    if keys_pressed[0] and tim==0:
        flag=True
        if check_over_pos(x,y,over_pos):#判断是否可以落子，再落子
            if len(over_pos)%2==0:#黑子
                over_pos.append([[x,y],black_color])
            else:
                over_pos.append([[x,y],white_color])

    #鼠标左键延时作用
    if flag:
        tim+=1
    if tim%50==0:#延时200ms
        flag=False
        tim=0

    pygame.display.update()#刷新显示

