from wordcloud import WordCloud
import matplotlib.pyplot as plt
from scipy.misc import imread
import re
import numpy
import jieba
import jieba.analyse
import pandas as pd
class Generate_Wrdcld():
    '''
    Configure:
        words_filepath
        newwords_addlist
        stopwords_addlist
        correctwords_list
        bg_pic_filepath : background picture
        zh_font : zh-font file path
        wrdcld_picpath
    '''
    words_filepath = "./crawed/Comments_content.txt"
    stopwords_filepath = "./configure/stopwords.txt"
    newwords_addlist = ["今敏","牛逼","梦境","想象力","天马行空","红辣椒","盗梦空间","文科生","工科生"]
    stopwords_addlist = ["这部","这片","像是","终于","一个","太","之事"]
    correctwords_list = ["天马行空","无所不能","玻璃窗","想象力"]
    delwords_list = ["马行","行空","马行空","天马"]
    bg_pic_filepath = "./configure/alice_color.png"
    zh_font = "./configure/simhei.ttf"
    wrdcld_picpath = './analysis/Paprika.png'
    def __init__(self,*args):
        self.content = open(Generate_Wrdcld.words_filepath,'r').read()
        self.bg_pic = imread(Generate_Wrdcld.bg_pic_filepath)
        self.myWordDict()
        self.correct_words()
        self.del_words()
    def myWordDict(self):
        for new in Generate_Wrdcld.newwords_addlist:
            jieba.add_word(new,freq=10000)
        return None
    def correct_words(self):
        for word in Generate_Wrdcld.correctwords_list:
            jieba.suggest_freq(word,tune = True)
        return None
    def del_words(self):
        for word in Generate_Wrdcld.delwords_list:
            jieba.del_word(word)
        return None
    def myStopwordDict(self):
        stopwords_list = pd.read_csv(Generate_Wrdcld.stopwords_filepath,
                                     index_col=False,
                                     quoting=3,
                                     sep="\t",
                                     names=['stopword'],
                                     encoding='utf-8'
                                     )
        for new in Generate_Wrdcld.stopwords_addlist:
            stopwords_list.loc[stopwords_list.shape[0]+1] = new
        return stopwords_list
    def words_clean(self):
        self.content = self.content.strip()
        "filter improper symbol"
        pattern = re.compile(r'[\u4e00-\u9fa5]+')
        filter_content = re.findall(pattern,self.content)
        "jieba cut words"
        cleaned_content = ''.join(filter_content)
        segment = jieba.lcut(cleaned_content,cut_all = True,HMM = False)
        words_df = pd.DataFrame({'segment':segment})
        "obtain stopwords list"
        stopwords = self.myStopwordDict()
        words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
#        print(words_df)
        "analysis words frequency"
        words_state = words_df.groupby(by=['segment'])['segment'].agg({"Count:":numpy.size})
        words_state = words_state.reset_index().sort_values(by=["Count:"],ascending=False)
        words_frequence = {x[0]:x[1] for x in words_state.values}
#        print(words_frequence)
        return words_frequence
    def Towrdcld(self):
        "Clean Comments Words"
        words_frequence = self.words_clean()
        "Generate Word Cloud"
        #words_content = " ".join(words_frequence.keys())
        wrdcld = WordCloud(
                mask=self.bg_pic,
                font_path=Generate_Wrdcld.zh_font,
                background_color="white",
                max_font_size=100,
                width=2000,
                height=1800,
                #margin=2,
                mode="RGBA"
                )
        wrdcld=wrdcld.fit_words(words_frequence)
        #"Set BG Color"
        #image_colors = ImageColorGenerator(Generate_Wrdcld.bg_pic_filepath)
        plt.axis("off")
        wrdcld.to_file(Generate_Wrdcld.wrdcld_picpath)
        plt.imshow(wrdcld)
        return None
    
my_wldcld = Generate_Wrdcld()
my_wldcld.Towrdcld()