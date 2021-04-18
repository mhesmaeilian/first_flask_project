from flask_wtf import FlaskForm
from wtforms import  StringField , PasswordField,SubmitField ,TextAreaField ,FileField
from wtforms.validators import DataRequired , Length ,Email ,EqualTo

class Login(FlaskForm):
    email=StringField(_name='email',validators=[DataRequired('email field is required')])
    password=PasswordField(_name='password',validators=[DataRequired('password  field is required'),
                                                        Length(min=8 , message='password is less than 8 characters')])

    submit=SubmitField()



class Register(FlaskForm):
    name=StringField(_name='name',validators=[DataRequired('name field is required')])
    email=StringField(_name='email',validators=[DataRequired('email field is required') ,
                                                Email('email is invalid')])

    password = PasswordField(_name='password', validators=[DataRequired('password  field is required'),
                                     Length(min=8, message='password is less than 8 characters')])
    confirm= PasswordField(_name='confirm',validators=[DataRequired('confirm field is required'),
                                                        Length(min=8 , message='confirm is less than 8 characters') ,
                                                       EqualTo("password" , 'does not confirm')])
    submit=SubmitField()


class EditProfile(FlaskForm):
    name = StringField(_name='name', validators=[DataRequired('name field is required')])
    email = StringField(_name='email', validators=[DataRequired('email field is required'),
                                                   Email('email is invalid')])
    phone = StringField(_name='phone', validators=[DataRequired('phone field is required')])

    submit = SubmitField('update profile')


class ChangePassword(FlaskForm):
   oldpassword = PasswordField(_name='oldpassword',
                               validators=[DataRequired('password  field is required'),
                              Length(min=8, message='password is less than 8 characters')])

   newpassword = PasswordField(_name='newpassword',
                               validators=[DataRequired('password  field is required'),
                              Length(min=8, message='password is less than 8 characters')])

   confirm= PasswordField(_name='confirm',validators=[DataRequired('confirm field is required'),
                                                        Length(min=8 , message='confirm is less than 8 characters') ,
                                                       EqualTo("newpassword" , 'does not confirm')])

   submit = SubmitField('update profile')


class Creatpost(FlaskForm):
    subject=StringField(_name='subject',validators=[DataRequired('subject field is required')])
    content=TextAreaField(_name='content',validators=[DataRequired('content field is required')])
    thumb=FileField()
    submit=SubmitField('creat new post')

class Editpost(FlaskForm):
    subject = StringField(_name='subject', validators=[DataRequired('subject field is required')])
    thumb = FileField()
    submit = SubmitField('creat new post')