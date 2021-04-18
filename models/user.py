from firstproject import db
from sqlalchemy import Integer , String ,Boolean ,Column , DateTime
from datetime import datetime
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import  UserMixin
class User_sign(db.Model , UserMixin):
    id=Column(Integer() , primary_key=True )
    name=Column(String(110))
    email=Column(String(110))
    password=Column(String(110))
    admin=Column(Boolean(),default=False )
    avatar=Column(String(110) , default='/static/img/avatar.png')
    phone=Column(String(20) , default=0)
    created_at=Column(DateTime(),default=datetime.utcnow())
    __table_args__ = {'extend_existing': True}

    @property
    def passwd(self):
        raise AttributeError('access forbidden')
    @passwd.setter
    def passwd(self, password):
        self.password=generate_password_hash(password)

    def isoriginalpassword(self,user_password):
        return check_password_hash(self.password , user_password)


