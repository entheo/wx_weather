import requests,json

#api:www.tianqiapi.com


url = 'https://www.tianqiapi.com/api/'

def sevendays_weather(city):
    payloads = {
        'appid':'52642256',
        'appsecret':'XDmlDP9h',
        'version':'v1',
        'city':city
    }
    res = requests.get(url,params=payloads)
    return json.loads(res.text)

def today_weather(city):
    res = sevendays_weather(city)
    t = res['data'][0]
    return t

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

