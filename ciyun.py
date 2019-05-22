import wordcloud

with open(r'results.txt','r',encoding='utf-8') as f:
    content_list=f.read()
    #print(type(content_list))

from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
#from scipy.misc import
import imageio

back_group=imageio.imread('back1.png')
wc=WordCloud(background_color='white',
             mask=back_group,
             font_path='C:\Windows\Fonts\simkai.ttf',

             max_font_size=60,
             min_font_size=3,
             )

wc_color=wc.generate(content_list)
ciyun_color=ImageColorGenerator(back_group)
new_color=wc.recolor(color_func=ciyun_color)
plt.imshow(new_color)
plt.axis('off')
plt.savefig('ciyun_pic.jpg')
