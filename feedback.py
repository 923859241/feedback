# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 01:34:36 2020

@author: 92385
"""

import xlrd
import xlwt
import jieba
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

def dataClean():
    #语料集
    validData = []
    invalidData =[]
    
    dataMeipai = xlrd.open_workbook('meipai.xlsx')
    dataVivo = xlrd.open_workbook('vivo.xlsx')
    
    sheelData = dataVivo.sheet_by_index(0)
    for rowI in range(1,sheelData.nrows):
        seg_list = jieba.cut( str(sheelData.cell(rowI, 9).value), cut_all=True)
        if(sheelData.cell(rowI, 11).value==1):
            validData.append("".join(seg_list))
        else:
            invalidData.append("".join(seg_list))
            
    # sheelData = dataMeipai.sheet_by_index(0)
    # for rowI in range(1,sheelData.nrows):
    #     seg_list = jieba.cut( str(sheelData.cell(rowI, 9).value), cut_all=True)
    #     if(sheelData.cell(rowI, 15).value==1):
    #         validData.append("".join(seg_list))
    #     else:
    #         invalidData.append("".join(seg_list))
    
    
    return validData,invalidData
    

if __name__ == "__main__":
    #基本思路，重点是过滤无效反馈，留下有效反馈，所以对无法判断是否为有效反馈的时候（没有该词向量）
    #则默认为有效反馈
    validData,invalidData = dataClean()
    
    #将文本中的词语转换为词频矩阵
    vectorizer = CountVectorizer()
    #计算个词语出现的次数
    XX = vectorizer.fit_transform(invalidData).toarray()
    #获取词袋中所有文本关键词
    invalidWord = vectorizer.get_feature_names()
    ascllData = [chr(i) for i in range(0,127)]
    
    allInvalid = 0
    
    for dataI in validData:
        countAscall = 0
        allCount = 1
        #逐个词分割
        for splitI in list(dataI):
            #是否在ascall内
            allCount+=1
            if splitI in ascllData:
                countAscall+=1
                
        #判断后输出
        if countAscall/allCount > 1/3:
            allInvalid += 1
            print(dataI)
            #print(countAscall/allCount)
    
    #对存在ascall码词语占总词语1/3的句子，直接过滤了77% 有效反馈不会被过滤
    #对于meipai的无效反馈过滤60.5%，有效反馈不会被过滤
    
    
    
    #查看词频结果
    
#    vectorizer = CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
#    transformer = TfidfTransformer()#该类会统计每个词语的tf-idf权值
#    tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
#    word=vectorizer.get_feature_names()#获取词袋模型中的所有词语
#    
#    corpus=["我 来到 北京 清华大学",#第一类文本切词后的结果，词之间以空格隔开
#		"他 来到 了 网易 杭研 大厦",#第二类文本的切词结果
#		"小明 硕士 毕业 与 中国 科学院",#第三类文本的切词结果
#		"我 爱 北京 天安门"]#第四类文本的切词结果
#    vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
#    transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值
#    tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
#    word=vectorizer.get_feature_names()#获取词袋模型中的所有词语
#    weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
#    for i in range(len(weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
#        print("-------这里输出第",i,u"类文本的词语tf-idf权重------")
#        for j in range(len(word)):
#            print (word[j],weight[i][j])
