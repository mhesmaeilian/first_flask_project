from firstproject import db
from sqlalchemy import Integer , String ,Boolean ,Column , DateTime ,Text ,ForeignKey
from datetime import datetime
#from models import user
#from werkzeug.security import generate_password_hash , check_password_hash
#from flask_login import  UserMixin

class Articles(db.Model):
    id=Column(Integer,primary_key=True)
    subject=Column(String(150))
    content=Column(Text)
    thumb=Column(String(100) , default='')
    publish=Column(Boolean ,default=False)
    created_at=Column(DateTime(),default=datetime.utcnow())
    __table_args__ = {'extend_existing': True}