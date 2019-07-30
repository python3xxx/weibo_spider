import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt

path = os.getcwd() + '/comment.txt'
# 读signature.txt文本内容
content = open(path, encoding='utf-8').read().replace('图片评论', '')\
    .replace('回复', '').replace('等人', '')

# 词云配置
wc = WordCloud(
    # 背景色
    background_color='white',
    # 最大显示的词数
    max_words=1000,
    height=500,
    width=500,
    # worldcloud 本身不支持中文，需要指定字体文件路径
    font_path='C:\Windows\Fonts\msyh.ttf',
    max_font_size=60,
    # 随机配色方案数
    random_state=30,
).generate(content)

plt.imshow(wc)
plt.axis('off')
plt.show()
wc.to_file('signature_cloud.png')