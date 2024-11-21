
import os
import pandas as pd
import mylib

dir_student = "./student_answers"
report_excel = "./correct_answer/report_summary.xlsx"

# レポートまとめファイルを読み込む
df_report = mylib.read_excel(report_excel, sheet_name=0, header=0, dtype=str)
df_report["識別子"] = df_report[["所属", "学年", "組", "番号"]].fillna("").agg("".join, axis=1)
print(df_report.head())

# ディレクトリ内のファイルを取得
for file_name in os.listdir(dir_student):
    # ファイル名が数字で始まり、.pdfで終わるものを判定
    if file_name[0].isdigit():
        # 最初の10文字を取り出す
        file_prefix = file_name[:10]

        # データフレームから学生番号が一致する行を探す
        matching_row = df_report[df_report["学生番号"] == file_prefix]

        # 一致する行が存在する場合
        if not matching_row.empty:
            # 「識別子」の値を取得
            identifier = matching_row.iloc[0]["識別子"]

            # 新しいファイル名を作成
            new_file_name = f"{identifier}_{file_name}"

            # ファイルのリネーム処理
            old_file_path = os.path.join(dir_student, file_name)
            new_file_path = os.path.join(dir_student, new_file_name)
            os.rename(old_file_path, new_file_path)

            print(f"Renamed: {file_name} -> {new_file_name}")