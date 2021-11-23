import random
from re import S, sub
from threading import main_thread
import numpy as np
from numpy.core.numeric import ones
from subway import subway
import xlrd
import matplotlib.pyplot as plt

subway = subway()
'''
    预处理模块
'''
# 读取表格数据
data = xlrd.open_workbook(r'/home/storm/桌面/蚁群存储信息/列车数据3.xlsx')
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
v_max = max(matrix[:,1])
s_max = matrix[-1,0]

def SVEM():
    SVEM1 = np.zeros((v_max,s_max))
    vk = 0
    loc = list(matrix[:,0])
    i = s_max
    j = len(loc)-1

    '''
        注：这里有部分问题，正逆向的起点不为0
    '''
    # 逆向计算
    v_lim = matrix[j,1]
    while vk < v_lim:
        if i >= loc[j]:
            ik = matrix[j,2]
            R = matrix[j,3]
            L = matrix[j,4]
            vk = subway.Zhi_dong(vk,ik,R,L,v_lim)
            col = vk
            for k in range(int(col)+1):
                SVEM1[v_max-k-1,i-1] = 1
            i -= 1
        else:
            j -= 1
            v_lim = matrix[j,1]

    s_max_ = i
    i = 0 
    j = 0
    vk = 0
    # 正向计算
    while i < s_max_:
        if i < loc[j]:
            v_lim = matrix[j,1]
        else:
            j += 1
            v_lim = matrix[j,1]
        if vk < v_lim:
            ik = matrix[j,2]
            R = matrix[j,3]
            L = matrix[j,4]
            vk = subway.Qian_yin(vk,ik,R,L,v_lim)[0]
            i += 1
            col = vk
            for k in range(int(col)+1):
                SVEM1[v_max-k-1,i-1] = 1
        else:
            vk = v_lim
            i += 1
            for k in range(int(vk)+1):
                SVEM1[v_max-k-1,i-1] = 1
    
    s_pic = 50
    # dis_x = []
    # dis_y = []
    (ALPHA, BETA, RHO, Q,T) = (1.0,2.0,0.5,100.0,0.033)
    # 28
    length = SVEM1.shape[1]//s_pic+2
    new_mx = np.zeros((SVEM1.shape[0],length))
    # 27
    for i in range(0,length-1):
        new_mx[:,i] = SVEM1[:,i*s_pic]
    new_mx[:,-1] = SVEM1[:,-1]
    # print(SVEM1[:,-1])
    # for i in range(new_mx.shape[1]):
    #     lis = list(new_mx[:,i])
    #     for j in range(len(lis)):
    #         if lis.pop(-1) > 0:
    #             dis_y.append(j+1)
    #             dis_x.append(i+1)
    #         else:
    #             break
    # plt.scatter(dis_x,dis_y)
    # plt.show()
    return SVEM1,new_mx

if __name__ == "__main__":
    # 矩阵写入表格
    import xlwt 
    from Pretreatment import SVEM
    SVEM1,Ju_mx = SVEM()
    filename = xlwt.Workbook() #创建工作簿
    sheet1 = filename.add_sheet(u'sheet1',cell_overwrite_ok=True) #创建sheet
    [h,l]=Ju_mx.shape #h为行数，l为列数
    for i in range (h):
        for j in range (l):
            sheet1.write(i,j,Ju_mx[i,j])
    filename.save('/home/storm/桌面/蚁群存储信息/Ju_mx1.xls')

    plt.matshow(SVEM1)
    plt.matshow(Ju_mx)
    plt.show()


