def validate_input(user_input: str) -> str:
    """ユーザー入力のバリデーションを行い、問題なければ整形済み文字列を返す。"""
    cleaned = user_input.strip()
    if not cleaned:
        raise ValueError("入力が空です。不正な値です。")
    return cleaned

def validate_file_path(file_path: str, allowed_modes: tuple, mode: str):
    """ファイルパスの拡張子とモードのバリデーションを行う。"""
    if mode not in allowed_modes:
        raise ValueError(f"modeは{allowed_modes}のいずれかである必要があります。")
    if not file_path.endswith(".txt"):
        raise ValueError("ファイルの拡張子が.txtではありません")

def save_to_file(file_path: str, content: str, mode: str = 'w', encoding: str = "utf-8"):
    """ファイルに書き込みを行う。"""
    with open(file_path, mode, encoding=encoding) as f:
        f.write(content)

def main():
    ALLOWED_MODES = ('w',)
    file_path = "data/output_func.txt"
    mode = 'w'

    user_input = input("何か入力してください：")
    cleaned_input = validate_input(user_input)
    validate_file_path(file_path, ALLOWED_MODES, mode)
    save_to_file(file_path, cleaned_input, mode)

    print("入力内容を output_func.txt に保存しました。")
    print(f"ユーザから入力された内容は「{cleaned_input}」です。")
    print(f"保存先ファイルパス: {file_path}")

if __name__ == "__main__":
    main()
