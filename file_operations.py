file_path = 'input.txt'

def write_to_file(content: str, mode: str = 'w'):
    """ファイルに書き込みまたは追記を行う"""
    if mode not in ('w', 'a'):
        raise ValueError("modeは 'w' または 'a' のいずれかである必要があります")
    with open(file_path, mode, encoding='utf-8')as file:
        file.write(content)

def read_file():
    """ファイルの内容を表示"""
    print('---ファイルの中身を表示---')
    with open(file_path, 'r', encoding='utf-8')as file:
        print(file.read())

def init_file():
    """ファイルの内容を初期状態に戻す"""
    write_to_file('こんにちは、私の名前は田中です。', mode='w')
    print('---ファイルを元の内容に戻しました---')
    read_file()

def write_file():
    """ファイルの内容を上書きする"""
    write_to_file('ファイルを上書きしました', mode='w')
    print('---ファイルを上書き---')
    read_file()

def add_file():
    """ファイルの内容を追記する"""
    write_to_file('ファイルに追記しました', mode='a')
    print('---ファイルを追記---')
    read_file()

# 実行
read_file()
write_file()
add_file()
init_file()