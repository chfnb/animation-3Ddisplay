#利用三维轴方法
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd #调用pandas库来读取excel文件
import seaborn as sns
import numpy as np
import numbers
import time
class A(object):
    def __init__(self,dataPath,col1,col2,col3,rootDir):
        self.col1 = col1
        self.col2 = col2
        self.col3 = col3
        self.dataPath = dataPath
        self.rootDir = rootDir
    def getImages(self):
        #读取数据
        df=pd.read_excel(self.dataPath)
        arr = [self.col1,self.col2,self.col3]
        for i in arr:
        # 将非数字的异常值改为缺失值
            df[i]=df[i].apply(lambda x:self.func(x))
        # 将缺失值所在的行剔除
        df.dropna(axis='rows')
        #定义图像和三维格式坐标轴
        fig=plt.figure()
        ax1=Axes3D(fig)
        # #定义三维数据
        x = df[self.col1]
        y = df[self.col2]
        z = df[self.col3]
        ax1.plot3D(x,y,z)    #绘制折线图

        # 设置轴坐标轴Label
        ax1.set_xlabel(arr[0])
        ax1.set_ylabel(arr[1])
        ax1.set_zlabel(arr[2])
        # 保存图片
        imageName =  'image/'+str(time.time())+'_3D.png'
        plt.savefig(self.rootDir+imageName)
        # plt.show()
        return imageName

    # 判断变量是否是数字 非数字改为缺失值   
    def func(self,x):
        if isinstance(x, numbers.Number)==False:
            return np.nan
        return x

if __name__ == "__main__":
    '''import sys
    if len(sys.argv) != 6:
        raise  RuntimeError('传递进来的参数个数不是5个')
    dataName = sys.argv[1] + '.xlsx'
    rootDir = sys.argv[5]
    dataPath = rootDir +  dataName
    attr1 = sys.argv[2]
    attr2 = sys.argv[3]
    attr3 = sys.argv[4]
    a = A(dataPath,attr1,attr2,attr3,rootDir)'''
    b = A('昌江.xlsx','ID','date','time','E:/Document/python/threedimension/')
    print(b.getImages())


