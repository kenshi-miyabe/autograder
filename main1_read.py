
# pdfから文字を読み取りtxtファイルに保存
# 複数モデルで結果を比較して差異を抽出する
# その後，手動でdiff_log, txt, pdfを見ながらtxtを修正する

# 学生の解答用紙ファイルのディレクトリ設定
dir_students = './student_answers'
diff_log = "./correct_answer/diff_log.txt"

import os
import pandas as pd
import re
import mylib
import pdf_to_jpg
import image_to_text
import txt_to_df


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
model_path_list = ["mlx-community/QVQ-72B-Preview-4bit",
                "mlx-community/Qwen2-VL-72B-Instruct-4bit"]
model_name_list = ["QVQ",
                "Qwen2-72B"]
#mlx-community/Qwen2-VL-7B-Instruct-4bit
#mlx-community/Qwen2-VL-2B-Instruct-bf16
#mlx-community/pixtral-12b-4bit
#mlx-community/Phi-3.5-vision-instruct-bf16
#mlx-community/Phi-3-vision-128k-instruct-4bit
#mlx-community/Llama-3.2-11B-Vision-Instruct-4bit
#mlx-community/Molmo-7B-D-0924-4bit

prompt = """
The main section of the document consists of a grid with 50 questions, numbered from 1 to 50.
Each question has a single-digit handwritten answer or a cross mark.
Your task is to output the answers accurately in plain text directly within this response, without referencing or creating any files.

First, output the points to be noted.
Then, output the string `**Final Answer**' followed by the answers to the questions.
Format each answer on a separate line in the following style without using TeX formatting:
=====
(Question number) Answer's digit
=====
Make sure the question number is enclosed in parentheses.
If the answer is a cross mark, replace `Answer's digit' with `_'.
If the answer is illegible, replace it with `?'.

Example final output:
=====
**Final Answer**
(1) 0
(2) 0
(3) _
(4) ?
=====

Ensure the final output is in plain text format, without TeX formatting or file references.
"""

#"""
for file_name in sorted(os.listdir(dir_students)):

    if file_name.endswith("_page1.jpg"):
        image_path = os.path.join(dir_students, file_name)

        print(f"{image_path}を処理中")
        for model_path, model_name in zip(model_path_list, model_name_list):
            output = image_to_text.process_images_with_prompt(model_path, [image_path], prompt)
            final_output = image_to_text.extract_from_marker(output, "Final Answer")

            # テキストファイルに出力
            base, ext = os.path.splitext(image_path)
            txt_path = base + "-" + model_name + ".txt"
            mylib.write_text_file(txt_path, final_output)
#"""

#テキストファイルからデータフレームの作成
columns = ["学生番号"] + [f"Q{i:02}" for i in range(1, problem_length+1)]
df0 = txt_to_df.construct_df(dir_students, "_page1-" + model_name_list[0] + ".txt", columns, problem_length)
df1 = txt_to_df.construct_df(dir_students, "_page1-" + model_name_list[1] + ".txt", columns, problem_length)
#df2 = txt_to_df.construct_df(dir_students, "_page1-" + model_name_list[2] + ".txt", columns, problem_length)
df_student = df0
print(df_student.head())

differences = []
for row in range(df0.shape[0]):
    for col in range(df0.shape[1]):
#        if df0.iat[row, col] != df1.iat[row, col] and df1.iat[row, col] == df2.iat[row, col]:
        if df0.iat[row, col] != df1.iat[row, col]:
            differences.append((row, col))

# 相違のある行と列を抽出
if differences:
    for row, col in differences:
        log = f"Diff at ID '{df0.at[row,"学生番号"]}', column '{col}': df0={df0.iat[row, col]}, df1={df1.iat[row, col]}"
        print(log)
        mylib.log_error(log, file_name=diff_log)
else:
    print("No shared objection.")


