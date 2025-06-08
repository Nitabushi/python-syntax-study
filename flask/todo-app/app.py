# 標準ライブラリ
import os
import re
from datetime import datetime, date, timedelta

# サードパーティライブラリ
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import (
    LoginManager, UserMixin, login_user, login_required, logout_user, current_user
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from collections import OrderedDict

# .envを読み込み
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# DB設定
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Flask-Login設定
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# モデル定義
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    user = db.relationship('User', backref='todos')

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def get_weekly_completed_tasks(user_id):
    """
    今週（月曜〜日曜）の曜日ごとの完了タスク数を取得し、
    {'月': 件数, '火': 件数, ..., '日': 件数}のOrderedDictを返す
    """
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())  # 今週の月曜日
    end_of_week = start_of_week + timedelta(days=6)         # 今週の日曜日

    # 完了日時でグループ化して件数を取得
    completed_counts = db.session.query(
        db.func.date(Todo.completed_at).label('completed_date'),
        db.func.count().label('count')
    ).filter(
        Todo.user_id == user_id,
        Todo.completed == True,
        Todo.completed_at >= datetime.combine(start_of_week, datetime.min.time()),
        Todo.completed_at <= datetime.combine(end_of_week, datetime.max.time())
    ).group_by(db.func.date(Todo.completed_at)).all()

    # 曜日（日本語）をキーに0で初期化
    week_dict = OrderedDict((day, 0) for day in ['月', '火', '水', '木', '金', '土', '日'])

    for record in completed_counts:
        weekday_idx = record.completed_date.weekday()  # 0=月曜
        day_jp = ['月', '火', '水', '木', '金', '土', '日'][weekday_idx]
        week_dict[day_jp] = record.count

    return week_dict


@app.route('/')
@login_required
def home():
    return redirect(url_for('todos'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not re.match(r'^[a-zA-Z0-9]+$', password):
            flash('パスワードは半角英数字のみ使用できます')
            return render_template('login.html')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('todos'))
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
    
    today = date.today()
    today_completed_count = Todo.query.filter(
        Todo.user_id == current_user.id,
        Todo.completed == True,
        Todo.completed_at >= datetime(today.year, today.month, today.day)
    ).count()

    weekly_completed = get_weekly_completed_tasks(current_user.id)

    return render_template(
        'todos.html',
        tasks=tasks,
        today_completed_count=today_completed_count,
        weekly_completed=weekly_completed
    )


@app.route('/complete/<int:task_id>')
@login_required
def complete_task(task_id):
    task = Todo.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('他のユーザーのタスクは操作できません')
        return redirect(url_for('todos'))

    task.completed = not task.completed
    task.completed_at = datetime.utcnow() if task.completed else None
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
    flash('タスクを削除しました')
    return redirect(url_for('todos'))


@app.route('/bulk_action', methods=['POST'])
@login_required
def bulk_action():
    task_ids = request.form.getlist('task_ids')
    action = request.form.get('action')

    if not task_ids:
        flash('操作するタスクを選択してください')
        return redirect(url_for('todos'))

    for task_id in task_ids:
        task = Todo.query.get(int(task_id))
        if task and task.user_id == current_user.id:
            if action == 'complete':
                task.completed = not task.completed
                task.completed_at = datetime.utcnow() if task.completed else None
            elif action == 'delete':
                db.session.delete(task)
        else:
            flash('一部のタスクは操作できませんでした')

    db.session.commit()

    if action == 'complete':
        flash('選択したタスクの状態を変更しました')
    elif action == 'delete':
        flash('選択したタスクを削除しました')

    return redirect(url_for('todos'))


# 初回テーブル作成
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8002, debug=True)
