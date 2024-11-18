import os
import pandas as pd
import mylib
import pdf_to_jpg
import image_to_text
import check
import reformulate

# 学生の解答用紙ファイルのディレクトリ設定
dir_students = './student_answers'

"""
# pdfファイルをjpgに変換
for file_name in sorted(os.listdir(dir_students)):
    if file_name.endswith(".pdf"):
        pdf_path = os.path.join(dir_students, file_name)
        print(f"{pdf_path}を処理中")
        pdf_to_jpg.convert_pdf_to_jpg(pdf_path)
"""

# 画像からテキストを抽出
# モデル名、プロンプトを設定
model_path = "mlx-community/Qwen2-VL-7B-Instruct-4bit"
prompt_list = []
prompt_list.append("Provide the student ID (starting with 158R).")
prompt_list.append("The student's grade is 1, 2, 3 or 4, the student's class is 16. Then, what is the student's number?")
prompt_list.append("The answers to problems (1) through (5) are written in uppercase letters of the alphabet. State what each of them is.")
prompt_list.append("The answers to problems (6) through (10) are written in lowercase letters of the alphabet. State what each of them is.")
prompt_list.append("The answers to problems (11) through (15) are written as single-digit numbers. State what each of them is.")
prompt_list.append("The answers for Question (16)-(20) are written as fractions. Provide each of them in the format ?/?")

for file_name in sorted(os.listdir(dir_students)):
    if file_name.endswith("_page1.jpg"):
        image_path = os.path.join(dir_students, file_name)

        print(f"{image_path}を処理中")
        output_list = image_to_text.process_images_with_prompt(model_path, [image_path], prompt_list)
        
        # テキストファイルに出力
        base, ext = os.path.splitext(image_path)
        txt_path = base + ".txt"
        with open(txt_path, "w", encoding="utf-8") as file:
            # 各要素を1行ずつ書き込む
            for line in output_list:
                file.write(line + "\n")  # 各行の最後に改行を追加

"""
# 解答の正誤判定
answer_file = "./correct_answer/answer.csv"
df_correct_answer = mylib.load_csv(answer_file)
if df_correct_answer is None:
    mylib.log_error("エラー: 模範解答ファイルからデータを読み込めませんでした．")

for file_name in sorted(os.listdir(dir_students)):
    if file_name.endswith(".txt"):
        txt_path = os.path.join(dir_students, file_name)
        print(f"{txt_path}を処理中")
        df_your_answer = mylib.load_csv(txt_path)
        if df_your_answer is None:
            mylib.log_error("エラー: 学生解答ファイルからデータを読み込めませんでした．")

        # 比較
        result = check.compare_lists(df_correct_answer.iloc[0], df_your_answer.iloc[0])
        print(result)

        # 結果をCSVファイルに追記
        mylib.write_to_csv(txt_path, result, mode='a')

# Excelファイルと同じ行になるように成績を整形
report_excel = "./correct_answer/report_summary.xlsx"
# レポートまとめファイルから2番目のシート（インデックス1）を読み込む
try:
    df_report = pd.read_excel(report_excel, sheet_name=1, header=1, dtype=str)
except Exception as e:
    print(f"エラーが発生しました: {e}")
    exit()
#print(df_report.head())

# 使用例
df_student = reformulate.read_second_row_from_all_txt(dir_students)

# 結果を表示
df_student.columns = ["ファイル名", "学生番号"] + [f"Q{i}" for i in range(1, 11)]  # Q1～Q10
print(df_student)

merged_df = pd.merge(df_report, df_student, on="学生番号", how="left")
print(merged_df.head())

# データフレームをCSVファイルとして保存
output_file = "./correct_answer/grade.csv"  # 保存するファイル名
merged_df.to_csv(output_file, index=False, encoding="utf-8-sig")
"""


