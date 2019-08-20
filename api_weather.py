import requests,json
from bs4 import BeautifulSoup
import time

#api:www.tianqiapi.com

def localtime():
    return time.localtime(time.time())


def today_weather(city_name):
    city_id = get_city_id(city_name)
    base_url = 'http://www.weather.com.cn/weather1d/'
    today = {}
    url = base_url+str(city_id)+'.shtml'
    res = requests.get(url)
    soup = BeautifulSoup(res.content,'html.parser')
    today_html = soup.find('div',class_='t').find('ul',class_='clearfix')

    #网站每天18:00调换日间与夜间信息的位置
    lt=localtime()
    today_day_html,today_night_html = ['','']

    if lt.tm_hour < 18:
        today_day_html = today_html.contents[1]
        today_night_html = today_html.contents[3]
    else:
        today_day_html = today_html.contents[3]
        today_night_html = today_html.contents[1]


    today['day_wea'] = today_day_html.find('p',class_='wea').string
    today['high_tem'] = today_day_html.find('p',class_='tem').find('span').string
    today['day_win'] = today_day_html.find('p',class_='win').find('span').string
    today['sunrise'] = today_day_html.find('p',class_ = 'sun').find('span').string
    today['night_wea'] = today_night_html.find('p',class_= 'wea').string
    today['low_tem'] = today_night_html.find('p',class_='tem').find('span').string
    today['night_win'] = today_night_html.find('p',class_='win').find('span').string
    today['sunset'] = today_night_html.find('p',class_='sun').find('span').string

    return today


#查询城市ID
def read_city_id():
    with open('city_id.json','r') as f:
        j = json.loads(f.read())
        return j

#城市列表
def cities(res):
    city_list = []
    for i in res:
        city_list.append(i['cityZh'])
    return city_list

#是否在城市列表中
def is_city(city):
    r = read_city_id()
    city_list = cities(r)
    if city in city_list:
        return True
    else:
        return False

#返回城市id
def get_city_id(city_name):
    r = read_city_id()
    for i in r:
        if i['cityZh'] == city_name and i['leaderZh'] == city_name:
            return i['id']

        
          
        



