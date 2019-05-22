import jieba
import numpy as np

def judge(n):
    return n

def sentiment_grade_lists(data_set):
    split_sentence = data_set.split('。') #以句号切割
    count1 = []
    count2 = []
    for sen in split_sentence:  # 循环遍历每一个评论
        fenci_result = jieba.lcut(sen, cut_all=False)  # 把句子进行分词，以列表的形式返回
        #print(fenci_result)
        i = 0  # 记录扫描到的词的位置
        a = 0  # 记录情感词的位置
        positive_count1 = 0  # 积极词的第一次分值
        positive_count2 = 0  # 积极词反转后的分值
        positive_count3 = 0  # 积极词的最后分值（包括叹号的分值）
        negtive_count1 = 0
        negtive_count2 = 0
        negtive_count3 = 0

        neg_dict = [line.strip() for line in open('negative.txt', encoding='UTF-8').readlines()]
        pos_dict = [line.strip() for line in open('positive.txt', encoding='UTF-8').readlines()]
        most_dict = [line.strip() for line in open('most_dict.txt', encoding='UTF-8').readlines()]
        very_dict = [line.strip() for line in open('very_dict.txt', encoding='UTF-8').readlines()]
        more_dict = [line.strip() for line in open('more_dict.txt', encoding='UTF-8').readlines()]
        ish_dict = [line.strip() for line in open('ish_dict.txt', encoding='UTF-8').readlines()]
        deny_dict = [line.strip() for line in open('deny_dict.txt', encoding='UTF-8').readlines()]

        #print(fenci_result)
        for word in fenci_result:
            if word in pos_dict:  # 判断词语是否是情感词
                positive_count1 += 1
                c = 0
                for w in fenci_result[a:i]:  # 扫描情感词前的程度词
                    if w in most_dict:
                        positive_count1 *= 4.0
                    elif w in very_dict:
                        positive_count1 *= 3.0
                    elif w in more_dict:
                        positive_count1 *= 2.0
                    elif w in ish_dict:
                        positive_count1 *= 0.5
                    elif w in deny_dict:
                        c += 1
                if judge(c) == 'odd':  # 扫描情感词前的否定词数
                    positive_count1 *= -1.0
                    positive_count2 += positive_count1
                    positive_count1 = 0
                    positive_count3 = positive_count1 + positive_count2 + positive_count3
                    positive_count2 = 0
                else:
                    positive_count3 = positive_count1 + positive_count2 + positive_count3
                    positive_count1 = 0
                a = i + 1  # 情感词的位置变化

            elif word in neg_dict:  # 消极情感的分析，与上面一致
                negtive_count1 += 1
                d = 0
                for w in fenci_result[a:i]:
                    if w in most_dict:
                        negtive_count1 *= 4.0
                    elif w in very_dict:
                        negtive_count1 *= 3.0
                    elif w in more_dict:
                        negtive_count1 *= 2.0
                    elif w in ish_dict:
                        negtive_count1 *= 0.5
                    elif w in deny_dict:
                        d += 1
                if judge(d) == 'odd':
                    negtive_count1 *= -1.0
                    negtive_count2 += negtive_count1
                    negtive_count1 = 0
                    negtive_count3 = negtive_count1 + negtive_count2 + negtive_count3
                    negtive_count2 = 0
                else:
                    negtive_count3 = negtive_count1 + negtive_count2 + negtive_count3
                    negtive_count1 = 0
                a = i + 1
            elif word == '！' or word == '!':  ##判断句子是否有感叹号
                for w2 in fenci_result[::-1]:  # 扫描感叹号前的情感词，发现后权值+2，然后退出循环
                    if w2 in pos_dict or neg_dict:
                        positive_count3 += 2
                        negtive_count3 += 2
                        break
            i += 1  # 扫描词位置前移

            # 以下是防止出现负数的情况
            pos_count = 0
            neg_count = 0
            if positive_count3 < 0 and negtive_count3 > 0:
                neg_count += negtive_count3 - positive_count3
                pos_count = 0
            elif negtive_count3 < 0 and positive_count3 > 0:
                pos_count = positive_count3 - negtive_count3
                neg_count = 0
            elif positive_count3 < 0 and negtive_count3 < 0:
                neg_count = -positive_count3
                pos_count = -negtive_count3
            else:
                pos_count = positive_count3
                neg_count = negtive_count3

            count1.append([pos_count, neg_count])
        count2.append(count1)
        count1 = []
    return count2

def sentiment_grade(senti_grade_lists):
    score = []
    for review in senti_grade_lists:
        score_array = np.array(review)
        Pos = np.sum(score_array[:, 0])
        Neg = np.sum(score_array[:, 1])
        AvgPos = np.mean(score_array[:, 0])
        AvgPos = float('%.1f' % AvgPos)
        AvgNeg = np.mean(score_array[:, 1])
        AvgNeg = float('%.1f' % AvgNeg)
        StdPos = np.std(score_array[:, 0])
        StdPos = float('%.1f' % StdPos)
        StdNeg = np.std(score_array[:, 1])
        StdNeg = float('%.1f' % StdNeg)
        score.append([Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg])

    return score

f = open(r"results.txt",encoding ='utf-8')#打开已经分好词的文件
line = f.readlines() #读取每一行
data_list = [] #初始化列表
while line:
    data_list.append(line)
    line = f.readlines()
    #print(data_list)
    data = str(data_list) #强制转换数据类型，化为字符串类型
f.close() #关闭文件
print(sentiment_grade(sentiment_grade_lists(data))) #打印整个情感分析结果
#结果列表里面参数解释： 第一个参数代表褒义权值分数，第二个是贬义权值分数。

#以下是功能准确率测试，采用单句结果，要用时可以去掉注释。
'''
data1 = '很好，主要比较符合自己的爱好。满足我的需求了!'
data2 = '外观现在比之前好看了，很多了，尤其是现在的样子是我很喜欢的。颜色我也喜欢，感觉比白色的洋气多了，看着都舒服！'
data3 = '空间够大，还有外形也好看，出去自驾游啥的方便，行车视野好 '
data4 = '空间是我最喜欢的地方，无论是前排还是后排，个子高的人也不觉得压抑，宽敞的 '
data5 = '隔音效果稍微差了点，油耗稍微高了点  '

print(sentiment_grade(sentiment_grade_lists(data1)))
print(sentiment_grade(sentiment_grade_lists(data2)))
print(sentiment_grade(sentiment_grade_lists(data3)))
print(sentiment_grade(sentiment_grade_lists(data4)))
print(sentiment_grade(sentiment_grade_lists(data5)))
'''




