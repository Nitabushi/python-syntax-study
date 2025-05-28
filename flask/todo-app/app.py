from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# テスト用のユーザIDとパスワード
users = {'testuser': {'password': 'testpass'}}

# ユーザークラス
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# ユーザー読み込みコールバック
@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

@app.route('/')
@login_required
def home():
    return render_template('home.html', name=current_user.id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 半角英数字チェック
        if not re.match(r'^[a-zA-Z0-9]+$', password):
            flash('パスワードは半角英数字のみ使用できます')
            return render_template('login.html')
        
        # ユーザ名とパスワード確認
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('ログイン失敗：ユーザー名かパスワードが間違っています')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8002, debug=True)
