import pandas as pd
import csv

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

def write_to_csv(file_name, data, col_names):
    """
    リストをCSVファイルに追記する関数。
    
    Parameters:
        file_name (str): 書き込むCSVファイルの名前。
        col_names (list): CSVファイルの列名。
        data (list): CSVに追記するリスト（複数行分のデータ）。
    """
    try:
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if col_names is not None:
                writer.writerow(col_names)
            writer.writerows(data)
        print(f"データを{file_name}に書き込みました。")
    except Exception as e:
        log_error(f"エラーが発生しました: {e}")


# ファイルを読み込む関数
def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            #print(content)  # ファイル内容を表示
            return content  # 必要なら内容を返す
    except FileNotFoundError:
        log_error(f"ファイルが見つかりません: {file_path}")
    except Exception as e:
        log_error(f"エラーが発生しました: {e}")

# ファイルを書き込む関数
def write_text_file(file_path, content_list):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            # 各要素を1行ずつ書き込む
            for line in content_list:
                file.write(line + "\n")  # 各行の最後に改行を追加
        print(f"ファイルを{file_path}に書き込みました。")
    except Exception as e:
        log_error(f"エラーが発生しました: {e}")

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

