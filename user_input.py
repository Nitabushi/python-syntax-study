# 情報を受け取る
user_input = input("何か入力してください：")

# 受け取ったが空またはスペース、タブの場合エラーメッセージを表示する
if not user_input.strip():
    raise ValueError("入力が空です。不正な値です。")

print(user_input)
