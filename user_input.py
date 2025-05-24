# 情報を受け取る
user_input = input("何か入力してください：")

# 受け取ったが空またはスペース、タブの場合エラーメッセージを表示する
if not user_input.strip():
    raise ValueError("入力が空です。不正な値です。")

# 受け取った情報をファイルに書き込む
with open("data/output.txt", "w", encoding="utf-8")as file:
    file.write(user_input)
print("入力内容を  output.txt  に保存しました。")

print(f"ユーザから入力された内容は「{user_input}」です。")