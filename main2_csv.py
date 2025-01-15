
# txtからcsvへの変換
# target_substrが含まれるファイルからcsvファイルを作成

import pandas as pd
import txt_to_df
import mylib

dir_students = './student_answers'
target_substr = "_page1-QVQ.txt"
report_excel = "./correct_answer/report_summary.xlsx"
output_file = "./correct_answer/grade.csv"  # 保存するファイル名
problem_length = 50

#テキストファイルからデータフレームの作成
columns = ["学生番号"] + [f"Q{i:02}" for i in range(1, problem_length+1)]
df_student = txt_to_df.construct_df(dir_students, target_substr, columns, problem_length)
print(df_student.head())

# Excelファイルからデータフレームの作成
df_report = mylib.read_excel(report_excel, sheet_name=0, header=0, dtype=str)
print(df_report.head())

# マージ
merged_df = pd.merge(df_report, df_student, on="学生番号", how="left")
print(merged_df.head())

# データフレームをCSVファイルとして保存
merged_df.to_csv(output_file, index=False, encoding="utf-8-sig")