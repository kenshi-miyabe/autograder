import os
import pandas as pd
import re
import mylib
import pdf_to_jpg
import image_to_text
import check
import reformulate

# 学生の解答用紙ファイルのディレクトリ設定
dir_students = './student_answers'

# pdfファイルをjpgに変換
for file_name in sorted(os.listdir(dir_students)):
    if file_name.endswith(".pdf"):
        pdf_path = os.path.join(dir_students, file_name)
        print(f"{pdf_path}を処理中")
        pdf_to_jpg.convert_pdf_to_jpg(pdf_path)

# 画像からテキストを抽出
problem_length = 50
# モデル名、プロンプトを設定
model_path = "mlx-community/Qwen2-VL-7B-Instruct-4bit"
prompt_list = []
prompt = """
The answers to problems (1) through (50) are written as single-digit numbers.
Provide the answers in the format '(problem-number) digit'. Example:  
===
(1) 0
(2) 0
(3) 0
...
(50) 0
===
"""
prompt_list.append(prompt)

for file_name in sorted(os.listdir(dir_students)):
    if file_name.endswith("_page1.jpg"):
        image_path = os.path.join(dir_students, file_name)

        print(f"{image_path}を処理中")
        output_list = image_to_text.process_images_with_prompt(model_path, [image_path], prompt_list)
        
        # テキストファイルに出力
        base, ext = os.path.splitext(image_path)
        txt_path = base + ".txt"
        mylib.write_text_file(txt_path, output_list)


# モデル名、プロンプトを設定
model_path = "mlx-community/Mistral-7B-Instruct-v0.3-4bit"
prompt0 = """
The answers to problems (1) through (50) are written as single-digit numbers.
Output the answers separated by commas in order. Example:
===
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ...
===
"""


#"""
for file_name in sorted(os.listdir(dir_students)):
    if file_name.endswith("_page1.txt"):
        txt_path = os.path.join(dir_students, file_name)
        print(f"{txt_path}を処理中")
        content = mylib.read_text_file(txt_path)
        prompt = prompt0 + content
        student_answer = check.generate_with_prompt(model_path, prompt)
        student_answer = re.sub(r'[^0-9,]', '', student_answer) # 数字とカンマ以外を削除
        print(student_answer)
        student_answer_list = check.text_to_list(student_answer, problem_length)
        student_answer_list.insert(0, "-".join(student_answer_list))
        student_answer_list.insert(0, os.path.basename(txt_path)[:10])
        student_answer_list.insert(0, os.path.basename(txt_path))
        
        # テキストファイルに出力
        base, ext = os.path.splitext(txt_path)
        txt_path = base + "-grade.txt"
        mylib.write_to_csv(txt_path, [student_answer_list], None)
#"""

# Excelファイルと同じ行になるように成績を整形
report_excel = "./correct_answer/report_summary.xlsx"
df_report = mylib.read_excel(report_excel, sheet_name=0, header=0, dtype=str)

# 学生の成績
df_student = reformulate.read_row_from_all_txt(directory = dir_students, end_text = "-grade.txt", line_num = 1)
df_student.columns = ["ファイル名", "学生番号", "結合文字列"] + [f"Q{i}" for i in range(1, problem_length+1)]
#print(df_student)

merged_df = pd.merge(df_report, df_student, on="学生番号", how="left")
print(merged_df.head())

# データフレームをCSVファイルとして保存
output_file = "./correct_answer/grade.csv"  # 保存するファイル名
merged_df.to_csv(output_file, index=False, encoding="utf-8-sig")
