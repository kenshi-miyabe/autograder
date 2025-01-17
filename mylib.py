import os
import pandas as pd
import csv

# txtファイルを読み込む関数
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

# txtファイルを書き込む関数
def write_text_file(file_path, content):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"ファイルを{file_path}に書き込みました。")
    except Exception as e:
        log_error(f"エラーが発生しました: {e}")

# CSVファイルを読み込む関数
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

# dfをCSVファイルを書き込む関数
def write_df_to_csv(df, filename):
    """
    すべて文字列型の値が含まれているDataFrameをCSV形式で書き出す

    Parameters:
    -----------
    df : pandas.DataFrame
        書き出したいDataFrame
    filename : str
        書き出し先のCSVファイル名
    """
    # 列をすべて文字列型に変換
    df_str = df.astype(str)

    # CSVファイルへ書き出し(index=Falseは行番号を省略)
    df_str.to_csv(filename, index=False, encoding="utf-8")

# 列名のリスト，リストのリストをCSVファイルに書き込む関数
def write_to_csv(file_name, data, col_names):
    """
    リストをCSVファイルに書き込む関数（上書き）。
    
    Parameters:
        file_name (str): 書き込むCSVファイルの名前。
        col_names (list): CSVファイルの列名（最初の行に書き込まれる）。
        data (list): CSVに書き込むリスト（複数行分のデータ）。
        
    注意: この関数は既存の内容を削除して上書きします。
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


# Excelファイルを読み込む関数
def read_excel(file_path, sheet_name=0, header=1, dtype=str):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=header, dtype=dtype)
        print("Excelファイルを正常に読み込みました。")
        return df
    except FileNotFoundError:
        log_error(f"エラー: ファイルが見つかりません: {file_path}")
    except Exception as e:
        log_error(f"エラーが発生しました: {e}")

# エラーメッセージをファイルに記録する関数
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
    
    return error_message

# dir内のstrで終わるファイルすべてにfuncを適用する関数
def repeat_func_in_dir(dir, str, func):
    """
    指定されたディレクトリ内の指定された文字列で終わるファイルに指定された関数を繰り返し適用する関数。

    Parameters:
        dir (str): ファイルを検索するディレクトリのパス。
        func (function): 適用する関数。
        str (str): ファイル名の末尾に含まれる文字列。

    Returns:
        None
    """
    try:
        for file_name in sorted(os.listdir(dir)):
            if file_name.endswith(str):
                file_path = os.path.join(dir, file_name)
                print(f"{file_path}を処理中")
                func(file_path)
    except Exception as e:
        log_error(f"エラーが発生しました: {e}")