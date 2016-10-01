#-*- coding:utf-8 -*-

from flask_login import UserMixin, LoginManager
import requests

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = u"请先登录"
login_manager.refresh_view = "reauth"


class User(UserMixin):
    def __init__(self, id, pwd):
        self.id = id
        self.pwd = pwd 
        self.s = requests.Session()
        if self.id=='admin' and self.pwd=='admin':
            self.isOk = True    
        else:
            self.isOK = False    
    
    @classmethod
    def get(self_class, id, pwd):
        '''Return user instance of id, return None if not exist'''
        try:
            return self_class(id, pwd)
        except UserNotFoundError:
            return None

class UserNotFoundError(Exception):
    pass


@login_manager.user_loader
def load_user(id):
    return User.get(id, None)
