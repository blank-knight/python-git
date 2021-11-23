# -*- coding: utf-8 -*-  
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
# test = np.array([[1,2,3],
#                  [4,5,6],
#                  [7,8,9]])
# for i in test:
#     print(i)
from Pretreatment import SVEM
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"C:\Windows\Fonts\msyh.ttf",size=10)
SVEM1,Ju_mx = SVEM()

solu_x = []
solu_y = []
k = 0
for i in range(Ju_mx.shape[1]):
    for j in Ju_mx[:,i]:
        k += 1
        if j == 1:
            solu_x.append(i*50)
            solu_y.append(80-k)
            k = 0
            break

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.title("ene-factor:2,time-factor:1,imf-factor:0.5")
plt.text(0,80,'ant-num:1,loop-num:10,time-lim:198')
plt.plot(solu_x,solu_y)
plt.show()