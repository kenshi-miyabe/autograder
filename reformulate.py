import pandas as pd
import os

def read_second_row_from_all_txt(directory):
    """
    指定されたディレクトリ内のすべてのTXTファイルから2行目を読み込み、
    データフレームに格納する関数。

    Parameters:
        directory (str): 対象のディレクトリパス。

    Returns:
        pd.DataFrame: すべての2行目を1つにまとめたデータフレーム。
    """
    all_data = []  # 2行目のデータを格納するリスト

    # ディレクトリ内のすべてのファイルを走査
    for file_name in os.listdir(directory):
        if file_name.endswith("-grade.txt"):  # txtファイルのみ処理
            file_path = os.path.join(directory, file_name)
            
            try:
                # CSVファイルを読み込み、2行目を取得
                df = pd.read_csv(file_path, header=None)
                second_row = df.iloc[1]  # 2行目（インデックス1）
                all_data.append(second_row)  # リストに追加
            except Exception as e:
                print(f"エラー: {file_path}の読み込みに失敗しました: {e}")
    
    # リストからデータフレームを作成
    #return all_data
    result_df = pd.DataFrame(all_data)
    return result_df

