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
model_path_list = ["mlx-community/Qwen2-VL-72B-Instruct-4bit",
                "mlx-community/pixtral-12b-8bit"]
#                "mlx-community/Llama-3.2-11B-Vision-Instruct-8bit"]
#                "mlx-community/Qwen2-VL-7B-Instruct-8bit"]
model_name_list = ["Qwen2",
                "Pixtral"]
#mlx-community/Qwen2-VL-7B-Instruct-4bit
#mlx-community/Qwen2-VL-2B-Instruct-bf16
#mlx-community/pixtral-12b-4bit
#mlx-community/Phi-3.5-vision-instruct-bf16
#mlx-community/Phi-3-vision-128k-instruct-4bit
#mlx-community/Llama-3.2-11B-Vision-Instruct-4bit
#mlx-community/Molmo-7B-D-0924-4bit

prompt_list = []
prompt = """
The answers to questions (1) through (50) must be written as single-digit numbers, exactly as shown in the image.
Each answer must strictly adhere to the following format and be written on a separate line:
(Question number) Answer's digit
Example output (for illustration only):
(1) 0
(2) 0
(3) 0
Ensure that the question number is enclosed in parentheses.
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
columns = ["学生番号"] + [f"Q{i:02}" for i in range(1, problem_length+1)]
df0 = txt_to_df.construct_df(dir_students, "_page1-" + model_name_list[0] + ".txt", columns, problem_length)
df1 = txt_to_df.construct_df(dir_students, "_page1-" + model_name_list[1] + ".txt", columns, problem_length)
df_student = df0
print(df_student.head())

# 全ての列について値の違いを検出
differences = (df0 != df1)

# 相違のある行と列を抽出
if differences.any().any():
    diff_indices = differences[differences].stack().index.tolist()
    for row, col in diff_indices:
        log = f"Diff at ID '{df1.at[row,"学生番号"]}', column '{col}': df0={df0.at[row, col]}, df1={df1.at[row, col]}"
        print(log)
        mylib.log_error(log, file_name="./correct_answer/diff_log.txt")
else:
    print("The DataFrames are identical.")

# Excelファイルからデータフレームの作成
report_excel = "./correct_answer/report_summary.xlsx"
df_report = mylib.read_excel(report_excel, sheet_name=0, header=0, dtype=str)
print(df_report.head())

# マージ
merged_df = pd.merge(df_report, df_student, on="学生番号", how="left")
print(merged_df.head())

# データフレームをCSVファイルとして保存
output_file = "./correct_answer/grade.csv"  # 保存するファイル名
merged_df.to_csv(output_file, index=False, encoding="utf-8-sig")
