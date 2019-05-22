import jieba

# 初始化停用词列表
stopwords = [line.strip() for line in open('stopwords.txt',encoding='UTF-8').readlines()]

# 对句子进行中文分词
def seg_depart(sentence):
    # 对文档中的每一行进行中文分词
    sentence_depart = jieba.cut(sentence.strip())
    # 输出结果为outdata
    outdata = ''
    # 去停用词
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outdata += word
                outdata += " "
    return outdata

# 给出输入输出文档路径
filename = "content_label.txt"
outfilename = "results_label.txt"
inputs = open(filename, 'r', encoding='UTF-8')
outputs = open(outfilename, 'w', encoding='UTF-8')

# 调用seg_depart函数，将输出结果写入ou.txt中
for line in inputs:
    line_seg = seg_depart(line)
    outputs.write(line_seg + '\n')

outputs.close()
inputs.close()
print("恭喜！分词以及删除停用词成功！")