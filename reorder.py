import pandas as pd
import os

# ファイルパス
report_excel = './correct_answer/report_summary.xlsx'
diff_log_file = './correct_answer/diff_log.txt'
reordered_file = './correct_answer/diff_log_reordered.txt'

# Excelファイルを読み込む
df = pd.read_excel(report_excel, sheet_name=0, header=0, dtype=str)
required_columns = ["学生番号", "学年", "組", "番号"]
if not all(col in df.columns for col in required_columns):
    raise ValueError(f"Excelファイルに必要な列 {required_columns} がありません")
filtered_df = df[required_columns]

# 学生番号をキーにした辞書を作成
student_dict = filtered_df.set_index("学生番号").to_dict(orient="index")
#print(student_dict)

# txtファイルを読み込み
with open(diff_log_file, "r", encoding="utf-8") as f:
    txt_lines = f.readlines()

# 学生番号を年組番号に置き換える
processed_lines = []
for line in txt_lines:
    for student_id, info in student_dict.items():
        if student_id in line:
            year_group_num = f"{info['学年']}年{info['組']}組{info['番号']}番"
            line = line.replace(student_id, year_group_num + "', '" + student_id)
    processed_lines.append(line)
print(processed_lines)

# 結果を出力
with open(reordered_file, "w", encoding="utf-8") as f:
    f.writelines(processed_lines)

print(f"処理が完了しました．結果は {reordered_file} に出力されました．")
