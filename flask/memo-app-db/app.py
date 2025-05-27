from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from dotenv import load_dotenv
import os

# .env情報の読み取り
load_dotenv()  

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# DB接続設定
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# モデルの設定
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ルーティング
@app.route('/')
def index():
    messages = Message.query.order_by(Message.id.desc()).all()
    return render_template('index.html', messages=messages)

@app.route('/confirm', methods=['POST'])
def submit():
    message = request.form['message']
    return render_template('confirm.html',message=message)

@app.route('/complete', methods=['POST'])
def complete():
    message = request.form['message']
    print(f"Received message: {message}") 

    new_message = Message(content=message)
    db.session.add(new_message)
    db.session.commit()
    print("Saved to DB.")

    return render_template('complete.html', message=message)

@app.route('/delete/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    print(f"Deleted message with ID: {message_id}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    
    # 初回だけテーブル作成（なければ）
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=8001, debug=True)
