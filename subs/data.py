# 数据库操作

# 导入模块
import pymysql


# 初始化函数
def _init():

    # 连接数据库
    db = pymysql.connect(
        host='localhost',
        port=3306,
        user='Blog',
        passwd='20041123',
        db='alimo1029-blog',
        charset='utf8'
    )

    # 创建游标
    cursor = db.cursor()
    return db, cursor


class C_user:
    def addUser(db, cursor, username, password, mail):
        # 添加新用户
        try:
            args = (username, password, mail)
            sql = "INSERT INTO users(username, password, mail) VALUES (%s,%s,%s)"
            # print(sql)
            cursor.execute(sql, args)
            db.commit()
            return True
        except:
            # 异常
            db.rollback()
            return False

    def searchUser(db, cursor, username, password, mail, need):
        """need = 0代表登录模式
           need = 1代表注册模式
           need = 2代表单纯查询
        """
        # 搜索数据库
        args = (username, password)
        L_sql = "SELECT username FROM users WHERE username = %s AND password = %s"
        R_sql = "SELECT username FROM users WHERE username = %s"
        S_sql = "SELECT username FROM users WHERE username = %s"
        # print(L_sql)
        if (need == 0):
            # 登录模式
            cursor.execute(L_sql, args)
            sehData = cursor.fetchone()
            if (sehData != None):
                # 账号和密码组合获取成功
                # print('ok')
                # print(sehData)
                sehData = None
                return True
            else:
                # 获取不到，账号或密码错误
                # print('sorry')
                L_sql = None
                return False
        elif (need == 1):
            # 注册模式
            cursor.execute(R_sql, username)
            sehData = cursor.fetchone()
            if (sehData == None):
                # 无人使用，可以注册
                C_user.addUser(db, cursor, username, password, mail)
                #db.commit()
                return True
            else:
                # 有人使用，禁止注册
                sehData = None
                return False
        elif (need == 2):
            # 查询模式
            cursor.execute(S_sql, username)
            sehData = cursor.fetchone()
            db.commit()
            if (sehData == None):
                # 查无此人
                return 0
            else:
                # 查有此人
                sehData = None
                return 1
        else:
            return False

    def delUser(db, cursor, username):
        # 删除指定用户
        sql = "DELETE FROM users WHERE username = %s"
        try:
            cursor.execute(sql, username)
            db.commit()
            return True
        except:
            return False

# db, cursor = _init()
# print(C_user.addUser(db, cursor, 'limo1029', '20041123'))
# print(C_user.searchUser(db, cursor, 'limo1029asd', '20041123', '1282160815@qq.com', 1))
# print(C_user.delUser(db, cursor, 'limo1029'))