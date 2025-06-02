import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import re
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# .envを読み込み
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# DB接続設定
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ユーザーモデル
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# ToDoモデル
class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='todos')


# ユーザー読み込みコールバック
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
        
        # DBからユーザを取得
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
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

@app.route('/todos', methods=['GET', 'POST'])
@login_required
def todos():
    if request.method == 'POST':
        task_content = request.form['task']
        if task_content:
            new_task = Todo(task=task_content, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('タスクを追加しました')
        else:
            flash('タスク内容を入力してください')

    order = request.args.get('order', 'desc')

    if order == 'asc':
        tasks = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.created_at.asc()).all()
    else:
        tasks = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.created_at.desc()).all()
    return render_template('todos.html', tasks=tasks)

@app.route('/complete/<int:task_id>')
@login_required
def complete_task(task_id):
    task = Todo.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('他のユーザーのタスクは操作できません')
        return redirect(url_for('todos'))
    
    task.completed = not task.completed
    db.session.commit()

    if task.completed:
        flash('よく頑張りました！')

    return redirect(url_for('todos'))

@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Todo.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('他のユーザーのタスクは削除できません')
        return redirect(url_for('todos'))
    
    db.session.delete(task)
    db.session.commit()
    
    return redirect(url_for('todos'))


# 初回だけテーブルを作成する
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8002, debug=True)
