
import os
import re
import pandas as pd
import numpy as np
from collections import Counter
import mylib

def construct_df(dir_name, end_str, columns, problem_length):
    df = pd.DataFrame(columns=columns)
    for file_name in sorted(os.listdir(dir_name)):
        if file_name.endswith(end_str):
            txt_path = os.path.join(dir_name, file_name)
            print(f"{txt_path}を処理中")
            content = mylib.read_text_file(txt_path)

            # マーカー以降を抽出
            marker_index = content.rfind("Final Answer")
            if marker_index != -1:
                final_answer = content[marker_index:]

            # 数字、()、X 以外を削除
            cleaned_text = re.sub(r"[^\d\(\)X\n]", "", final_answer)
            answer_list = ["NA"] * problem_length  # 初期値を "NA" に設定
            
            for i in range(1, problem_length + 1):
                # (i)の次の数字もしくはXを取得
                match = re.search(rf"\({i}\)\s*([\dX])?", cleaned_text)
                if match and match.group(1):  # 解答が存在する場合のみ値を設定
                    answer_list[i - 1] = match.group(1)
            
            # ファイル名から最初の10文字を抽出して挿入
            answer_list.insert(0, os.path.basename(txt_path)[:10])
            # データフレームに行を追加
            df.loc[len(df)] = answer_list
    return df

def majority_vote_from_list(df_list):
    """
    リストで与えられたデータフレームから多数決で1つのデータフレームを作成。
    同点の場合は最初に出現した値を優先する。
    """
    if len(df_list) == 0:
        raise ValueError("データフレームのリストが空です。")
    
    # 全てのデータフレームを3次元配列にスタック
    stacked = np.stack([df.values for df in df_list], axis=2)
    
    # 各要素で多数決を取る関数
    def vote(values):
        unique, counts = np.unique(values, return_counts=True)
        # 同点時に最初に出現した値を優先
        max_count = counts.max()
        candidates = unique[counts == max_count]
        for value in values:
            if value in candidates:
                return value
    
    # 全ての要素で多数決を適用
    majority_values = np.apply_along_axis(vote, axis=2, arr=stacked)
    
    # 新しいデータフレームを作成して返す
    return pd.DataFrame(majority_values, columns=df_list[0].columns, index=df_list[0].index)

def calculate_match_rate(df1, df2, fill_value=None):
    """
    2つのDataFrameの一致率を計算する関数。

    Parameters:
        df1 (pd.DataFrame): 比較対象の最初のDataFrame。
        df2 (pd.DataFrame): 比較対象の2番目のDataFrame。
        fill_value (optional): 欠損値を埋めるための値。デフォルトはNone（欠損値をそのまま比較）。

    Returns:
        float: 一致率（0から1の範囲）。

    Raises:
        ValueError: データフレームの形状が異なる場合に例外を発生。
    """
    # データフレームの形状確認
    if df1.shape != df2.shape:
        raise ValueError("データフレームの形状が異なります。")

    # 欠損値の処理
    if fill_value is not None:
        df1 = df1.fillna(fill_value)
        df2 = df2.fillna(fill_value)

    # 要素ごとの比較
    comparison = df1 == df2

    # 一致数のカウント
    match_count = comparison.values.sum()

    # 全要素数の取得
    total_elements = df1.size

    # 一致率の計算
    match_rate = match_count / total_elements

    return match_rate

def get_consensus_answer(answers, threshold=0.5):
    """
    複数のモデルの答え(answers)が与えられたとき，
    出現回数が threshold を超える答えがあればそれを返し，
    なければ 'NA' を返す関数．
    """
    if not answers:
        return "NA"

    counter = Counter(answers)
    # 最も多く選ばれている答えとその回数を取得
    most_common_answer, most_common_count = counter.most_common(1)[0]

    # しきい値を超えているか判定
    if most_common_count / len(answers) >= threshold:
        return most_common_answer
    else:
        return "NA"

def consensus_df(dfs, threshold=0.5):
    """
    dfs: list of pandas.DataFrame
        同じ形を持つDataFrameのリスト

    returns
        合意形成後のDataFrame
    """
    # ここでは，dfsに含まれるDataFrameすべてが
    # 同じindexおよびcolumnsを持っていると仮定します
    base_df = dfs[0]
    new_df = pd.DataFrame(index=base_df.index, columns=base_df.columns)

    # 行と列を総当たりしながら処理
    for i in range(len(base_df.index)):
        for j in range(len(base_df.columns)):
            # i行j列に対応するすべてのdfsの値をリストにまとめる
            elements = [df.iloc[i, j] for df in dfs]

            # get_consensus_answerで合意形成
            new_df.iloc[i, j] = get_consensus_answer(elements, threshold)

    return new_df

if __name__ == "__main__":
    problem_length = 50
    columns = ["学生番号"] + [f"Q{i}" for i in range(1, problem_length+1)]
    df = construct_df('./student_answers', "_page1-Qwen2.txt", columns, problem_length)
    print(df.head())