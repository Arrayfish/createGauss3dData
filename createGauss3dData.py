from scipy.stats import multivariate_normal
import random
import numpy as np
import pandas as pd
MEANS = np.array([
    [1, 1, 1],
    [1, -1, -1],
    [-1, 1, -1],  
    [-1, -1, 1]
])
classNum = 3
allClassNum = classNum + 1
trainClassDataNum = 1000
testClassDataNum = 1000
classDataNum = trainClassDataNum + testClassDataNum
dataNum = trainClassDataNum*allClassNum + testClassDataNum*allClassNum

def main():
    point_np, oneHotTrain_np, oneHotTest_np = createPoints()
    point_np = normalize_data(point_np)
   
    for cls in range(classNum):
        if cls == 0:
            trainData_np = point_np[classDataNum *cls:classDataNum * cls + trainClassDataNum]
        else:
            trainData_np = np.append(trainData_np, point_np[classDataNum *cls:classDataNum * cls + trainClassDataNum], axis=0)
    for cls in range(allClassNum):
        if cls == 0:
            testData_np = point_np[classDataNum * cls + trainClassDataNum:classDataNum * (cls + 1)]
        else:
            testData_np = np.append(testData_np, point_np[classDataNum * cls + trainClassDataNum:classDataNum * (cls + 1)], axis=0)
    pd.DataFrame(trainData_np).to_csv("easy3dData.csv", header=None, index=None)
    pd.DataFrame(oneHotTrain_np).to_csv("easy3dLabel.csv", header=None, index=None)
    pd.DataFrame(testData_np).to_csv("easy3dTestData.csv", header=None, index=None)
    pd.DataFrame(oneHotTest_np).to_csv("easy3dTestLabel.csv", header=None, index=None)

def normalize_data(point_np):
    min_np = np.min(point_np, axis=0)
    max_np = np.max(point_np, axis=0)
    # print(max_np,min_np)
    point_np = (point_np - min_np) / (max_np - min_np)
    # print(len(np.sum(point_np, axis=1)))

    for i in range(len(point_np)):
        point_np[i] = point_np[i] / np.sum(point_np[i])

    return point_np

# 点群作成
def createPoints():
    covar_np = np.zeros((allClassNum, 3, 3))
    for i in range(allClassNum):
        for row in range(3):
            for col in range(row, 3):
                covar_np[i][row][col] = random.random()
                covar_np[i][row][col] = covar_np[i][col][row]
        if np.linalg.det(covar_np[i]) < 0:
            i = i - 1
    point_np = np.array([])
    for cls in range(allClassNum):
        clsPoint_np = np.array(multivariate_normal(mean=MEANS[cls], cov=covar_np[cls]).rvs(size=dataNum))
        if cls == 0:
            point_np = clsPoint_np
        else:
            point_np = np.concatenate([point_np,clsPoint_np])
    # pd.DataFrame(point_np).to_csv("easy3dData.csv", header=None, index=None)
    # 
    oneHotTrain_np = np.zeros((trainClassDataNum * classNum, classNum), dtype="int64")
    oneHotTest_np = np.zeros((testClassDataNum * allClassNum, allClassNum), dtype="int64")
    for i in range(classNum):
        oneHotTrain_np[trainClassDataNum * i:trainClassDataNum * (i + 1), i] = 1

    oneHotTest_np[testClassDataNum * classNum: testClassDataNum * (classNum + 1), 0] = 1
    for i in range(classNum):
        oneHotTest_np[testClassDataNum * i: testClassDataNum * (i + 1), i + 1] = 1
    #pd.DataFrame(oneHot_np).to_csv("easy3dDatalabel.csv",header=None,index=None)
    return point_np, oneHotTrain_np, oneHotTest_np


if __name__ == "__main__":
    main()