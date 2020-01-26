# POST请求接收
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import socket
from time import sleep
from tornado.options import define, options

# 绑定地址
define('port', default=3000, type=int, help='Server Port')
Disk_addr = ('127.0.0.1', 32648)


# 连接disk
def connectDisk(addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    state = s.recv(1024)
    state = state.decode('utf-8')
    # print(state)
    if (state == 'what'):
        s.send('POST'.encode('utf-8'))
        return s


# seahToken && delToken
def s_dToken(username, U_Token):
    s = connectDisk(Disk_addr)
    s.send(username.encode('utf-8'))
    s.recv(1024)    #等待disk响应
    s.send(U_Token.encode('utf-8'))
    state = s.recv(1024)
    return state


# 定义继承类
class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST')


# POST请求
class POSTHandler(BaseHandler):
    def post(self):
        U_Token = self.get_argument('Token')
        username = self.get_argument('username')
        pwd = self.get_argument('pwd')
        Email = self.get_argument('Email')
        #print('getok')
        state = s_dToken(username, U_Token)
        state = state.decode('utf-8')
        #print(state)
        if (state == 'True'):
            #验证成功，写入数据库
            #print(username, pwd, Email, U_Token)
            self.finish({'message':'ok'})
        elif (state == 'False'):
            #验证失败，丢弃数据
            self.finish({'message':'error','why':'Token校验错误！'})
            U_Token, username, pwd, Email, state = None, None, None, None, None
        else:
            self.write("内部错误")


# 主函数
def main():
    tornado.options.parse_command_line()
    # 定义APP
    app = tornado.web.Application(
        handlers=[(r'/register', POSTHandler)],
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print('POST System is ready')
    tornado.ioloop.IOLoop.instance().start()


main()
