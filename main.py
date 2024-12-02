import os
import pandas as pd
import re
import mylib
import pdf_to_jpg
import image_to_text
import txt_to_df

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
model_path_list = ["mlx-community/Qwen2-VL-7B-Instruct-4bit",
                "mlx-community/pixtral-12b-4bit"]
model_name_list = ["Qwen2",
                "Pixtral"]
#mlx-community/Qwen2-VL-7B-Instruct-4bit
#mlx-community/Qwen2-VL-2B-Instruct-bf16
#mlx-community/pixtral-12b-4bit
#mlx-community/Phi-3.5-vision-instruct-bf16
#mlx-community/Phi-3-vision-128k-instruct-4bit
#mlx-community/Llama-3.2-3B-Instruct-8bit
prompt_list = []
prompt = """
The answers to problems (1) through (50) are written as single-digit numbers.
Provide only the answers in the format '(problem-number) digit'. Example:  
===
Answers:
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
        for model_path, model_name in zip(model_path_list, model_name_list):
            output_list = image_to_text.process_images_with_prompt(model_path, [image_path], prompt_list)

            # テキストファイルに出力
            base, ext = os.path.splitext(image_path)
            txt_path = base + "-" + model_name + ".txt"
            mylib.write_text_file(txt_path, output_list)
#"""

#テキストファイルからデータフレームの作成
columns = ["学生番号"] + [f"Q{i}" for i in range(1, problem_length+1)]
df1 = txt_to_df.construct_df(dir_students, "_page1-Qwen2.txt", columns, problem_length)
df2 = txt_to_df.construct_df(dir_students, "_page1-Pixtral.txt", columns, problem_length)
df_student = df1
print(df_student.head())

# 全ての列について値の違いを検出
differences = (df1 != df2)

# 相違のある行と列を抽出
if differences.any().any():
    diff_indices = differences[differences].stack().index.tolist()
    for row, col in diff_indices:
        log = f"Difference found at row {row}, column '{col}': df1={df1.at[row, col]}, df2={df2.at[row, col]}"
        print(log)
        mylib.log_error(log, file_name="./correct_answer/diff_log.txt")
else:
    print("The DataFrames are identical.")

# Excelファイルからデータフレームの作成
report_excel = "./correct_answer/report_summary.xlsx"
df_report = mylib.read_excel(report_excel, sheet_name=0, header=0, dtype=str)

# マージ
merged_df = pd.merge(df_report, df_student, on="学生番号", how="left")
print(merged_df.head())

# データフレームをCSVファイルとして保存
output_file = "./correct_answer/grade.csv"  # 保存するファイル名
merged_df.to_csv(output_file, index=False, encoding="utf-8-sig")
