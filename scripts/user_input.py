file_path = "data/output.txt"
ALLOWED_MODES =('w')

# 使用するファイルのモード
mode = 'w'

# 情報を受け取る
user_input = input("何か入力してください：")

# 受け取ったが空またはスペース、タブの場合エラーメッセージを表示する
if not user_input.strip():
    raise ValueError("入力が空です。不正な値です。")

# ファイル操作のバリデーション
if mode not in ALLOWED_MODES:
    raise ValueError(f"modeは{ALLOWED_MODES}のいずれかである必要があります。")

# ファイル拡張子のチェック
if not file_path.endswith(".txt"):
    raise ValueError("ファイルの拡張子が.txtではありません")

# ファイルに書き込む
with open(file_path, mode, encoding="utf-8")as file:
    file.write(user_input)

print("入力内容を  output.txt  に保存しました。")
print(f"ユーザから入力された内容は「{user_input}」です。"),