file_path = 'input.txt'

# 元のファイルの内容に戻す関数
def init_file():
    with open(file_path, 'w', encoding='utf-8')as file:
        file.write('こんにちは、私の名前は田中です。')
        print('---ファイルを元の内容に戻しました---')
    read_origin_file()

# 元ファイルを表示する関数
def read_origin_file():
    with open(file_path, 'r', encoding='utf-8')as file:
        print('---ファイルの中身を表示---')
        print(file.read())

# ファイルの内容を上書きする関数
def write_file():
    with open(file_path, 'w', encoding='utf-8')as file:
        file.write('ファイルを上書きしました。')
        print('---ファイルを上書き---')
    read_origin_file()

# ファイルの内容を追記する関数
def add_file():
    with open(file_path, 'a', encoding='utf-8')as file:
        file.write('ファイルに追記しました。')
        print('---ファイルを追記---')
    read_origin_file()


read_origin_file()
write_file()
add_file()
init_file()