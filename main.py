import os
import pandas as pd
import re
import mylib
import pdf_to_jpg
import image_to_text

# 学生の解答用紙ファイルのディレクトリ設定
dir_students = './student_answers'

# pdfファイルをjpgに変換
#"""
for file_name in sorted(os.listdir(dir_students)):
    if file_name.endswith(".pdf"):
        pdf_path = os.path.join(dir_students, file_name)
        print(f"{pdf_path}を処理中")
        pdf_to_jpg.convert_pdf_to_jpg(pdf_path)
#"""

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

#"""
for file_name in sorted(os.listdir(dir_students)):
    if file_name.endswith("_page1.jpg"):
        image_path = os.path.join(dir_students, file_name)

        print(f"{image_path}を処理中")
        output_list = image_to_text.process_images_with_prompt(model_path, [image_path], prompt_list)
        
        # テキストファイルに出力
        base, ext = os.path.splitext(image_path)
        txt_path = base + ".txt"
        mylib.write_text_file(txt_path, output_list)
#"""

#テキストファイルからデータフレームの作成
columns = ["学生番号"] + [f"Q{i}" for i in range(1, problem_length+1)]
df_student = pd.DataFrame(columns=columns)
for file_name in sorted(os.listdir(dir_students)):
    if file_name.endswith("_page1.txt"):
        txt_path = os.path.join(dir_students, file_name)
        print(f"{txt_path}を処理中")
        content = mylib.read_text_file(txt_path)
        cleaned_text = re.sub(r"[^\d()\n]","", content)
        answer_list = [None] * problem_length
        for i in range(1,problem_length+1):
            match = re.search(rf"\({i}\)(\S+)", cleaned_text)
            if match:
                answer_list[i-1] = match.group(1)
        answer_list.insert(0, os.path.basename(txt_path)[:10])
        df_student.loc[len(df_student)] = answer_list
        print(answer_list)

# Excelファイルからデータフレームの作成
report_excel = "./correct_answer/report_summary.xlsx"
df_report = mylib.read_excel(report_excel, sheet_name=0, header=0, dtype=str)

# マージ
merged_df = pd.merge(df_report, df_student, on="学生番号", how="left")
print(merged_df.head())

# データフレームをCSVファイルとして保存
output_file = "./correct_answer/grade.csv"  # 保存するファイル名
merged_df.to_csv(output_file, index=False, encoding="utf-8-sig")
