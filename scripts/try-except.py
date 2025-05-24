try:
    # エラーが発生するかもしれない処理
    user_input = input("数字を入力してください: ")
    user_input_num = int(user_input )
    division_result = 10 / user_input_num
    print("結果:", division_result)

except ValueError:
    # 数字以外が入力されたときの処理
    print(f"無効な入力です: '{user_input}'は数値ではありません")

except Exception as e:
    # その他のすべての例外に対応
    print("予期しないエラー:", e)

finally:
    # 例外の有無に関係なく必ず実行される処理
    print("処理を終了します。")
