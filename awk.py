import cherrypy
import hashlib
from Cheetah.Template import Template
from redis import Redis

class Wobsite:
    def __init__(self):
        self.db = Redis()

    def index(self):
        return str(Template(file="views/index.tmpl",searchList = [{"question":self.db.srandmember("awk_qs")}]))
    index.exposed = True

    def submit(self, awk_q = None):
        bool = False
        if awk_q:
            self.db.sadd("new_subs",awk_q)
            bool = True
        #should let the user post a random string
        return str(Template(file="views/submit.tmpl",searchList = [{"submitted":bool}]))
    submit.exposed = True

    def set_cookie(self, username = None, password = None):
        if username and password and hashlib.sha224(password).hexdigest() == self.db.get(username):
            cookie = cherrypy.response.cookie
            cookie['username'] = username
            cookie['username']['max-age'] = 3600
            cookie['password'] = hashlib.sha224(password).hexdigest()
            cookie['password']['max-age'] = 3600
            return str(Template(file="views/set_cookie.tmpl",searchList = [{"good":True}]))
        else:
            return str(Template(file="views/set_cookie.tmpl",searchList = [{"good":False}]))

    set_cookie.exposed = True

    def approve(self,which = None, del_which = None):
        cookie = cherrypy.request.cookie
        if cookie and cookie['password'].value == self.db.get(cookie['username'].value):
            bool = False
            if del_which:
                bool = True
                self.db.srem("new_subs",del_which)
            elif which:
                bool = True
                self.db.sadd("awk_qs",which)
                self.db.srem("new_subs",which)
                
            return str(Template(file="views/approve.tmpl",searchList = [{"submits":self.db.smembers("new_subs"),"changed":bool,"approved":True}]))
        else:
            return str(Template(file="views/approve.tmpl",searchList = [{"submits":[],"changed":False,"approved":False}]))
    approve.exposed = True

    def get_random(self):
        return self.db.srandmember("awk_qs")

    def random(self):
        #should return a random string, and only a random string
        return "Random page."

    random.exposed = True

cherrypy.quickstart(Wobsite())

