import cherrypy
import hashlib
from Cheetah.Template import Template
from redis import Redis

class Wobsite:
    def __init__(self):
        self.db = Redis()

    def index(self):
        #should give user a random string
        #there should also be a link to a submit page
#        self.db.
        return str(Template(file="views/index.tmpl",searchList = [{"question":"Cool."}]))
    index.exposed = True

    def submit(self, awk_q = None):
        if awk_q:
            self.db.sadd("new_subs",awk_q)
        #should let the user post a random string
        return "Submit page."
    submit.exposed = True

    def set_cookie(self, username = None, password = None):
        if username and password and hashlib.sha224(password).hexdigest() == self.db.get(username):
            cookie = cherrypy.response.cookie
            cookie['username'] = username
            cookie['username']['max-age'] = 3600
            return str(Template(file="views/set_cookie.tmpl",searchList = [{"good":True}]))
        else:
            return str(Template(file="views/set_cookie.tmpl",searchList = [{"good":False}]))

    set_cookie.exposed = True

    def approve(self):
        cookie = cherrypy.request.cookie
        if cookie['password'].value == self.db.get(cookie['username'].value):
            return "Big success!"
        else:
            return "Oh no . . ."
    approve.exposed = True

    def get_random(self):
        return self.db.srandmember("awk_qs")

    def random(self):
        #should return a random string, and only a random string
        return "Random page."

    random.exposed = True

cherrypy.quickstart(Wobsite())

