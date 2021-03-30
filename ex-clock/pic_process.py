from skimage import io
from PIL import Image
import numpy as np
import os
from os import listdir
from numpy import *
import operator

#Standard size 标准大小
N = 32
#灰度阈值
color = 1

#读取训练图片并保存
def GetTrainPicture(files):
    Picture = np.zeros([len(files), N**2])
    #enumerate函数用于遍历序列中的元素以及它们的下标（i是下标，item是元素信息）
    for i, item in enumerate(files):
        #读取这个图片并转为灰度值(黑色字体为0，白底为255)
        img = io.imread('C:/Users/夜了/.vscode/knn/pic/test.png', as_gray = True)
        #img=img.resize((48,48),Image.ANTIALIAS)
        #清除噪音
        img[img<color] = 0
        #将图片进行切割，得到有手写数字的的图像
        img = CutPicture(img)
        #将图片进行拉伸，得到标准大小100x100
        img = StretchPicture(img).reshape(N**2)
        #img = img.reshape(N**2)
        #将图片存入矩阵
        Picture[i, 0:N**2] = img
        #将图片的名字存入矩阵(需要存入名字，上面语句改Picture = np.zeros([len(files), N**2+1]))
        #Picture[i, N**2] = float(item[0])
    return Picture

#切割图象
def CutPicture(img):
    #初始化新大小
    size = []
    #图片的行数
    length = len(img)
    #图片的列数
    width = len(img[0,:])
    #计算新大小
    size.append(JudgeEdge(img, length, 0, [-1, -1]))
    size.append(JudgeEdge(img, width, 1, [-1, -1]))
    size = np.array(size).reshape(4)
    #print('图像尺寸（高低左右）：',size)
    return img[size[0]:size[1]+1, size[2]:size[3]+1]

def JudgeEdge(img, length, flag, size):
    for i in range(length):
        #判断是行是列
        if flag == 0:
            #正序判断该行是否有手写数字
            line1 = img[img[i,:]<color]
            #倒序判断该行是否有手写数字
            line2 = img[img[length-1-i,:]<color]
        else:
            line1 = img[img[:,i]<color]
            line2 = img[img[:,length-1-i]<color]
        #若有手写数字，即到达边界，记录下行
        if len(line1)>=1 and size[0]==-1:
            size[0] = i
        if len(line2)>=1 and size[1]==-1:
            size[1] = length-1-i
        #若上下边界都得到，则跳出
        if size[0]!=-1 and size[1]!=-1:
            break
    return size

#拉伸图像
def StretchPicture(img):
    newImg = np.ones(N**2).reshape(N, N)
    newImg1 = np.ones(N ** 2).reshape(N, N)
    #对每一行/列进行拉伸/压缩
    #每一行拉伸/压缩的步长
    step1 = len(img[0])/N
    #每一列拉伸/压缩的步长
    step2 = len(img)/N
    #对每一行进行操作
    for i in range(len(img)):
        for j in range(N):
            newImg[i, j] = img[i, int(np.floor(j*step1))]
    #对每一列进行操作
    for i in range(N):
        for j in range(N):
            newImg1[j, i] = newImg[int(np.floor(j*step2)), i]
    return newImg1

#用字符矩阵打印图片
def show_ndarray(pic):
    test=open('C:/Users/夜了/.vscode/knn/pic/test.txt','w')

    for i in range(N**2):
	    if(pic[0,i] == 0):
		    print ("1",end='',file=test)
	    else:
		    print ("0",end='',file=test)
	    if (i+1)%N == 0 :
		    print(file=test)

def resize_image(infile, x_s=32,y_s=32):
    """修改图片尺寸
    :param infile: 图片源文件
    :param outfile: 重设尺寸文件保存地址
    :param x_s: 设置的宽度
    :return:
    """
    im = Image.open(infile)
    out = im.resize((x_s, y_s), Image.ANTIALIAS)
    out.save(infile)

def KNN(test_data,train_data,train_label,k=3):
    #已知分类的数据集（训练集）的行数
    dataSetSize = train_data.shape[0]
    #求所有距离：先tile函数将输入点拓展成与训练集相同维数的矩阵，计算测试样本与每一个训练样本的距离
    all_distances = np.sqrt(np.sum(np.square(tile(test_data,(dataSetSize,1))-train_data),axis=1))
    #print("所有距离：",all_distances)
    #按all_distances中元素进行升序排序后得到其对应索引的列表
    sort_distance_index = all_distances.argsort()
    #print("文件索引排序：",sort_distance_index)
    #选择距离最小的k个点
    classCount = {}
    for i in range(k):
        #返回最小距离的训练集的索引(预测值)
        voteIlabel = train_label[sort_distance_index[i]]
        #print('第',i+1,'次预测值',voteIlabel)
        classCount[voteIlabel] = classCount.get(voteIlabel,0)+1
    #求众数：按classCount字典的第2个元素（即类别出现的次数）从大到小排序
    sortedClassCount = sorted(classCount.items(), key = operator.itemgetter(1), reverse = True)
    return sortedClassCount[0][0]

#文本向量化 32x32 -> 1x1024
def img2vector(filename):
    returnVect = []
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect.append(int(lineStr[j]))
    return returnVect

#从文件名中解析分类数字
def classnumCut(fileName):
    #参考文件名格式为：0_3.txt
    fileStr = fileName.split('.')[0]
    classNumStr = int(fileStr.split('_')[0])
    return classNumStr

#构建训练集数据向量，及对应分类标签向量
def trainingDataSet():
    train_label = []
    trainingFileList = listdir('C:/Users/夜了/.vscode/knn/digits/trainingDigits')
    m = len(trainingFileList)
    train_data = zeros((m,1024))
    #获取训练集的标签
    for i in range(m):
        # fileNameStr:所有训练集文件名
        fileNameStr = trainingFileList[i]
        # 得到训练集索引
        train_label.append(classnumCut(fileNameStr))
        train_data[i,:] = img2vector('C:/Users/夜了/.vscode/knn/digits/trainingDigits/%s' % fileNameStr)
    return train_label,train_data

#测试函数
def distinguish():
    #t1 = datetime.datetime.now()  # 计时开始
    #Nearest_Neighbor_number = int(input('选取最邻近的K个值，K='))
    train_label,train_data = trainingDataSet()
    '''
    testFileList = listdir('C:/Users/夜了/.vscode/knn/digits/testDigits')
    error_sum = 0
    test_number = len(testFileList)
    for i in range(test_number):
        #测试集文件名
        fileNameStr = testFileList[i]
        #切片后得到测试集索引
        classNumStr = classnumCut(fileNameStr)
        test_data = img2vector('C:/Users/夜了/.vscode/knn/digits/testDigits/%s' % fileNameStr)
        #调用knn算法进行测试
        '''
    test_data = img2vector('C:/Users/夜了/.vscode/knn/pic/test.txt')
    classifierResult = KNN(test_data, train_data, train_label)
    print("预测的值为：",classifierResult)
    return classifierResult

def work():
#得到在num目录下所有文件的名称组成的列表
    resize_image('C:/Users/夜了/.vscode/knn/pic/test.png')
    filenames = os.listdir(r"C:/Users/夜了/.vscode/knn/pic")
    #得到所有训练图像向量的矩阵
    pic = GetTrainPicture(filenames)
    #print('图像向量的矩阵',pic)
    #调用show_ndarray()函数：用字符矩阵打印图片
    show_ndarray(pic)
    ans=distinguish()
    return ans