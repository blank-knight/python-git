import random
from re import S, X, sub
from threading import main_thread
from typing import Iterable
import numpy as np
from numpy.core.numeric import ones
from subway_ import subway
import xlrd
import matplotlib.pyplot as plt
from Pretreatment import SVEM
import joblib
import pickle
'''
    注：这一模块文件发现在后面其实没啥用，可以融合进蚁群算法里面
'''
subway = subway()
'''
    预处理模块
'''
# 读取表格数据
data = xlrd.open_workbook(r'/home/zhaowentao/桌面/列车数据.xlsx')
table = data.sheets()[0]
# 获取列表的行列，并构建相应的矩阵存储数据
rowNum = table.nrows
colNum = table.ncols
matrix_ = np.zeros((rowNum,colNum))
tables = []
#将excel表格内容导入到matrix矩阵中
for rown in range(table.nrows):
    # 读取数据，已在Excel表上做完了预处理
    matrix_[rown,] = table.row_values(rown)
matrix = matrix_.astype(int)
# print(matrix)
v_max = max(matrix[:,1])
s_max = matrix[-1,0]

'''
    根据可行解空间构建能耗，时间，运动状态，信息素四大矩阵
'''
# x为离散后图的横坐标
def V_E_cal(cla,x,start,end,vk,ik,R,L,v_lim):
    # print(cla,x,start,end,vk,ik,R,L,v_lim)
    if cla == 0:
        v_q,E_q,t_q = subway.Qian_yin(start,end,vk,ik,R,L,matrix,v_lim)
        if Ju_mx[-int(v_q),x] == 1:
            ECH[-int(v_q),x] = E_q
            TCH[-int(v_q),x] = t_q
            SCH[-int(v_q),x] = 1
            LK[-int(v_q),x] =  pow(E_q, ALPHA) / pow(t_q, BETA)
            SVEM2[-int(v_q),x] = 1
        return v_q
    elif cla == 1:
        print(x)
        v_lis2 = []
        E_lis1 = []
        T_lis1 = []
        S_lis1 = []
        v_q,E_q,t_q = subway.Qian_yin(start,end,vk,ik,R,L,matrix,v_lim)
        v_x,E_x,t_x = subway.Xun_hang(start,end,vk,ik,R,L,matrix)
        v_d,E_d,t_d = subway.Duo_xing(start,end,vk,ik,R,L,matrix,v_lim)
        # print(v_q,v_x,v_d)
        v_lis1.extend([int(v_q),int(v_x),int(v_d)])
        v_lis2.extend([int(v_q),int(v_x),int(v_d)])
        E_lis1.extend([int(E_q),int(E_x),int(E_d)])
        T_lis1.extend([t_q,t_x,t_d])
        S_lis1.extend([1,2,3])
        # E_lis1.extend([E_q,E_x,0])
        for i in range(3):
            if v_lis2[i] > v_lim or v_lis2[i] < 0:
                continue
            if Ju_mx[-v_lis2[i],x] == 1:
                ECH[-v_lis2[i],x] = E_lis1[i]
                TCH[-v_lis2[i],x] = T_lis1[i]
                SCH[-v_lis2[i],x] = S_lis1[i]
                SVEM2[-v_lis2[i],x] = 1
                if T_lis1[i] > 0:
                    LK[-v_lis2[i],x] =  pow(E_lis1[i], ALPHA) / pow(T_lis1[i], BETA)
    elif cla == 2:
        v_z,E_z,t_z = subway.Zhi_dong(vk,ik,R,L)
        if Ju_mx[-int(v_z),x] == 1:
            ECH[-int(v_z),x] = E_z
            TCH[-int(v_z),x] = t_z
            SCH[-int(v_z),x] = 1
            LK[-int(v_z),x] =  pow(E_z, ALPHA) / pow(t_z, BETA)

'''
    构建距离、速度、能耗可行解矩阵,初始化
'''
(ALPHA, BETA, RHO, Q,T) = (2.0,4.0,0.4,400.0,150)
# 计算可行速度节点(注意，这里不能出现50整数倍的距离)
s_pic = 50
s_sli = s_max//s_pic+1
v_sli = v_max//1
# 获取最大可行解矩阵，将LK设为信息素矩阵
SVEM1,Ju_mx = SVEM()
# plt.matshow(Ju_mx)
# plt.show()
# 信息素，状态(1位牵引，2为巡航，3为惰行，4为制动)，能耗，时间，可行解矩阵
LK = np.zeros((Ju_mx.shape[0],Ju_mx.shape[1]))
SCH = np.zeros((Ju_mx.shape[0],Ju_mx.shape[1]))
ECH = np.zeros((Ju_mx.shape[0],Ju_mx.shape[1]))
TCH = np.zeros((Ju_mx.shape[0],Ju_mx.shape[1]))
SVEM2 = np.zeros((Ju_mx.shape[0],Ju_mx.shape[1]))
s = 0
vk = 0
# 牵引
s += s_pic
s_id = np.where(matrix)[0][0]
x = 1
# 第一个节点必为牵引
vk = V_E_cal(0,1,0,s,vk,matrix[s_id,2],matrix[s_id,3],matrix[s_id,4],matrix[s_id,1])
# 第一步
v_s = [vk,s_sli]
v_lis1 = []
v_lis1.append(vk)
# 牵引、巡航、惰行
# 这里不能s_sli-1因为到1300时，end=1350超出了
for i in range(1,s_sli-2):
    s += s_pic 
    end = s+s_pic
    s_id = np.where(matrix[:,0]>s)[0][0]
    v_li = matrix[s_id,1]
    ik = matrix[s_id,2]
    R = matrix[s_id,3]
    L = matrix[s_id,4]
    for j in range(len(v_lis1)):
        # bug所在处
        # v_lis1 = list(set(v_lis1))
        # v_lis1 = sorted(list(set(v_lis1)))
        k = 0
        while True:
            if k < len(v_lis1):
                if v_lis1[k] in v_lis1[k+1::]:
                    del v_lis1[k]
                else:
                    k += 1
            else:
                break
        # print(v_lis1)
        vk = v_lis1.pop(0)
        if vk > v_li or vk <= 0:
            continue
        else:
            V_E_cal(1,i,s,end,vk,ik,R,L,v_li)

#把矩阵保存到磁盘，生成一个文件ECH
joblib.dump(ECH,'/home/zhaowentao/桌面/蚁群矩阵信息/ECH')
joblib.dump(TCH,'/home/zhaowentao/桌面/蚁群矩阵信息/TCH')
joblib.dump(LK,'/home/zhaowentao/桌面/蚁群矩阵信息/LK')
joblib.dump(SCH,'/home/zhaowentao/桌面/蚁群矩阵信息/SCH')
joblib.dump(matrix,'/home/zhaowentao/桌面/蚁群矩阵信息/matrix')

f=open('/home/zhaowentao/桌面/蚁群矩阵信息/v_s.txt','wb')
pickle.dump(v_s,f)
f.close()

plt.matshow(ECH)
plt.title('ECH')
plt.matshow(TCH)
plt.title('TCH')
plt.matshow(SCH)
plt.title('SCH')
plt.matshow(LK)
plt.title('LK')
plt.matshow(SVEM2)
plt.title('SVEM2')
plt.show()


