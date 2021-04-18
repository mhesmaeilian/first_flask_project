from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, flash
from validators.auth import Login, Register , EditProfile ,ChangePassword,Creatpost,Editpost
from werkzeug.utils import secure_filename
from static.uploads.func import allowed_extension
from werkzeug.datastructures import FileStorage
import os
from flask_login import LoginManager ,current_user , logout_user ,login_required ,login_user
from random import randint

myapp = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
myapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'blog.db')
myapp.config['SQLALCHEMY_TRACK_MODIFIACTIONS'] = False
db = SQLAlchemy(myapp)

from models import user
from models import article
login=LoginManager(myapp)
login.login_view='Signin'

@login.user_loader
def userloader(user_id):
    return user.User_sign.query.get(user_id)



myapp.secret_key = 'dkhhrqiuhrqu8@@@@@eklkqi'

UPLOAD_DIR = os.path.curdir + '/static/uploads/'
myapp.config['UPLOAD_DIR'] = UPLOAD_DIR


@myapp.route('/')
def main():
    return render_template('testingfile.html', phones={'type': 'apple', 'date_created': 2002, 'name': 'iphon12'})


@myapp.route('/logforms', methods=['POST', 'GET'])
def signing():
    form = Login()
    if request.method == 'POST':
        if form.validate():
            username = request.form['username']
            password = request.form['password']
            if username == 'sahelchegini' and password == '123456789':
                return redirect(url_for('main'))
    return render_template("login(forms).html", form=form)


@myapp.route('/login', methods=['POST', "GET"])
def login():
    userid = request.args.get('find')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'Admin' and password == '654321':
            return 'login successfuly'
        else:
            return 'username or password is incorrect'
    return render_template('login.html', userId=userid)


@myapp.route("/post/", defaults={'post_id': 1, 'name': 'mohammad'})
@myapp.route('/post/<int:post_id>/<string:name>')
def signin(post_id, name):
    return render_template('post.html', Postid=post_id, Name=name,
                           Courses=['java', 'python', 'angular', 'java sscript'], text='jafar')


@myapp.template_filter('reversing')
def revstr(data):
    return data[::-1]


@myapp.route('/test')
def testing():
    return render_template('defined.html', content='content added successfuly!')


@myapp.route('/upload', methods=['GET', 'POST'])
def uploadfile():
    if request.method == 'POST' and "photo" in request.files:
        files = request.files['photo']
        filename = files.filename
        if allowed_extension(filename):
            filenamesecure = secure_filename(filename)
            files.save(os.path.join(UPLOAD_DIR, filenamesecure))
            flash('File uploaded successfuly', 'success')
            return redirect(url_for('uploadfile'))
        else:
            flash('file is not allowed', 'warning')
            return redirect(url_for('uploadfile'))
            print('extension is not allowed')

    return render_template('uploading.html')


@myapp.errorhandler(404)
def notfound(error):
    return render_template('404.html', error=error)


@myapp.route('/signup', methods=['post', 'get'])
def Signup():

    form = Register()
    if request.method == 'POST':
        if form.validate():
            id = randint(0,2000)
            name = request.form['name']
            password = request.form['password']
            email = request.form['email']
            userr = user.User_sign.query.filter_by(email=email).first()
            if not userr:

                newUser = user.User_sign(id=id, name=name, email=email, passwd=password)
                db.session.add(newUser)
                result = db.session.commit()
                if result != False:

                    flash('user created successfuly', 'success')
                    return redirect(url_for('Signup'))
            else:
                flash('user is exist')
                return redirect(url_for("Signup"))


    return render_template('/auth/signup.html', form=form)

@myapp.route('/signin' , methods=['post','get'])
def Signin():

    form=Login()
    if request.method=='POST':
        if form.validate():
            email=request.form.get('email')
            password = request.form.get('password')
            userr=user.User_sign.query.filter_by(email=email).first()
            if not userr:
                flash('user not exist','warning')
                return redirect(url_for('Signin'))
            if userr and userr.isoriginalpassword(password):
                login_user(userr)
                flash('log in successfully','success')
                return redirect(url_for('main'))
            else :
                return 'wrong password'


    return render_template('/auth/signin.html',form=form)

@myapp.route('/Account')
@login_required
def account():
    return render_template('/Account/index.html')

@myapp.route('/Account/info')
def account_info():
    users=user.User_sign.query.filter_by(email=current_user.email).first()
    return render_template('/Account/info.html' , user=users)

@myapp.route('/Account/edit', methods=['post', 'get'] )
def account_edit():
    form=EditProfile()
    if request.method=='POST':
        if form.validate_on_submit():
            name=request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            users=db.session.query(user.User_sign).filter_by(email=current_user.email).one()
            #updating profile
            users.name=name
            users.phone=phone
            users.email=email
            #add and submit
            db.session.add(users)
            db.session.commit()
            return redirect(url_for('account_info'))
    return render_template('/Account/edit.html' ,form=form )

@myapp.route('/Account/changepassword' , methods=['post','get'])
def account_password():
    form=ChangePassword()
    if request.method=="POST":
        if form.validate_on_submit():
            oldpassword=request.form.get('oldpassword')
            users=db.session.query(user.User_sign).filter_by(email=current_user.email).one()
            if not users.isoriginalpassword(oldpassword):
                flash('old password is incorrect' , 'danger')
                return redirect(url_for('account_password'))
            newpassword = request.form.get('newpassword')
            users.passwd=newpassword
            db.session.add(users)
            db.session.commit()
            flash('password changed successfully','success')
            return redirect(url_for('account_password'))
    return render_template('/Account/changepassword.html', form=form )


@myapp.route('/Account/avatar' ,methods=['get','post'])
def account_avatar():
    if request.method == 'POST' and 'avatar' in request.files:
        avatar = request.files['avatar']
        filename = avatar.filename
        filesecure = secure_filename(filename)
        if not allowed_extension(filename):
            flash('extension file is not allowed', 'danger')
            return redirect(url_for('acocunt_avatar'))
        avatar.save(os.path.join(myapp.config['UPLOAD_DIR'], filesecure))
        users = db.session.query(user.User_sign).filter_by(email=current_user.email).one()
        users.avatar = f'uploads/{filename}'
        db.session.add(users)
        db.session.commit()
        flash('uploaded file ssuccessfully')
        return redirect(url_for('account_avatar'))

    return render_template('/Account/avatar.html')


###signout

@myapp.route('/signout')
def Signout():
    logout_user()
    return redirect(url_for('main'))



##### Admin
@myapp.route('/Admin')
@login_required
def admin():
    if not current_user.admin:
        return redirect(url_for('account'))
    return render_template('/Admin/index.html')

@myapp.route('/Admin/edit', methods=['post', 'get'] )
def admin_edit():
    form=EditProfile()
    if request.method=='POST':
        if form.validate_on_submit():
            name=request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            users=db.session.query(user.User_sign).filter_by(email=current_user.email).one()
            #updating profile
            users.name=name
            users.phone=phone
            users.email=email
            #add and submit
            db.session.add(users)
            db.session.commit()
            return redirect(url_for('admin'))
    return render_template('/Admin/edit.html' ,form=form )

@myapp.route('/Admin/info')
def admin_info():
    users=user.User_sign.query.filter_by(email=current_user.email).first()
    return render_template('/Admin/info.html' , user=users)


@myapp.route('/Admin/changepassword' , methods=['post','get'])
def admin_password():
    form=ChangePassword()
    if request.method=="POST":
        if form.validate_on_submit():
            oldpassword=request.form.get('oldpassword')
            users=db.session.query(user.User_sign).filter_by(email=current_user.email).one()
            if not users.isoriginalpassword(oldpassword):
                flash('old password is incorrect' , 'danger')
                return redirect(url_for('account_password'))
            newpassword = request.form.get('newpassword')
            users.passwd=newpassword
            db.session.add(users)
            db.session.commit()
            flash('password changed successfully','success')
            return redirect(url_for('account_password'))
    return render_template('/Admin/changepassword.html', form=form )


@myapp.route('/Admin/avatar' ,methods=['get','post'])
def admin_avatar():
    if request.method == 'POST' and 'avatar' in request.files:
        avatar = request.files['avatar']
        filename = avatar.filename
        filesecure = secure_filename(filename)
        if not allowed_extension(filename):
            flash('extension file is not allowed', 'danger')
            return redirect(url_for('admin_avatar'))
        avatar.save(os.path.join(myapp.config['UPLOAD_DIR'], filesecure))
        users = db.session.query(user.User_sign).filter_by(email=current_user.email).one()
        users.avatar = f'uploads/{filename}'
        db.session.add(users)
        db.session.commit()
        flash('uploaded file ssuccessfully')
        return redirect(url_for('admin_avatar'))

    return render_template('/Admin/avatar.html')

@myapp.route('/Admin/list' , methods=['get','post'])
def admin_list_users():
    get_all_user=user.User_sign.query.all()
    return render_template('/Admin/list.html',users=get_all_user)
@myapp.route('/Admn/add',methods=['get','post'])
def admin_add_users():
    form=Register()
    if request.method=="POST" :
        if form.validate():
            id=randint(2000,10000)
            name=request.form.get('name')
            password=request.form.get('password')
            email=request.form.get('email')
            userr = user.User_sign.query.filter_by(email=email).first()
            if not userr:

                newUser = user.User_sign(id=id, name=name, email=email, passwd=password)
                db.session.add(newUser)
                result = db.session.commit()
                if result != False:
                    flash('user created successfuly', 'success')
                    return redirect(url_for('admin_list_users'))
            else:
                flash('user is exist')
                return redirect(url_for("admin_list_users"))

    return render_template('/Admin/adding.html',form=form)

@myapp.route('/Admin/list/edit',methods=["get","post"])
def admin_edit_users():
    form=EditProfile()
    users=db.session.query(user.User_sign).filter_by(id=request.args.get('id')).one()
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        users.name=name
        users.email=email
        users.phone=phone
        db.session.add(users)
        db.session.commit()
        return redirect(url_for('admin_list_users'))
    return render_template('Admin/edit_users.html',form=form,user=users)

@myapp.route('/Admin/list/delete/' ,methods=['get','post'])
def admin_delete_users():
    if request.method=='POST':
        db.session.query(user.User_sign).filter_by(id=request.args.get('id')).delete()
        db.session.commit()
        return redirect(url_for('admin_list_users'))


@myapp.route('/Admin/add_post', methods=['get', 'post'])
def admin_add_post():
    form = Creatpost()
    if request.method == 'POST':
        if form.validate_on_submit():
            id = randint(0, 2000)
            subject = request.form.get('subject')
            content = request.form.get('content')
            publish = True if request.form.get('publish') == 'on' else False
            thumb = request.files['thumb'] if 'thumb' in request.files else None
            if thumb is not None:
                thumb.save(os.path.join(myapp.config['UPLOAD_DIR'], secure_filename(thumb.filename)))
                newpost = article.Articles(id=id ,subject=subject, content=content, publish=publish,
                                           thumb=f'uploads/{thumb.filename}')
                db.session.add(newpost)
                db.session.commit()
                flash("article created successfuly", 'success')
                return redirect(url_for('admin_add_post'))

    return render_template('/Admin/create_post.html', form=form)

@myapp.route('/Admin/list_post',methods=['get', 'post'])
def admin_list_posts():
    get_all_articles = article.Articles.query.all()
    return render_template('/Admin/list_posts.html', articles=get_all_articles)

@myapp.route('/Admin/list_post/delete_post' , methods=['get','post'])
def admin_delete_posts():
    if request.method == 'POST':
        db.session.query(article.Articles).filter_by(id=request.args.get('id')).delete()
        db.session.commit()
        return redirect(url_for('admin_list_posts'))


@myapp.route('/Admin/list_post/edit_post',methods=['get','post'])
def admin_edit_posts():
    form=Editpost()
    articless=article.Articles.query.filter_by(id=request.args.get('id')).one()
    if request.method=='post':
        if form.validate_on_submit():
            subject=request.form.get('subject')
            content=request.form.get('content')
            publish=1 if request.form.get('publish')=='on' else 0
            thumb=request.files['thumb'] if request.files['thumb'].filename != '' else articless.thumb
            if isinstance(thumb,FileStorage):
                thumb.save(os.path.join(myapp.config['UPLOAD_DIR'],secure_filename(thumb.filename)))

            articless.subject=subject
            articless.content=content
            articless.publish=publish
            articless.thumb=f'uploads/{thumb.filename}' if isinstance(thumb,FileStorage) else articless.thumb
            db.session.add(articless)
            db.session.commit()
            return redirect(url_for('admin_list_posts'))

    return render_template('/Admin/edit_posts.html' , form=form ,article=articless)






# app.jinja_env.line_statement_prefix="#"

if __name__ == '__main__':
    myapp.run(debug=True, port=3030)
