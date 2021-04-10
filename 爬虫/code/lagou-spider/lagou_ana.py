import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from scipy.misc import imread
import jieba
from pylab import mpl

# 使matplotlib模块能显示中文
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# 读取数据
df = pd.read_csv(open('lagou_jobs.csv', encoding='gbk'))

# 数据清洗,剔除实习岗位
df.drop(df[df['职位名称'].str.contains('实习')].index, inplace=True)
# print(df.describe())

# 由于CSV文件内的数据是字符串形式,先用正则表达式将字符串转化为列表,再取区间的均值
# 在字符串中找到正则表达式所匹配的所有子串，并返回一个列表
pattern = '\d+'
df['工作年限'] = df['工作经验'].str.findall(pattern)

avg_work_year = []
for i in df['工作年限']:
    # 如果工作经验为'不限'或'应届毕业生',那么匹配值为空,工作年限为0
    if len(i) == 0:
        avg_work_year.append(0)
    # 如果匹配值为一个数值,那么返回该数值
    elif len(i) == 1:
        avg_work_year.append(int(''.join(i)))
    # 如果匹配值为一个区间,那么取平均值
    else:
        num_list = [int(j) for j in i]
        avg_year = sum(num_list) / 2
        avg_work_year.append(avg_year)

df['经验'] = avg_work_year

# 将字符串转化为列表,再取区间的前25%，比较贴近现实
df['salary'] = df['工资'].str.findall(pattern)

avg_salary = []
for k in df['salary']:
    int_list = [int(n) for n in k]
    avg_wage = int_list[0] + (int_list[1] - int_list[0]) / 4
    avg_salary.append(avg_wage)

df['月工资'] = avg_salary
# 将清洗后的数据保存,以便检查
df.to_csv('draft.csv', index=False)

# 描述统计  对数据分析师工资进行简单的统计，并打印出来
print('数据分析师工资描述：\n{}'.format(df['月工资'].describe( )))

# 绘制频率直方图并保存
plt.hist(df['月工资'], bins=12)
plt.xlabel('工资 (千元)')
plt.ylabel('频数')
plt.title("工资直方图")
plt.savefig('histogram.jpg')
plt.show( )

# 绘制饼图并保存
# 计算区域中地区出现的频数的数组
count = df['区域'].value_counts( )
print(count)
# (每一块)的比例，如果sum(x) > 1会使用sum(x)归一化
plt.pie(count, labels=count.keys( ), labeldistance=1.4, autopct='%2.1f%%')
plt.axis('equal')  # 使饼图为正圆形
plt.legend(loc='upper left', bbox_to_anchor=(-0.1, 1))  # 设置图例的位置
plt.savefig('pie_chart.jpg')
plt.show( )

# 绘制词云,将职位福利中的字符串汇总
text = ''
for line in df['职位福利']:
    text += line
# 使用jieba模块将字符串分割为单词列表
cut_text = ' '.join(jieba.cut(text))
print(cut_text)
color_mask = imread('wordcloud.jpg')  # 设置词云背景图
font = r'C:\Windows\Fonts\simhei.ttf'
cloud = WordCloud(
    font_path=font,
    background_color='white',
    mask=color_mask,
    max_words=1000,
    max_font_size=100
)

word_cloud = cloud.generate(cut_text)
# 保存词云图片
word_cloud.to_file('word_cloud.jpg')
plt.imshow(word_cloud)
plt.axis('off')
plt.show()
