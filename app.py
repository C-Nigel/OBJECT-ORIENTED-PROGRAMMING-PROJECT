from flask import *
from persistence import *

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY = 'dev'
)
@app.route('/')
def Home():
    return render_template('Home.html')

@app.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        email = request.form['email']
        Cname = request.form['Cname']
        password = request.form['password']
        contact = request.form['contact']

        if not email:
            error = 'Email is Required'
        elif not Cname:
            error = 'Company name is required.'
        elif not password:
            error = 'Password is required.'
        elif not contact:
            error = 'Contact is required.'
        else:
            create_user(email, Cname, password, contact)
            return redirect(url_for('Home'))
        flash(error)
    return render_template('Home.html')

@app.route('/login',  methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == re.search("[@.]", email) is None:
            print("Invalid Email")
        else:
            return True
        error = None
        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        else:
            user = get_user(email, password)
            if user is None:
                error = 'Wrong email and password'
            else:
                session['tag'] = user.get_tag()
                session['email'] = user.get_email()
                return redirect(url_for('Home'))
        flash(error)
    # after login go to the specific profile pages.
    return render_template('Home.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('Home'))

if __name__ == '__main__':
    app.run()
