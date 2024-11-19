import pandas as pd
import os

def read_row_from_all_txt(directory, end_text, line_num):
    """
    指定されたディレクトリ内のすべてのTXTファイルから2行目を読み込み、
    データフレームに格納する関数。

    Parameters:
        directory (str): 対象のディレクトリパス。
        end_text (str): ファイル名の末尾にある文字列。
        line_num (int): 取得する行番号。

    Returns:
        pd.DataFrame: すべての2行目を1つにまとめたデータフレーム。
    """
    all_data = []  # 2行目のデータを格納するリスト

    # ディレクトリ内のすべてのファイルを走査
    for file_name in os.listdir(directory):
        if file_name.endswith(end_text):  # txtファイルのみ処理
            file_path = os.path.join(directory, file_name)
            
            try:
                # CSVファイルを読み込み、2行目を取得
                df = pd.read_csv(file_path, header=None)
                row = df.iloc[line_num-1]  # line_num 行目
                all_data.append(row)  # リストに追加
            except Exception as e:
                print(f"エラー: {file_path}の読み込みに失敗しました: {e}")
    
    # リストからデータフレームを作成
    #return all_data
    result_df = pd.DataFrame(all_data)
    return result_df

