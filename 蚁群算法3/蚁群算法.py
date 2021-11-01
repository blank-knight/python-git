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

# 数据读取
ECH = joblib.load('/home/zhaowentao/桌面/蚁群矩阵信息/ECH')
TCH = joblib.load('/home/zhaowentao/桌面/蚁群矩阵信息/TCH')
matrix = joblib.load('/home/zhaowentao/桌面/蚁群矩阵信息/matrix')
v_s = joblib.load('/home/zhaowentao/桌面/蚁群矩阵信息/v_s.txt')
vs = v_s[0]
vk = int(vs)
s_sli = v_s[1]
s_pic = 50

'''
    蚁群模块
'''
subway = subway()
SVEM1,Ju_mx = SVEM()
# 能耗，时间启发因子，信息素衰减因子，蚂蚁数量，迭代次数,时间限制
(ALPHA, BETA,R,NUM,ITER,TIME) = (2,1,0.5,1,50,0.055)
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
T_st,ant_tmx = TCH[-vk,1],TCH[-vk,1]
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
    # print("当前横坐标为{0}".format(x))
    v_lis2,E_lis1,T_lis1,SC,LK = [],[],[],[],[0,0,0]
    pro = random.random()
    v_lis2.extend([int(v_q),int(v_x),int(v_d)])
    E_lis1.extend([int(E_q),int(E_x),int(E_d)])
    T_lis1.extend([t_q,t_x,t_d])
    SC.extend([1,2,3])
    ch_lis = [0,1,2]
    flag = 1
    fre = 0
    for i in range(3):
        if v_lis2[i] > v_lim or v_lis2[i] < 0:
            fre += 1
            continue
        if Ju_mx[-v_lis2[i],x] == 0 or T_lis1[i] < 0:
            fre += 1
    if fre == 3:
        # 如果此解为边缘解，直接将其信息素设为0，踢出可行解空间
        # print("--------------------")
        # print(vk)
        LCH[-vk,x] = -99
        Ju_mx[-vk,x] = 0 
        flag = 0
        return flag,0,0,0,0
    # 以0.4的概率进行随机游走
    if pro < 0.4:
        # fre = 0
        np.random.seed(0)
        p = np.array([0.2,0.5,0.3])
        while True:
            # fre += 1
            # if fre > 20:
            #     return 0,_,_,_,_
            id = np.random.choice([0,1,2], p=p.ravel())
            if id in ch_lis:
                del ch_lis[id-1]
            if ch_lis == []:
                return flag,0,0,0,0
            # print(id)
            # print(v_lis2)
            # print(v_lim)
            if v_lis2[id] > v_lim or v_lis2[id] < 0:
                continue
            if Ju_mx[-v_lis2[id],x] == 1 and T_lis1[id] > 0:
            # 计算信息素 
                LCH[-v_lis2[id],x] = pow(E_lis1[id], ALPHA) / pow(T_lis1[id], BETA)+LCH[-v_lis2[id],x]*R
                return 1,v_lis2[id],E_lis1[id],T_lis1[id],SC[id]
    for i in range(3):
        if v_lis2[i] > v_lim or v_lis2[i] < 0:
            fre += 1
            continue
        # 如果有最优解，优先走最优解
        if v_lis2[i] == best_mx[0,x]:
            return 1,best_mx[0,x],best_mx[1,x],best_mx[2,x],best_mx[3,x]
        if Ju_mx[-v_lis2[i],x] == 1 and T_lis1[i] > 0:
            # 计算信息素 
            LCH[-v_lis2[i],x] = pow(E_lis1[i], ALPHA) / pow(T_lis1[i], BETA)+LCH[-v_lis2[i],x]*R
            LK[i] = LCH[-v_lis2[i],x] 
    # 选择信息素最大的
    id = LK.index(max(LK))
    return 1,v_lis2[id],E_lis1[id],T_lis1[id],SC[id]


for m in range(ITER):
    print("当前迭代次数是{0}".format(m))
    # 逐个蚂蚁开始跑
    for i in range(NUM):
        # 每只蚂蚁都要从头初始化参数
        print("当前是第{0}只蚂蚁".format(i))
        vk = int(vs)
        E_tol = E_st
        T_tol = T_st
        s = s_pic
        # print("初始能耗是",E_tol)
        # time.sleep(2)
        # 蚂蚁从开头跑到结尾，除了开头的牵引和最后的制动没有加进来
        for j in range(1,s_sli-1):
            if j < s_sli-2:
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
                # vk = int(next_v)
                # print("下一节点速度为{0}".format(next_v))
                E_tol += next_E
                T_tol += next_T
                ant_smx[i,j] = next_sta
                # print("当前蚂蚁的状态序列",ant_smx[i,0:j])
                ant_vmx[i,j] = next_v
                continue
            # 加入制动
            s_id = np.where(matrix[:,0]>end)[0][0]
            ik = matrix[s_id,2]
            R = matrix[s_id,3]
            L = matrix[s_id,4]
            start = end
            end = matrix[-1,0]
            next_v,next_E,next_T,next_sta = subway.Zhi_dong(start,end,next_v,ik,R,L,matrix)
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
    if best_mx[0,-2] == 0 or ant_vmx[best_id,-2] < best_mx[0,-2]:
        for n in range(col):
            best_mx[0,n] = ant_vmx[best_id,n]
            best_mx[1,n] = ant_vmx[best_id,-2]
            best_mx[2,n] = ant_vmx[best_id,-1]
            best_mx[3,n] = ant_smx[best_id,n]

print(tm)
s_pic = 50
dis_x = []
dis_y = []
dis_x = [x for x in range(0,col-1)]
dis_y = list(best_mx[0,0:-2])
dis_y.insert(0,0)
plt.plot(dis_x,dis_y)
# plt.plot(d_x,d_y)
plt.show()
# print(dis_x)
# print(dis_y)
# print(d_x)
# print(d_y)
print("消耗的能量是：",best_mx[0,-2])
print("消耗的是时间：",best_mx[0,-1])