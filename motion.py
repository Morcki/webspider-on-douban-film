import json
from snownlp import SnowNLP
from pyecharts import Bar,Gauge,Pie
with open('./crawed/Comments_content.txt','r',encoding = 'UTF-8') as f:
    sentimentslist = [SnowNLP(line).sentiments for line in f]
with open('./crawed/Comments.json') as f:
    comments = json.load(f)
def Plot_motion(data):
    user_number = [i+1 for i in range(len(data))]
    motion_sliderbar = Bar("Analysis of Sentiments",width = 1000,height = 800,title_pos = 'center')
    motion_sliderbar.add(
                "",
                user_number,
                data,
                is_datazoom_show=True,
                datazoom_type="slider",
                datazoom_range=[60,90],
                is_datazoom_extra_show=True,
                datazoom_extra_type="slider",
                datazoom_extra_range=[50, 100],
                #is_toolbox_show=False,
                xaxis_name="Comment Order",
                yaxis_name="Sentiments Probability"
                )
    motion_sliderbar.render("./analysis/motions_slider.html")
    
    motion_normalbar = Bar("Analysis of Sentiments",width = 1000,height = 800,title_pos = 'center')
    motion_normalbar.add(
            "",
            user_number,
            data,
            mark_line=["average"],
            mark_point=["max", "min"],
            mark_point_textcolor='black',
            xaixs_name='Comment Order',
            yaixs_name='Sentiments Probability'
            )
    motion_normalbar.render("./analysis/motion_normal.html")
    return None
def Plot_Satification(data,json_data = None):
    'weight power based on comment votes'
    if not json_data == None:
        votes = [int(json_data[comment]['Comment Votes']) for comment in json_data if comment!='film']
        votes_sum = sum(votes)
        power = [(vote+int(bool(vote==0)))/votes_sum for vote in votes]
        satif = sum([i*j for i,j in zip(data,power)])*100
    else:
        data = [i+int(bool(i==0)) for i in data]
        satif = sum(data)/len(data)*100
    gauge = Gauge("Satification",title_pos = 'center')
    gauge.add("Satification", "motion rank", round(satif,3))
    gauge.render("./analysis/Satification.html")
    return None
def Plot_stars(json_data):
    star_rank = ['Not Given Star','1stars','2stars','3stars','4stars','5stars']
    star_list = [0,0,0,0,0,0]
    for comment in json_data:
        try:
            star_list[star_rank.index(json_data[comment]['Comment Star'])]+=1
        except TypeError:
            continue
    pie = Pie("Comment Stars Given", title_pos='center')
    pie.add(
            "",
            star_rank,
            star_list,
            radius=[40, 75],
            label_text_color=None,
            is_label_show=True,
            legend_orient="vertical",
            legend_pos="left",
            )
    pie.render("./analysis/Comments_star.html")
    return None
Plot_motion(sentimentslist)
Plot_Satification(sentimentslist,comments)
Plot_stars(comments)
