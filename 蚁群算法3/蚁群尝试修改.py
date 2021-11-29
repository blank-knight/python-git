from os import TMP_MAX
import random
from re import M, U
import re
from threading import main_thread
from typing import Iterable
import numpy as np
from numpy.core.numeric import ones
from subway_ import subway
import xlrd
import matplotlib.pyplot as plt
from Pretreatment import SVEM
import joblib
import time
from collections import Counter 
import xlwt 
import matplotlib as mpl

# 数据读取
ECH = joblib.load('/home/storm/桌面/蚁群存储信息/ECH')
TCH = joblib.load('/home/storm/桌面/蚁群存储信息/TCH')
matrix = joblib.load('/home/storm/桌面/蚁群存储信息/matrix')
v_s = joblib.load('/home/storm/桌面/蚁群存储信息/v_s.txt')
vs = v_s[0]
vk = int(vs)
s_sli = v_s[1]
s_pic = 50
time_start = time.time()

subway = subway()
SVEM1,Ju_mx,sol_mx = SVEM()

solu_x = []
solu_y = []
k = 0
for i in range(sol_mx.shape[1]):
    for j in sol_mx[:,i]:
        k += 1
        if j == 1:
            solu_x.append(i*50)
            solu_y.append(80-k)
            k = 0
            break
solu_y[0] = 0
solu_y[-1] = 0

'''
    随机数生成
'''
def p_random(arr1,arr2):
    assert len(arr1) == len(arr2), "Length does not match."
    assert sum(arr2) == 1 , "Total rate is not 1."

    # 提取小数点后面的位数。0.209年变209(str)
    sup_list = [len(str(i).split(".")[-1]) for i in arr2]
    # 找到最大的位数。1000
    top = 10 ** max(sup_list)
    # 将其全部化为整数。209(int)
    new_rate = [int(i*top) for i in arr2]
    rate_arr = []
    # 依次求和。209，500，1000
    for i in range(1,len(new_rate)+1):
        rate_arr.append(sum(new_rate[:i]))
    rand = random.randint(1,top)
    data = None
    # 判断产生的随机数在哪个区间段
    for i in range(len(rate_arr)):
        if rand <= rate_arr[i]:
            data = arr1[i]
            break
    return data

'''
    蚁群模块
'''

# 能耗，时间启发因子，信息素衰减因子，蚂蚁数量，迭代次数,时间限制(s)
(ALPHA, BETA,R,NUM,ITER,TIME) = (2,1,0.5,1,10,198)
col = Ju_mx.shape[1]+2
# d_x = []
# d_y = []
# for i in range(Ju_mx.shape[1]):
#     lis = list(Ju_mx[:,i])
#     for j in range(len(lis)):
#         if lis.pop(-1) == 0:
#             d_y.append(j+1)
#             d_x.append(i+1)
#             break
# d_x.insert(0,0)
# d_y.insert(0,0)
# d_x.insert(len(d_x),d_x[-1]+1)
# d_y.insert(len(d_y)+1,0)
# plt.plot(d_x,d_y)
# plt.show()

# 蚁群信息矩阵，后两维表示当前蚂蚁的总能耗和总时间，前面的表示蚂蚁的状态
ant_smx = np.zeros((NUM,col))
ant_smx[:,0] = 1
# 表示蚂蚁速度
ant_vmx = np.zeros((NUM,col))
ant_vmx[:,0] = vk
ant_emx = np.zeros((NUM,col))
E_st,ant_emx[:,0] = ECH[-vk,1],ECH[-vk,1]
ant_tmx = np.zeros((NUM,col))
T_st,ant_tmx[:,0] = TCH[-vk,1],TCH[-vk,1]*3600
# 把ECH变为信息素矩阵
LCH = np.zeros((ECH.shape[0],ECH.shape[1]))
# 存储当前最优，第一行为速度，第二行为能耗，第三行为时间，第四行为状态，后两列均为总能耗和总时间
best_mx = np.zeros((4,col)) 
best_mx[:,:] = 9999999999
tm = 0

# LK：信息素，SCH：状态(1位牵引，2为巡航，3为惰行，4为制动)，ECH：能耗，TCH：时间，SVEM2：可行解矩阵
# 返回下一个站点信息素最大的值,也就是最有可能选择的状态
def next_sta_pro(x,start,end,vk,ik,R,L,v_lim):
    v_q,E_q,t_q = subway.Qian_yin(start,end,vk,ik,R,L,matrix,v_lim)
    v_x,E_x,t_x = subway.Xun_hang(start,end,vk,ik,R,L,matrix)
    v_d,E_d,t_d = subway.Duo_xing(start,end,vk,ik,R,L,matrix,v_lim)
    print("当前横坐标为{0}".format(x))
    v_lis2,E_lis1,T_lis1,SC,LK = [],[],[],[],[0,0,0]
    v_lis2.extend([int(v_q),int(v_x),int(v_d)])
    pro = random.random()
    E_lis1.extend([int(E_q),int(E_x),int(E_d)])
    T_lis1.extend([t_q,t_x,t_d])
    SC.extend([1,2,3])
    ch_lis = [0,1,2]
    flag = 1
    ET_tol = 0
    for i in range(3):
        # 如果不满足条件，就将对应的元素从ch_lis删除
        if v_lis2[i] >= v_lim or v_lis2[i] < 0:
            del ch_lis[ch_lis.index(i)]
            continue
        # Ju_mx[-51,5]相当于Ju_mx[29,5]，而python矩阵正向下标是从0开始的，逆向是从-1开始
        # 所以Ju_mx[-51，5] == 1，但v_q是正向计算的，v_q == 51时是超速的，
        # 而我这里判断没有超速，所以出错了，应该再减个1
        # 正逆向列表推导公式lis[i] = lis[-(len(lis)-i)]
        # print("v_lis:",v_lis2)
        # print("v_lim:",v_lim)
        # print("v_lis2[i]:",v_lis2[i])
        if Ju_mx[-v_lis2[i]-1,x] == 0 or T_lis1[i] <= 0:
            del ch_lis[ch_lis.index(i)]
    # 如果此解为边缘解，直接将其信息素设为0，踢出可行解空间
    if ch_lis == []:
        # print("--------------------")
        # print(vk)
        LCH[-vk-1,x] = -99
        Ju_mx[-vk-1,x] = 0 
        flag = 0
        return flag,0,0,0,0
    for i in ch_lis:
        # print("vk为：",vk)
        # print("能耗列表为：",E_lis1)
        # print("时间列表为：",T_lis1)
        # print("速度列表为:",v_lis2)
        # print("ch_lis列表为:",ch_lis)
        ET_tol += pow(1/E_lis1[i], ALPHA)*pow(1/T_lis1[i], BETA)
    # 以0.4的概率进行随机游走
    if pro < 0.2:
        id = random.choice(ch_lis)
        print("随机变异的id为",id)
        # print(v_lis2)
        # print(v_lim)
        # 计算信息素 
        E = pow(1/E_lis1[i], ALPHA)
        T = pow(1/T_lis1[i], BETA)
        LCH[-v_lis2[id]-1,x] = E*T/ET_tol+LCH[-v_lis2[id]-1,x]*R
        return 1,v_lis2[id],E_lis1[id],int(T_lis1[id]*3600),SC[id]
    for i in ch_lis:
        # 如果有最优解，优先走最优解
        if v_lis2[i] == best_mx[0,x]:
            return 1,best_mx[0,x],best_mx[1,x],best_mx[2,x],best_mx[3,x]
        # 计算信息素,E很大，T很小，导致二者造成的平衡不一致 
        E = pow(1/E_lis1[i], ALPHA)
        T = pow(1/T_lis1[i], BETA)
        LCH[-v_lis2[i]-1,x] = E*T/ET_tol+LCH[-v_lis2[i]-1,x]*R
        LK[i] = LCH[-v_lis2[i]-1,x] 
    # 选择信息素最大的
    id = LK.index(max(LK))
    return 1,v_lis2[id],E_lis1[id],int(T_lis1[id]*3600),SC[id]

'''
    注意：我这里时间改为s
'''
for m in range(ITER):
    print("当前迭代次数是{0}".format(m))
    # 逐个蚂蚁开始跑
    for i in range(NUM):
        # 每只蚂蚁都要从头初始化参数
        print("当前是第{0}只蚂蚁".format(i))
        vk = int(vs)
        E_tol = E_st
        T_tol = T_st*3600
        s = s_pic
        # print("初始能耗是",E_tol)
        # time.sleep(2)
        # 蚂蚁从开头跑到结尾，除了开头的牵引和最后的制动没有加进来
        '''
            注意：这里有部分问题，矩阵和最后绘图对不上，s_sli为27
        '''
        for j in range(1,s_sli-1):
            if j < s_sli-2:
                print(j)
                s += s_pic
                end = s+s_pic
                s_id = np.where(matrix[:,0]>s)[0][0]
                v_li = matrix[s_id,1]
                ik = matrix[s_id,2]
                R = matrix[s_id,3]
                L = matrix[s_id,4]
                # j表示当前列数也就是位置
                flag,next_v,next_E,next_T,next_sta = next_sta_pro(j,s,end,vk,ik,R,L,v_li)
                # flag为0说明此蚂蚁走进了死胡同，放弃此蚂蚁
                if flag == 0:
                    break
                vk = int(next_v)
                print("下一节点速度为{0}".format(next_v))
                E_tol += next_E
                T_tol += next_T
                ant_smx[i,j] = next_sta
                print("当前蚂蚁的状态序列",ant_smx[i,0:j])
                ant_vmx[i,j] = next_v
                ant_emx[i,j] = next_E
                ant_tmx[i,j] = next_T
                continue
            # 加入制动
            s_id = np.where(matrix[:,0]>end)[0][0]
            ik = matrix[s_id,2]
            R = matrix[s_id,3]
            L = matrix[s_id,4]
            start = end
            end = matrix[-1,0]
            next_v,next_E,next_T,next_sta = subway.Zhi_dong(start,end,vk,ik,R,L,matrix)
            if next_v != 0:
                LCH[-vk-1,j] = -99
                Ju_mx[-vk-1,j] = 0
                continue 
            # print(next_v)
            T_tol += next_T
            E_tol += next_E
            ant_smx[i,j] = next_sta
            ant_vmx[i,j] = next_v
        if flag == 0:
            continue
        # 如果超时了，就进入下一只蚂蚁
        if T_tol > TIME:
            tm += 1
            # print("Time Out")
            # time.sleep(2)
            ant_vmx[i,-1],ant_vmx[i,-2] = 9999999999,9999999999
            ant_smx[i,-1],ant_smx[i,-2] = 9999999999,9999999999
            continue
        ant_vmx[i,-1],ant_vmx[i,-2] = T_tol,E_tol
        ant_smx[i,-1],ant_smx[i,-2] = T_tol,E_tol
        # print(ant_vmx[i,:])
    # 返回能耗最小的蚂蚁
    best_id = ant_smx.argmin(axis=0)[-2]
    # 判断此次是否是第一次迭代或者此次的蚂蚁能耗是否小于目前最优蚂蚁
    if best_mx[0,-2] == 0 or ant_vmx[best_id,-2] < best_mx[0,-2]:
        for n in range(col-2):
            best_mx[0,n] = ant_vmx[best_id,n]
            best_mx[1,n] = ant_emx[best_id,n]
            best_mx[2,n] = ant_tmx[best_id,n]
            best_mx[3,n] = ant_smx[best_id,n]
        best_mx[0,col-2] = ant_vmx[best_id,col-2]
        best_mx[0,col-1] = ant_vmx[best_id,col-1]
    # print(best_mx)
    # ant_vmx[:,:] = 0
    # ant_emx[:,:] = 0
    # ant_tmx[:,:] = 0
    # ant_smx[:,:] = 0
    # ant_smx[:,0] = 1
    # ant_vmx[:,0] = vk
    # ant_emx[:,0] = ECH[-vk,1]
    # ant_tmx[:,0] = TCH[-vk,1]*3600
    

time_end = time.time()
time_total = time_end-time_start
# print(tm)
s_pic = 50
dis_x = []
dis_y = []
dis_x = [x*s_pic for x in range(0,col-2)]
print("dis_x:",dis_x) 
dis_y = list(best_mx[0,0:-3])
dis_y.insert(0,0)
print("dis_y:",dis_y)
plt.plot(dis_x,dis_y,label="Original curve")
plt.legend()
z1 = np.polyfit(dis_x, dis_y, 10)              # 曲线拟合，返回值为多项式的各项系数
p1 = np.poly1d(z1)                    # 返回值为多项式的表达式，也就是函数式子
# print(p1)
y_pred = p1(dis_x)  
plt.plot(dis_x,y_pred,label="Curve fitting")
plt.legend()
# 最大可行解曲线
plt.plot(solu_x,solu_y,label="Maximum feasible solution")
plt.legend()
plt.xlabel("Distance")
plt.ylabel("Speed")
plt.title("ene-factor:3,time-factor:2,imf-factor:0.7")
plt.text(0,80,'ant-num:10,loop-num:10,time-lim:500')

# plt.plot(d_x,d_y)
plt.show()
# print(dis_x)
# print(dis_y)
# print(d_x)
# print(d_y)
print("程序运行时间是:",time_total)
print("消耗的能量是：",best_mx[0,-2])
print("消耗的是时间：",best_mx[0,-1])
print("注意，这里最佳速度和路径状态是从50米处开始的，0处的没有添加进来")
print("最佳的速度状态：",best_mx[0,0:-4])
print("最佳的路径状态：",best_mx[3,0:-4])