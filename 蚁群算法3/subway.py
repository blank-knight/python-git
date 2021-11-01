import numpy as np
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
        try:
            if 0 <= v <= 51.5:
                return 203
            elif 51.5 < v <= 80:
                return -0.002032*v*v*v+0.4928*v*v-41.23*v+1343
        except:
            print("速度不符合要求")
        
    
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

    '''
        定义各个行为
    '''
    # 其中ik为坡度，Rk为曲线半径，Lk为隧道长度
    def Qian_yin(self,vk,ik,Rk,Lk,v_lim):
        E_q = 0
        t = 0
       
        for i in range(100):
            if vk <= v_lim-1:
                F_k = self.f_F(vk)  
                W_k = self.W_calculate(vk,ik,Rk,Lk)   
                vk = pow(vk/3.6*vk/3.6+2*(F_k-W_k)/self.M*self.s,1/2)*3.6  
                E_q += F_k*self.s
                t += self.s/1000/vk
            else:
                return v_lim,E_q,t
        return vk,E_q,t


    def Zhi_dong(self,vk,ij,Rj,Lj,v_lim):
        for i in range(100):
            if vk < v_lim:
                B_j = self.f_B(vk)
                W_j = self.W_calculate(vk,ij,Rj,Lj)
                a = (B_j+W_j)/self.M
                # 因为制动最后速度一定为0，所以这里速度是从后往前推的,因为制动只在构建反
                # 向矩阵中调用，所以这里变为加速
                vk = pow(vk/3.6*vk/3.6+2*a*self.s,1/2)*3.6
            else:
                return vk
        return vk
    
    
    
    