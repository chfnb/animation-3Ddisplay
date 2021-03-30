'''
数据预处理类
'''
import numpy as np
from numpy.core.defchararray import array
class pretreatment(object):
    def __init__(self):
        pass
    # 归一化
    def normalization(self,df):
        return 2*(df-np.min(df,axis=0)) / (np.max(df,axis=0)-np.min(df,axis=0))-1
    # 剔除异常值 3-sigma
    def removeOutliers(self,df):
        left = np.mean(df,axis=0) - 3 * np.std(df,axis=0)
        right = np.mean(df,axis=0) + 3 * np.std(df,axis=0)
        return df[(left<df) & (df<right)].dropna()
    #插值，前后平均值
    def interpolation(df):
        for column in df.columns:
            for i in range(len(df[column])):
                if np.isnan(df[column][i]):
                    if i-1 >=0 and i+1 < len(df[column]):
                        df[column][i] = (df[column][i-1]+df[column][i+1])/2
                    elif i-1 >=0:
                        df[column][i] = df[column][i-1]
                    else:
                        df[column][i] = df[column][i+1]
        
if __name__ == "__main__":
    p = pretreatment()
    print(p.removeOutliers(np.array([[1,3,45,6],[6,8,1,3],[7,8,12,3]])))
