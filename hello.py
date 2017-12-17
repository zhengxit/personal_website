from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)




@app.route('/about')
def about_view():
    return render_template('about.html')

@app.route('/contact')
def contact_view():
    return render_template('contact.html')

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
