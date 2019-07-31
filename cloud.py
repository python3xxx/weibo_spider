import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import os
import numpy as np
import PIL.Image as Image

"""
wordcloud词云  
"""

path = os.getcwd() + '/comment.txt'
content = open(path, encoding='utf-8').read().replace('图片评论', '')\
    .replace('回复', '').replace('等人', '')
alice_coloring = np.array(Image.open('background.jpg'))

my_wordcloud = WordCloud(background_color="white", max_words=2000,
                         mask=alice_coloring,max_font_size=40, random_state=42,
                         font_path='C:\Windows\Fonts\msyh.ttf').generate(content)

image_colors = ImageColorGenerator(alice_coloring)
plt.imshow(my_wordcloud.recolor(color_func=image_colors))
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()

my_wordcloud.to_file('weibo_xiong.png')