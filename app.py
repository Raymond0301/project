from persistence import *
import functools
from flask import *
import uuid
app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev'
)


@app.route('/')
def home():
    return render_template('home.html')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session['id'] is None:
            return redirect(url_for('home'))
        return view(**kwargs)
    return wrapped_view


@app.route('/init')
def init():
    init.db()
    return 'db initialised'


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/tips')
def tips():
    return render_template('tips.html')


@app.route('/table', methods=('GET', 'POST'))
def table():
    if request.method == 'POST':
        error = None
        username = request.form['username']
        month = request.form['month']
        target = request.form['target']
        actual = request.form['actual']
        save = saving_table(username, month, target, actual)
        if save is False:
            flash('Your table has been saved!')
    return render_template('table.html')


@app.route('/quiz')
def quiz():
    return render_template('quiz.html')


@app.route('/login',  methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            user = get_user(username, password)
            if user is None:
                error = 'Wrong credentials'
            elif user == username:
                session['user_name'] = username
                flash('You successfully logged in!')
                return redirect(url_for('profile'))
        flash(error)
    return render_template('login.html')
    # guest mode button if press instantly log in so skip signup page


@app.route('/signup', methods=('GET', 'POST'))
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email required'
        else:
            validation = check_user(username, email)
            if validation is False:
                error = 'Username/Email has already been taken'
            else:
                id = str(uuid.uuid4())
                create_user(id, username, email, password)
                flash('You have successfully signed up!')
                return redirect(url_for('login'))
        flash(error)
    return render_template('signup.html')


@app.route('/forget_password', methods=('GET', 'POST'))
def forget_password():
    if request.method == 'POST':
        email = request.form['email']
        word = forget_passwords(email)
        if word is False:
            flash("Email have been successfully sent, containing your password!")
            return redirect(url_for('login'))
        else:
            flash('Invalid email')
    return render_template('forget_password.html')


@app.route('/reset', methods=('GET', 'POST'))
def reset():
    if request.method == 'POST':
        email = request.form['email']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        checking = check_users(email, old_password)
        if checking is False:
            if new_password == confirm_password:
                new = change(email, new_password)
                if new is False:
                    flash("Password have been changed")
                    return redirect(url_for('login'))
                else:
                    flash('Failed to reset password!')
            else:
                flash('Passwords are not the same')
        else:
            flash('Invalid email/ old password')
    return render_template('reset.html')


@app.route('/logout', methods=('GET', 'POST'))
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(port=5000)
