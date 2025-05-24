file_path = 'input.txt'

# 元のファイルを表示する
with open(file_path, 'r', encoding='utf-8')as file:
    content = file.read()
    print('ファイルの初期状態は以下となります')
    print(content)

# ファイルの内容を上書きする
with open(file_path, 'w', encoding='utf-8')as file:
    file.write('ファイルを上書きしました')

# 上書きしたファイルの内容を確認する
with open(file_path, 'r', encoding='utf-8')as file:
    content = file.read()
    print('上書きしたファイルの内容は以下です。\n')
    print(content)

# ファイルへの追記
with open(file_path, 'a', encoding='utf-8')as file:
    file.write('この内容を追記します。')

# 追記したファイルの中身を確認する
with open(file_path, 'r', encoding='utf-8')as file:
    content = file.read()
    print('追記した内容は以下です。\n')
    print(content)

# ファイルを上書きする
with open(file_path, 'w', encoding="utf-8")as file:
    file.write('こんにちは、私の名前は田中です。')

# ファイルの中身を表示する
with open(file_path, 'r', encoding='utf-8')as file:
    print()
    print(file.read())