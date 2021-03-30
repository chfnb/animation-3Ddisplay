import itertools

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import numbers
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.gridspec import GridSpec
class Animal(object):
    def __init__(self,dataPath,col1,col2,col3,rootDir):
        self.col1 = col1
        self.col2 = col2
        self.col3 = col3
        self.dataPath = dataPath
        self.rootDir = rootDir
        self.initPlot()
        
    #初始化画板
    def initPlot(self):
        self.df = self.readData()
        self.fig = plt.figure(constrained_layout=True,figsize = (8,16))
        gs = GridSpec(3, 2, figure=self.fig)
        #二维绘图对象
        self.axArray = [self.fig.add_subplot(gs[i, :1]) for i in range(3)]
        #三维绘图对象ax4 = fig.add_subplot(gs[0:, -1],projection='3d')
        self.ax4=self.fig.add_subplot(gs[0:, -1],projection='3d')
        self.init2D()
        self.init3D()
    # 2维画图初始化
    def init2D(self):
        lines = []
        xdatas = []
        ydatas = []
        for index,ax in enumerate(self.axArray):
            line, = ax.plot([], [], lw=2)
            ax.set_ylim(min(self.df[self.df.columns[index]]), max(self.df[self.df.columns[index]]))
            ax.set_xlim(0, len(self.df))
            ax.set_ylabel(self.df.columns[index])
            ax.set_xlabel('cnt')
            lines.append(line)
            xdatas.append([])
            ydatas.append([])
        self.init3D()
        # 2维数据，三维画图的数据来源于2维，所以不需要额外保存
        # 2维直线，长度为3
        self.lines = lines
        #横坐标
        self.xdatas = xdatas
        #纵坐标
        self.ydatas = ydatas
    # 3维画图初始化
    def init3D(self):
        # 3d直线初始化
        self._3dLines = self.ax4.plot([],[],[],lw=2)[0]
        #坐标轴初始化
        self.ax4.set_xlim3d(min(self.df[self.df.columns[0]]), max(self.df[self.df.columns[0]]))
        self.ax4.set_xlabel(self.df.columns[0])

        self.ax4.set_ylim3d(min(self.df[self.df.columns[1]]), max(self.df[self.df.columns[1]]))
        self.ax4.set_ylabel(self.df.columns[1])

        self.ax4.set_zlim3d(min(self.df[self.df.columns[2]]), max(self.df[self.df.columns[2]]))
        self.ax4.set_zlabel(self.df.columns[2])
    # 读取数据
    def readData(self):
        def func(x):
            if isinstance(x, numbers.Number)==False:
                return np.nan
            return x
        df = pd.read_excel(self.dataPath)
        arr = [self.col1,self.col2,self.col3]
        df = df[arr]
        for i in arr:
            # 将非数字的异常值改为缺失值
            df[i]=df[i].apply(lambda x:func(x))
            # 将缺失值所在的行剔除
            df.dropna(inplace=True)
        return df[arr]
    # 数据生成器
    def data_gen(self):
        for index in range(len(self.df)):
            data = []  
            for value in self.df.iloc[index]:
                data.append([index, value])
            yield data
    # 二维绘图框架初始化,可以去掉它看看绘出来是什么效果 ，这个函数暂时还不知道为什么会有这个作用  
    def init(self):
        for index in range(len(self.xdatas)):
            self.lines[index].set_data(self.xdatas[index], self.ydatas[index])
        return self.lines
    #画图函数
    def run(self,data):
        # update the data
        for index,value in enumerate(data):
            self.xdatas[index].append(value[0])
            self.ydatas[index].append(value[1])
            self.lines[index].set_data(self.xdatas[index], self.ydatas[index])
        # 前两维为前面两个属性的值
        self._3dLines.set_data(self.ydatas[0],self.ydatas[1])
        # 第三维为第三个属性的值
        self._3dLines.set_3d_properties(self.ydatas[2])
        return self.lines,self._3dLines
    #开始画图
    def draw(self):
        ani = animation.FuncAnimation(self.fig, self.run, self.data_gen, interval=0,save_count=len(self.df),repeat=False,init_func=self.init)
        # ani.save('test.gif')
        plt.show()
if __name__ == "__main__":
    anim = Animal('昌江.xlsx','ID','date','time','')
    anim.draw()