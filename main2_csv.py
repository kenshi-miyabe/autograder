
# summary_csvとNA_csvからdfを作る
# Excelファイルからdfを作成
# 2つのdfをマージしてcsvファイルを作成

import pandas as pd
import txt_to_df
import mylib

# 学生の解答用紙ファイルのディレクトリ設定
dir_students = './student_answers'
summary_csv = "./correct_answer/summary.csv"
NA_csv = "./correct_answer/NA.csv"
report_excel = "./correct_answer/report_summary.xlsx"
output_file = "./correct_answer/grade.csv"  # 保存するファイル名


# summary_csvとNA_csvからdfを作成
df_summary = pd.read_csv(summary_csv, header=0, dtype=str)
df_NA = pd.read_csv(NA_csv, header=0, dtype=str)

# df_summaryを修正
# 各行を処理
for _, row in df_NA.iterrows():
    NA_dict = row.to_dict()
    ID, q_num, ans = NA_dict["学生番号"], NA_dict["Question"], NA_dict["Value"]
    index = df_summary[df_summary["学生番号"] == ID].index.item()
    df_summary.at[index, q_num] = ans

# Excelファイルからデータフレームの作成
df_report = mylib.read_excel(report_excel, sheet_name=0, header=0, dtype=str)
#print(df_report.head())

# マージ
merged_df = pd.merge(df_report, df_summary, on="学生番号", how="left")
#print(merged_df.head())

# データフレームをCSVファイルとして保存
merged_df.to_csv(output_file, index=False, encoding="utf-8-sig")