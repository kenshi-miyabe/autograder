import pandas as pd

def load_csv(file_path):
    """
    指定されたCSVファイルを読み込む関数。

    Parameters:
        file_path (str): 読み込むCSVファイルのパス。

    Returns:
        pandas.DataFrame: 読み込んだデータフレーム。
    """
    try:
        # CSVファイルを読み込む
        data = pd.read_csv(file_path, header=None)
        print("CSVファイルを正常に読み込みました。")
        # データの先頭5行を表示
        print(data.head())
        return data
    except FileNotFoundError:
        log_error(f"エラー: ファイルが見つかりません: {file_path}")

    except pd.errors.EmptyDataError:
        log_error("エラー: ファイルが空です: {file_path}")
    except pd.errors.ParserError:
        log_error("エラー: ファイルの形式が正しくありません。")
    return None

"""
# test
if __name__ == "__main__":
    # ユーザーからCSVファイル名を入力として取得
    file_path = input("CSVファイルの名前を入力してください（パスも含む場合があります）: ").strip()
    
    # CSVファイルを読み込む
    df = load_csv(file_path)
"""

def log_error(error_message, file_name="error.txt"):
    """
    エラーメッセージを指定されたファイルに追記する関数。

    Parameters:
        error_message (str): ログとして記録するエラーメッセージ。
        file_name (str): エラーログを記録するファイル名（デフォルトは 'error.txt'）。
    """
    
    print(error_message)

    try:
        with open(file_name, "a", encoding="utf-8") as file:
            file.write(error_message + "\n")
        print(f"エラーが{file_name}に記録されました。")
    except Exception as e:
        print(f"エラーログの記録に失敗しました: {e}")

