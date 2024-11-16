import pandas as pd
import os

report_excel = "./correct_answer/report_summary.xlsx"

# レポートまとめファイルから2番目のシート（インデックス1）を読み込む
try:
    df_report = pd.read_excel(report_excel, sheet_name=1, header=1)
except Exception as e:
    print(f"エラーが発生しました: {e}")
    exit()

print(df_report.head())

def read_second_row_from_all_csv(directory):
    """
    指定されたディレクトリ内のすべてのCSVファイルから2行目を読み込み、
    データフレームに格納する関数。

    Parameters:
        directory (str): 対象のディレクトリパス。

    Returns:
        pd.DataFrame: すべての2行目を1つにまとめたデータフレーム。
    """
    all_data = []  # 2行目のデータを格納するリスト

    # ディレクトリ内のすべてのファイルを走査
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):  # CSVファイルのみ処理
            file_path = os.path.join(directory, file_name)
            
            try:
                # CSVファイルを読み込み、2行目を取得
                df = pd.read_csv(file_path, header=None)
                second_row = df.iloc[1]  # 2行目（インデックス1）
                all_data.append(second_row)  # リストに追加
            except Exception as e:
                print(f"エラー: {file_path}の読み込みに失敗しました: {e}")
    
    # リストからデータフレームを作成
    result_df = pd.DataFrame(all_data)
    return result_df

# 使用例
directory_path = "student_answers"  # ディレクトリのパスを指定
df_student = read_second_row_from_all_csv(directory_path)

# 結果を表示
df_student.columns = ["Grd", "Cls", "Num", "学生番号"] + [f"Q{i}" for i in range(1, 11)] + ["NA"]  # Q1～Q1
print(df_student)

merged_df = pd.merge(df_report, df_student, on="学生番号")
print(merged_df.head())

# データフレームをCSVファイルとして保存
output_file = "./correct_answer/grade.csv"  # 保存するファイル名
merged_df.to_csv(output_file, index=False, encoding="utf-8-sig")