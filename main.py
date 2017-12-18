from flask import Flask, render_template, request, flash, redirect, url_for
from forms import ContactForm
from flask.ext.bootstrap import Bootstrap
from flask_script import Manager
from flask.ext.mail import Mail, Message

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
mail = Mail()


# unique token to prevent cross-site request forgery
app.secret_key = 'today is a great day!!'

# configuration for mail
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'real_email_address'
app.config["MAIL_PASSWORD"] = 'real_email_password'

mail.init_app(app)

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
    return render_template('blogs.html')

@app.route('/resume')
def resume_view():
    return render_template('resume.html')

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    manager.run()
