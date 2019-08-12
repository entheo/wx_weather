import json,requests


class fenci():
    def __init__(self,servant):
        self.name = 'fenci'
        self.servant = servant
  
    #获取分词结果
    def get_result(self,text):
        data = json.dumps({'text':text})
        headers = {'Content-Type':'application/json'}
        url = self.servant.yuyan_url+'?charaset=UTF-8&access_token='+self.servant.access_token
        res = requests.post(url=url,headers=headers,data=data)
        return res.text
    
    #定义获取分词结果的方法，可被根据不同规则来调用
    def get_msg(self,res_text):
        res = json.loads(self.get_result(res_text))
        return res


class baidu():
    def __init__(self):
        self.name = 'baidufenci'
        self.api_key = 'qQdffGp207ruKUdzCFAla4nk'
        self.secret_id = 'nGBvPdkQihjzWTwfEMvh5GSOfkVKodhl'
        self.token_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+self.api_key+'&client_secret='+self.secret_id
        self.yuyan_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer'
        self.access_token = self.get_access_token()

    #获取access_token
    def get_access_token(self):
        res = requests.post(self.token_url)
        access_token = json.loads(res.text)['access_token']
        return access_token

    

def baidu_fenci_result(text):
    bot = baidu()
    f = fenci(bot)
    r = f.get_msg(text)
    return r
