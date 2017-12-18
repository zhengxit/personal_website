from flask import Flask, render_template, request, flash
from forms import ContactForm
from flask.ext.bootstrap import Bootstrap
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)


# unique token to prevent cross-site request forgery
app.secret_key = 'zhengxi is great!'


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
            return '<h2>Your form is submitted successfully!!</h2>'
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
