import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # CSRF無効化
    with app.test_client() as client:
        yield client

def test_login_with_invalid_password(client):
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'あいうえお123'  # 全角文字を含む
    }, follow_redirects=True)

    # 日本語のメッセージをエンコードして比較
    assert 'パスワードは半角英数字のみ使用できます'.encode('utf-8') in response.data

def test_login_with_valid_password(client):
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'  # 正しい半角英数字
    }, follow_redirects=True)

    # 正しくログインできたかどうかを status_code または任意の文言で判定
    assert response.status_code == 200
    assert b'testuser' in response.data or 'ようこそ'.encode('utf-8') in response.data
