from wxpy import *
from api_weather import *
from data import *
from fenci import baidu_fenci_result
from apscheduler.schedulers.background import BackgroundScheduler




#早上好
moring = '早上好！'
#今日天气预报
def msg_today_weather(cityname):
    weather = today_weather(cityname)
    high_tem  =  weather['tem1']
    low_tem = weather['tem2']
    air_level = weather['air_level']+'\n'
    wea = '· 有'+ weather['wea']+'\n'
    wind = '· ' + weather['win'][0]+weather['win_speed']+'\n'
    ray = weather['index'][0]['desc']+'\n'
    blood = '· '+ weather['index'][2]['desc']
    r = '早上好！【今日'+cityname+'天气】\n'+ '· 最高温度: '+high_tem+'度\n'+'· 最低温度: '+low_tem+'度\n'+wind+wea+'· 空气质量: '+air_level+'· 紫外线: '+ray+'· 血糖影响: '+blood
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


#定义任务
def job():
    col = Col()
    clinets = []
    for i in col.col.find():
        client = bot.friends().search(i['name'])[0]
        w = msg_today_weather(i['city'])
        client.send(w)

if __name__ == '__main__':

    bot = Bot()
  
    #启动wxpy聊天对象特有ID
    bot.enable_puid()


    #定时任务
    sched = BackgroundScheduler()
    sched.add_job(job,'cron',hour='6',minute='30')
    sched.start()


    @bot.register()
    def process_message(msg):
    
        #获取wxpy特有id
        uid = msg.chat.puid
        name = msg.chat.name
        res = baidu_fenci_result(msg.text)
        col = Col()
    
        if res['items'][2]['item'] == '天气' and res['items'][0]['item'] == '订阅':
            city_name =res['items'][1]['item']
            #如果用户存在,更改订阅信息，回复当前天气  
            u = col.find_user(uid)
            if u:
                col.modify_city(uid,city_name)
                w = msg_today_weather(city_name)
                res = w + '\n'+'----------'+'\n'+'订阅成功，明天一早将收到天气提醒'
                msg.reply(res)

            #如果用户不存在，询问查询城市
            else:
                print(name,city_name)
                signup(uid,name,city_name)

                w = msg_today_weather(city_name)
                res = w + '\n'+'----------'+'\n'+'订阅成功，每天早上都会收到天气提醒'
                msg.reply(res)
        else:
            res = '使用帮助：'+ '\n' + '订阅+城市名字+天气，例如：订阅北京天气'
            msg.reply(res)
               

    embed()
