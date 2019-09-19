from flask import (Flask, render_template)
app = Flask(__name__, template_folder="templates")

app.config['TESTING'] = True

@app.route('/')
def home():
    """
    index response
    """
    return render_template('home.html')

@app.route('/chars')
def chars():
    return 'here are all the chars i know about'

@app.route('/char/<int:charId>')
def show_char(charId):
    return 'here is the info for char with id %s' % charId

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'logging ya in'
    else:
        return 'heres a login form'


if __name__ == '__main__':
    app.run()