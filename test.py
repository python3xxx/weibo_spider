
# wordcloud词云  
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import os
import numpy as np
import PIL.Image as Image


path = os.getcwd() + '/comment.txt'
# 读signature.txt文本内容
content = open(path, encoding='utf-8').read().replace('图片评论', '')\
    .replace('回复', '').replace('等人', '')
#d = os.path.dirname(__file__)  
#找一张微信logo图来生成配色方案,微信logo图wechat.jpg路径在F:\\盘下  
# alice_coloring = np.array(Image.open('cloud_backgroud.jpg'))
alice_coloring = np.array(Image.open('backgroud.jpg'))
# 这里要选择字体存放路径，win的字体在C:/windows／Fonts中  

my_wordcloud = WordCloud(background_color="white", max_words=2000,
                         mask=alice_coloring,max_font_size=40, random_state=42,
                         font_path='C:\Windows\Fonts\msyh.ttf') \
.generate(content)

image_colors = ImageColorGenerator(alice_coloring)
plt.imshow(my_wordcloud.recolor(color_func=image_colors))
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()

# 保存图片到F:\\盘下 并发送到手机里的文件传输助手(filehelper)里  
my_wordcloud.to_file('weibo_xiong.png')
