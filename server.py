# -*- coding: utf-8 -*-
import os,json,re
from collections import Counter
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado import escape
from tornado.options import define,options

from functions import *
cwd =os.path.dirname(__file__)

SPACES = {}


def get_space_names():
    files = os.listdir(os.path.join(cwd,'spaces'))
    return dict.fromkeys(files,True)

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html',message="")
    def post(self):
        pass

class LogoutHandler(tornado.web.RequestHandler):
    def post(self):
        if (self.get_argument("logout", None)):
            self.clear_cookie("id")
        self.redirect("/")

class pullHandler(tornado.web.RequestHandler):
    def get(self,):
        data  = self.request.arguments
        ss_name   = data['SS'][0].decode('utf8')
        text      = data['text'][0].decode('utf8')
        minweight = data['minWeight'][0]
        minweight = min(max(0.,float(minweight)),1.)
        topk      = int(data['topk'][0])
        lang      = data['lang'][0].decode('utf8')
        if ss_name not in SPACES:
            spaces = get_space_names()
            if ss_name + '.jsn' in spaces:
                SPACES[ss_name] = load_SS(ss_name+'.jsn')
        if ss_name not in SPACES:
            self.write('no such space exists')
            return 
        else:
            print(lang)
            result = retrieve(SPACES[ss_name],
                                text,topk=topk,minweight=minweight,lang=lang)
            
            self.write(json.dumps(result))
            return 

class compareTextHandler(tornado.web.RequestHandler):
    def get(self,):
        data  = json.loads(self.request.arguments)
        print(data)







        
        
if __name__=="__main__":
    define("port",default=8000,help="run on given port",type=int)
    tornado.options.parse_command_line()
    print("service started")
    app = tornado.web.Application(handlers=[
        (r"/pull",pullHandler),
        (r'/compareText',compareTextHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__),"templates"),
        static_path = os.path.join(os.path.dirname(__file__),'static'),
        cookie_secret= "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        login_url= "/login",
        debug=True,
        )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
