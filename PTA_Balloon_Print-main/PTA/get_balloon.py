import requests
from time import time
import json
import os

dic0={}             #存做题信息
balloon_color_list=['灰色','粉色','咖啡色','白色','黑色','蓝色','红色','果绿色','紫色','金色']#存放气球颜色

problem_name={'T527251':'A',
              'T527749':'B',
              'T527753':'C',
              'T529952':'D',
              'T529947':'E',
              'T529950':'F',
              'T529954':'G',
              'T532206':'H',
              'T527248':'I',
              'T529956':'J'
              }
比赛id=210723



url = 'https://www.luogu.com.cn/fe/api/contest/scoreboard/'+str(比赛id)
problem_name_index=list(problem_name.keys())        #用来给气球上色
#读取保存的做题信息
if os.path.exists('dic0.json'):
    with open('dic0.json', 'r', encoding='ANSI') as f:
        dic0 = json.load(f)
else:
    dic0 = {}

with open('../../data/team.json', 'r', encoding='UTF-8') as location_data:
    location_data = json.load(location_data)
personal_information={}
for _ , value in location_data.items():
    personal_information[value['name']]=[value['team_name'],value['location']]

text=open('C:\\ICPC\\第二修正案\\PTA_Balloon_Print-main\\PTA\\print_info\\printer.txt', 'w', encoding='ANSI')           #打开最后要写入的文件
text.write('BALLOON_STATUS\n')
index=1
for page in range(1,7):
    params = {
        'page': page,
    }
    headers = {
        'Cookie': '__client_id=e39e9a64402ba3cab7042d3d8c6d0caa4c06fa18; _uid=858510; C3VK=5ffe62',   #管理员账号下的信息
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 HBPC/12.1.3.310',
        'X-Requested-With': 'XMLHttpRequest'
    }
    try:
        response = requests.get(url, params=params, headers=headers,timeout=5)
        data=response.json()
        for i in data['scoreboard']['result']:
            if i['user']['name'] not in dic0:       #看人有没有存进去
                dic0[i['user']['name']] = {}
            for k in i['details']:                  #看人做的题有没有存过
                if k not in dic0[i['user']['name']]:
                    dic0[i['user']['name']][k]=-1
            for key,value in i['details'].items():
                score=i['details'][key]['score']
                if dic0[i['user']['name']][key]<0 and value['score'] >=0:
                    dic0[i['user']['name']][key]=score
                    '''
                    打印气球
                    '''
                    #气球id，通过时间戳实现
                    text.write(str(int(time()*1000000))+str(index)+'\n')
                    index+=1
                    #teamname
                    text.write(personal_information[i['user']['name']][0]+'\n')
                    # location
                    text.write(personal_information[i['user']['name']][1]+'\n')

                    # promblemname
                    text.write(problem_name[key]+'\n')

                    # ballooncolor
                    text.write(balloon_color_list[problem_name_index.index(key)]+'\n')

                    # firstsolve
                    if key in data['firstBloodUID']:
                        if data['firstBloodUID'][key]==i['user']['uid']:
                            text.write('True\n')
                        else:
                            text.write('False\n')
                    else:
                        text.write('False\n')

                    # spilt
                    text.write("------------\n")


        if len(data['scoreboard']['result']) != 50:
            break
    except requests.exceptions.Timeout:
        print("请求超时")
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except Exception as e:
        print(f"其他错误: {e}")

with open('dic0.json', 'w', encoding='utf-8') as f:#保存做题信息
    json.dump(dic0, f, ensure_ascii=False, indent=4)