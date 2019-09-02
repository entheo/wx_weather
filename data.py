import pymongo

class Data():
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://root:2810033@localhost:27017')
        self.db = self.client['wx_weather']
        self.is_authorized = self.client.wx_weather.authenticate('weather','2810033')

class Col(Data):
    def __init__(self):
        super(Col,self).__init__()
        self.col = self.db['user_city']
    
    def create(self,uid,name,city):
        self.col.insert_one({'uid':uid,'name':name,'city':city})
        
    def find_user(self,uid):
        u = self.col.find_one({'uid':uid})
        if u :
            return u
        else:
            return False
    
    def modify_city(self,uid,new_city):
        user = {'uid':uid}
        new = {'$set':{'city':new_city}}
        self.col.update_one(user,new)
        


