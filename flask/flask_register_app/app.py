from flask import Flask, render_template, redirect, url_for
from forms import RegisterForm
from models import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('register.html', form=form)

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5002)
