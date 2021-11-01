import numpy as np
import xlrd
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
'''
    单位统一：时间：h，力：KN，能量：KJ，距离：m，速度：km/h,加速度：m/s^2
'''
class subway:
    def __init__(self) -> None:
        self.M = 194.295
        self.A = 2.031
        self.B = 0.0622
        self.C = 0.001807
        self.c = 600
        self.s = 0.01
        self.s_sli = 50
        self.g = 9.98

    # KN
    def f_F(self,v):
        if 0 <= v <= 51.5:
            return 203
        elif 51.5 < v <= 80:
            return -0.002032*v*v*v+0.4928*v*v-41.23*v+1343
        else:
            print("请输入0到80的速度参数")
    
    # KN
    def f_B(self,v):
        try:
            if 0 <= v <= 77:
                return 166
            elif 77 < v <= 80:
                return 0.1343*v*v-25.07*v+1300
        except:
            print("速度不符合要求")
    # KN
    def W_calculate(self,v,i,R,L):
        if R == 0:
            W = (self.A+self.B*v+self.C*pow(v,2)+i+0.00013*L)\
                *self.M*self.g*pow(10,-3) 
        elif R > 0:
            W = (self.A+self.B*v+self.C*pow(v,2)+i+self.c/R+\
                0.00013*L)*self.M*self.g*pow(10,-3)
        return W

      # start,end为开始段和结束段
    def QY_change(self,start,end,vk,matrix):
        E_q = 0
        t = 0
        loc_ = list(matrix[:,0])
        for i in range(0,len(loc_)):
            ik = matrix[i,2]
            R = matrix[i,3]
            L = matrix[i,4]
            v_limit = matrix[i,1]
            if end > loc_[i]:
                for j in range(start*100,loc_[i]*100):
                    if vk > v_limit:
                        return vk,E_q,t
                    else:
                        F_k = self.f_F(vk)  
                        W_k = self.W_calculate(vk,ik,R,L)   
                        vk = pow(vk/3.6*vk/3.6+2*(F_k-W_k)/self.M*self.s,1/2)*3.6  
                        E_q += F_k*self.s
                        t += self.s/1000/vk
                start = loc_[i]
            elif end < loc_[i]:
                for j in range(start*100,end*100-start*100):
                    if vk > v_limit:
                        return vk,E_q,t
                    else:
                        F_k = self.f_F(vk)  
                        W_k = self.W_calculate(vk,ik,R,L)   
                        vk = pow(vk/3.6*vk/3.6+2*(F_k-W_k)/self.M*self.s,1/2)*3.6  
                        E_q += F_k*self.s
                        t += self.s/1000/vk
                return vk,E_q,t
            
    def XH_change(self,start,end,vk,matrix):
        E_q = 1
        t = (end-start)/1000/vk
        loc_ = list(matrix[:,0])
        for i in range(0,len(loc_)):
            ik = matrix[i,2]
            R = matrix[i,3]
            L = matrix[i,4]
            # 双指针进行判断
            if start <= loc_[i]and end >= loc_[i]:
                for j in range(start*100,loc_[i]*100):
                    W_k = self.W_calculate(vk,ik,R,L)
                    if W_k >= 0:
                        F_k = W_k
                        E_q += F_k*self.s
                        t += self.s/1000/vk
                    else:
                        B_k = -W_k
                start = loc_[i]
            elif start <= loc_[i] and end <= loc_[i]:
                for j in range(start*100,end*100):
                    W_k = self.W_calculate(vk,ik,R,L)
                    if W_k >= 0:
                        F_k = W_k
                        E_q += F_k*0.01
                        t += self.s/1000/vk
                    else:
                        B_k = -W_k
                return vk,E_q,t
            

    def DX_change(self,start,end,vk,matrix):
        t = 0
        loc_ = list(matrix[:,0])
        for i in range(0,len(loc_)):
            v_limit = matrix[i,1]
            ik = matrix[i,2]
            R = matrix[i,3]
            L = matrix[i,4]
            if start <= loc_[i] and end >= loc_[i]:
                for j in range(start*100,loc_[i]*100):
                    if vk < v_limit and vk >= 0:
                        W_k = self.W_calculate(vk,ik,R,L)
                        a = -W_k/self.M
                        t += self.s/1000/vk
                        vk = pow(vk/3.6*vk/3.6+2*a*self.s,1/2)*3.6
                    else:
                        return -1,1,t
                start = loc_[i]
            elif start <= loc_[i] and end <= loc_[i]:
                for j in range(start*100,end*100):
                    if vk < v_limit and vk >= 0:
                        W_k = self.W_calculate(vk,ik,R,L)
                        a = -W_k/self.M
                        t += self.s/1000/vk
                        vk = pow(vk/3.6*vk/3.6+2*a*self.s,1/2)*3.6
                    else:
                        return -1,0,t
                return vk,1,t

    def ZD_change(self,start,end,vk,matrix):
        t = 0
        loc_ = list(matrix[:,0])
        for i in range(0,len(loc_)):
            ik = matrix[i,2]
            R = matrix[i,3]
            L = matrix[i,4]
            if start <= loc_[i] and end > loc_[i]:
                for j in range(start*100,loc_[i]*100):
                    B_j = self.f_B(vk)
                    W_j = self.W_calculate(vk,ik,R,L)
                    a = (B_j+W_j)/self.M
                    t += self.s/1000/vk
                    vk = pow(vk/3.6*vk/3.6-2*a*self.s,1/2)*3.6
                start = loc_[i]
            elif start <= loc_[i] and end <= loc_[i]:
                for j in range(start*100,loc_[i]*100):
                    if np.isnan(vk) or vk < 0:
                        return -1,0,t,4
                    B_j = self.f_B(vk)
                    W_j = self.W_calculate(vk,ik,R,L)
                    a = (B_j+W_j)/self.M
                    t += self.s/1000/vk
                    # print("vk/3.6*vk/3.6:",vk/3.6*vk/3.6)
                    # print("2*a*self.s",2*a*self.s)
                    # print("vk是:",vk)
                    # bug 处
                    vk = pow(vk/3.6*vk/3.6-2*a*self.s,1/2)*3.6
                    # print("Pow后vk:",vk)
                return vk,1,t,4    


    '''
        定义各个行为
    '''
    # 其中ik为坡度，Rk为曲线半径，Lk为隧道长度
    def Qian_yin(self,start,end,vk,ik,Rk,Lk,mx,v_lim):
        E_q = 0
        t = 0
        # 判断是否会50m的区间内路况是否有变化
        if np.where(mx[:,0]>start)[0][0] == np.where(mx[:,0]>end)[0][0]:
            for i in range(self.s_sli*100):
                if vk > v_lim:
                    return v_lim+1,0,0
                F_k = self.f_F(vk)  
                W_k = self.W_calculate(vk,ik,Rk,Lk)   
                vk = pow(vk/3.6*vk/3.6+2*(F_k-W_k)/self.M*self.s,1/2)*3.6  
                E_q += F_k*self.s
                t += self.s/1000/vk
            return vk,E_q,t
        else:
            return self.QY_change(start,end,vk,mx)


    def Xun_hang(self,start,end,vk,ik,Rk,Lk,mx):
        F_k,B_k,E_q,t = 0,0,1,0
        if np.where(mx[:,0]>start)[0][0] == np.where(mx[:,0]>end)[0][0]:
            for i in range(self.s_sli*100):
                W_k = self.W_calculate(vk,ik,Rk,Lk)
                if W_k >= 0:
                    F_k = W_k
                    E_q += F_k*self.s
                    t += self.s/1000/vk
                else:
                    B_k = -pow(W_k,-3)
            return vk,E_q,t
        else:
            return self.XH_change(start,end,vk,mx)

    def Duo_xing(self,start,end,vk,ij,Rj,Lj,mx,v_lim):
        t = 0
        if np.where(mx[:,0]>start)[0][0] == np.where(mx[:,0]>end)[0][0]:
            for i in range(self.s_sli*100):
                if vk > v_lim:
                    return v_lim+1,0,0
                if vk >= 0: 
                    W_k = self.W_calculate(vk,ij,Rj,Lj)
                    a = -W_k/self.M
                    t += self.s/1000/vk
                    vk = pow(vk/3.6*vk/3.6+2*a*self.s,1/2)*3.6
                else:
                    return -1,1,t
            return vk,1,t
        else:
            return self.DX_change(start,end,vk,mx)

    def Zhi_dong(self,start,end,vk,ij,Rj,Lj,mx):
        t = 0
        if np.where(mx[:,0]>start)[0][0] == mx.shape[0]:
            for i in range((end-start)*100):
                B_j = self.f_B(vk)
                W_j = self.W_calculate(vk,ij,Rj,Lj)
                a = (B_j+W_j)/self.M
                t += self.s/1000/vk
                # 因为制动最后速度一定为0，所以这里速度是从后往前推的,因为制动只在构建反
                # 向矩阵中调用，所以这里变为加速
                vk = pow(vk/3.6*vk/3.6-2*a*self.s,1/2)*3.6
            return vk,1,t,4
        else:
            return self.ZD_change(start,end,vk,mx)
    
if __name__ == "__main__":
    test = subway()
    # t = 0
    # vk = pow(0.006390499495941598-0.01809520898732445,1/2)*3.6
    # if isinstance(vk,complex) or vk < 0:
    #     print("eeee")
    # # if vk < 0:
    # #     print("fafafa")
    # i = 14
    # B_j = test.f_B(vk)
    # ik = matrix[i,2]
    # R = matrix[i,3]
    # L = matrix[i,4]
    # W_j = test.W_calculate(vk,ik,R,L)
    # a = (B_j+W_j)/test.M
    # t += test.s/1000/vk
    # # bug 处
    # vk = pow(vk/3.6*vk/3.6-2*a*test.s,1/2)*3.6
    print(test.Xun_hang(350,400,31,-8,0,0,matrix))