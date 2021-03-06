from flask import Flask, render_template, request, flash, redirect, url_for
from forms import ContactForm
from forms import CommentForm
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_script import Manager
from flask_moment import Moment
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
# bootstrap = Bootstrap(app)
# mail = Mail()
# moment = Moment(app)
# manager = Manager(app)

# configuration of sqlite database
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# unique token to prevent cross-site request forgery
app.secret_key = 'today is a great day!!'

# configuration for mail
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'real_email_address'
app.config["MAIL_PASSWORD"] = 'real_email_password'

mail = Mail()
mail.init_app(app)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
manager = Manager(app)

# model of the comment table
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __repr__(self):
        return '<Comment %r>' % self.body

# model of the post table
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.Text)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='post')

    def __repr__(self):
        return '<Post %r>' % self.body


@app.route('/about')
def about_view():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact_view():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash("All fields are required.")
            return render_template('contact.html', form=form)
        else:
            msg = Message(form.subject.data, sender='zhengxitan1031@gmail.com', recipients=['zhengxit@umich.edu'])
            msg.body = """%s""" % (form.message.data)
            mail.send(msg)
            flash("Your message is sent successfully!")
            return redirect(url_for('contact_view'))
    elif request.method == 'GET':
        return render_template('contact.html', form=form)

@app.route('/blogs')
def blogs_view():
    posts = Post.query.all()
    print 'This is for testing!'
    return render_template('blogs.html', posts=posts)


@app.route('/blogs/<blogname>', methods=['GET', 'POST'])
def single_blog(blogname):
    form = CommentForm()
    current_blog = blogname + '.html'
    if request.method == 'POST':
        if form.validate() == False:
            flash("All the fields are required.")
            return render_template(current_blog, form=form)
        elif form.validate() == True and form.validate_on_submit():
            current_comment = Comment(body=form.body.data, timestamp=datetime.utcnow(), post_id=request.args.get('post_id'))
            db.session.add(current_comment)
            return redirect(url_for('single_blog', blogname=blogname, post_id=request.args.get('post_id')))
    elif request.method == 'GET':
        comments = Comment.query.filter_by(post_id=request.args.get('post_id')).all()
        return render_template(current_blog, form=form, comments=comments)


@app.route('/resume')
def resume_view():
    return render_template('resume.html')

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    db.create_all()
    manager.run()
