import requests
from bs4 import BeautifulSoup
import urllib
#import sys
#import time
import re
import json
from PIL import Image
def main(filmname,url_start):
    get_comments.run = 0
    get_comments.page = 0
    #page_comment_start = 0
    comments = {'film':filmname}
    url_base = 'start=%s'.join(re.split(r'start=[0-9]',url_start))
    while 1:
        #if get_comments.page % 10 == 0 and not get_comments.page == 0:
            #print('Sleeping...Waiting')
            #time.sleep(2)
        
        url = url_base%str(get_comments.run)
#        page = download_page(url)
#        get_comments(page,comments)
#        print('Page : {0}, Comments {1} have been crawered.'.format(str(get_comments.page),str(get_comments.run)))
        try:
            page = download_page(url)
            get_comments(page,comments)
            print('Page : {0}, Comments {1} have been crawered.'.format(str(get_comments.page),str(get_comments.run)))
        except AttributeError:
            get_comments.page -= 1
            page = Login_douban(url)
            #print(page)
            try:
                get_comments(page,comments)
                print('Page : {0}, Comments {1} have been crawered.'.format(str(get_comments.page),str(get_comments.run)))
            except AttributeError:
                print('Crawer Over!')
                break
        except Exception as e:
            print(e)
            break
    save_json2jsonfile('./crawed/Comments.json',comments)
    save_json2normalfile('./crawed/Comments.txt',comments)
    
def Login_douban(redir_url):
    "Build a session to post login data"
    s = requests.Session()
    login_url = "https://accounts.douban.com/login"
    login_infor = {
            'redir':redir_url,
            'form_email':'input Douban User Login',
            'form_password':'input Douban User Password',
            'login':u'登录'
            }
    login_infor_copy = login_infor.copy()
    while 1:
        content = s.post(login_url,data = login_infor_copy)
        "Input Identifying Code"
        try:
            soup = BeautifulSoup(content.text,'html.parser')
            captcha_url = soup.find('img',id='captcha_image')['src']
        except:
            return content.text
        if not len(captcha_url) == 0:
            "using re to obtain Identifying Code"
            pattern = re.compile('<input type="hidden" name="captcha-id" value="(.*?)"/')
            captcha_id = re.findall(pattern, content.text)
            "save Identifying Code into local"
            urllib.request.urlretrieve(captcha_url,"./crawed/captcha.jpg")
            captcha_img = Image.open("./crawed/captcha.jpg");captcha_img.show()
            captcha = input('please input the captcha:')
            login_infor['captcha-solution'] = captcha
            login_infor['captcha-id'] = captcha_id
            content = s.post(login_url,data = login_infor)
            #print(realcontent.text)
            if u"踏雪寻梅" in content.text:
                print("Login Succeed.")
                break
            else:
                print("Login Failed.")
                continue
    return content.text
def download_page(url):
    r = requests.get(url)
    return r.text
def save_json2jsonfile(file_path,dicts):
    '''
        save json data into file
    '''
    with open(file_path,'w') as f:
        json.dump(dicts,sort_keys = True,indent = 4,fp = f,ensure_ascii=False)
    return None
def save_json2normalfile(file_path,dicts):
    '''
        save json data into file
    '''
    with open(file_path,'w') as f:
        f.writelines('Film : '+ dicts.pop('film')+'\n')
        for key in ['Comment '+ str(i+1) for i in range(len(dicts.keys()))]:
            line = key+'\n\t'+'\n\t'.join([i+' : '+dicts[key][i] for i in sorted(dicts[key].keys(),reverse = True)])+'\n'
            f.writelines(line)
    with open(file_path[:-4]+'_content'+file_path[-4:],'w') as f:
        for key in ['Comment '+ str(i+1) for i in range(len(dicts.keys()))]:
            line = dicts[key]['Comment Content'] + '\n'
            f.writelines(line)
    return None
def get_comments(page,comments):
    get_comments.page += 1
    soup = BeautifulSoup(page,'html.parser')
#    print(soup.find(id = "comments").get_text())
    con = soup.find(id = "comments")
    con_list = con.find_all('div', class_="comment-item")
    for single in con_list:
        get_comments.run += 1
        "comment html stucture"
        single_con = single.find('div',class_ = 'comment')
        "Get comment information: user_name, user_star, user_comment_time"
        single_infor = single_con.find('span',class_ = 'comment-info')
        single_user = single_infor.find('a').get_text()
        single_star = single_infor.find_all('span')[1]['class']
        if not single_star[-1] == 'rating':
            single_star = "Not Given Star"
        else:
            single_star = single_star[0][-2] + 'stars'
        single_time = single_infor.find_all('span')[-1]['title']
        "Get comment votes"
        single_votes = single_con.find('span',class_ = 'votes').get_text()
        "Get comment content"
        single_comment = single_con.find('span',class_ = 'short').get_text()
        "convey into dict"
        comments['Comment '+str(get_comments.run)] = {}
        comments['Comment '+str(get_comments.run)]['Comment User'] = single_user
        comments['Comment '+str(get_comments.run)]['Comment Star'] = single_star
        comments['Comment '+str(get_comments.run)]['Comment Time'] = single_time
        comments['Comment '+str(get_comments.run)]['Comment Votes'] = single_votes
        comments['Comment '+str(get_comments.run)]['Comment Content'] = single_comment
    return None
if __name__ == '__main__':
    main('红辣椒',"https://movie.douban.com/subject/1865703/comments?start=0&limit=20&sort=new_score&status=P")

