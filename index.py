import cherrypy

class Wobsite:
    def index(self):
        #should give user a random string
        #there should also be a link to a submit page
        return "Index page."
    index.exposed = True

    def submit(self, awk_q = None):
        #should let the user post a random string
        return "Submit page."
    submit.exposed = True

    def random(self):
        #should return a random string, and only a random string
        return "Random page."

    random.exposed = True

cherrypy.quickstart(Wobsite())
