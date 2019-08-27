from wxpy import *
from datetime import date
from api_weather import *
from data import *
from fenci import baidu_fenci_result
from apscheduler.schedulers.background import BackgroundScheduler
import time



#早上好
moring = '早上好！'
success_weather = '订阅成功！从明天开始,每天早上都会收到当天的天气提醒:)'

#今日天气预报
def msg_today_weather(cityname):
    weather = today_weather(cityname)
    print(weather)
    high_tem  =  weather['high_tem']
    low_tem = weather['low_tem']
    day_wea =  weather['day_wea']
    night_wea = weather['night_wea']
    day_win = weather['day_win']
    night_win = weather['night_win']
    sunrise = weather['sunrise']
    sunset = weather['sunset']
    r = '早上好！😸\n【今日' + cityname + '】\n' + '· '+sunrise+'，'+sunset+'\n'+'· '+high_tem+'度'+'~'+low_tem+'度\n' + '· 白天'+day_wea+'，'+'风力'+day_win+'\n'+ '· 夜间'+night_wea+'，'+'风力'+night_win

    return r



#将当前wxpy特有id进行注册，订阅天气服务
def signup(uid,name,city_name):
    col = Col()
    col.create(uid,name,city_name)


#根据wxpy特有id对数据库进行查询
def user_info(uid):
    col = Col()
    u = col.find_user(uid)
    return u

def get_time():
    now_t = time.localtime(time.time())
    now = time.strftime('%Y-%m-%d %H:%M:%S',now_t)
    return now

#定义任务
def job():
    col = Col()
    
    for i in col.col.find():
        client = bot.friends().search(i['name'])[0]
        w = msg_today_weather(i['city'])
        client.send(w)

def check_login():
    now = get_time()
    print('当前机器人登录情况：', bot.alive)
    if not bot.alive:
        print('下线了时间：',now)


if __name__ == '__main__':

    bot = Bot(cache_path=True, console_qr=True)
    print('机器人登录时间：',get_time())
  
    #启动wxpy聊天对象特有ID
    bot.enable_puid()

    #定时任务
    sched = BackgroundScheduler()
    sched.add_job(job,'cron',hour='7',minute='0')
    sched.add_job(check_login,'interval',minutes=30)
    sched.start()


    @bot.register()
    def process_message(msg):
 
        print(msg)
        #获取wxpy特有id
        uid = msg.chat.puid
        name = msg.chat.name
        res = baidu_fenci_result(msg.text)
        col = Col()
    
        if res['items'][2]['item'] == '天气' and res['items'][0]['item'] == '订阅':
            city_name =res['items'][1]['item']
            #如果用户存在,更改订阅信息，回复当前天气 
            print('用户',name,'刚刚订阅了',city_name,'的天气')
            u = col.find_user(uid)
            if u:
                col.modify_city(uid,city_name)
                w = msg_today_weather(city_name)
                res = w + '\n'+'----------'+'\n'+success_weather
                msg.reply(res)

            #如果用户不存在，询问查询城市
            else:
                signup(uid,name,city_name)

                w = msg_today_weather(city_name)
                res = w + '\n'+'----------------------'+'\n'+success_weather
                msg.reply(res)
        else:
            res = '使用帮助：'+ '\n' + '订阅+城市名字+天气，例如：订阅北京天气'
            msg.reply(res)
               

    embed()
