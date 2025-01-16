
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
import image_to_text_ollama
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
# モデル名、プロンプトを設定
arg_list = [
    {'model_path': "mlx-community/QVQ-72B-Preview-4bit", 'model_name': "QVQ", 'type': "mlx", 'max_tokens': 15000}, #0.95
    {'model_path': "mlx-community/Qwen2-VL-72B-Instruct-4bit", 'model_name': "Qwen-72B", 'type': "mlx", 'max_tokens': 10000}, #0.88
    {'model_path': "mlx-community/Qwen2-VL-7B-Instruct-8bit", 'model_name': "Qwen-7B", 'type': "mlx", 'max_tokens': 5000}, #0.80
    {'model_path': "mlx-community/pixtral-12b-8bit", 'model_name': "Pixtral", 'type': "mlx", 'max_tokens': 5000}, #0.82
    {'model_path': "llama3.2-vision:90b", 'model_name': "llama-90B", 'type': "ollama", 'max_tokens': 5000}, #0.70
    {'model_path': "llama3.2-vision", 'model_name': "llama-11B", 'type': "ollama", 'max_tokens': 5000}, #0.81
#    {'model_path': "mlx-community/Llama-3.2-11B-Vision-Instruct-8bit", 'model_name': "llama-11B-mlx", 'type': "mlx", 'max_tokens': 5000}, #0.76
#    {'model_path': "llava:34b", 'model_name': "llava", 'type': "ollama", 'max_tokens': 5000}, #0.058
#    {'model_path': "minicpm-v", 'model_name': "minicpm", 'type': "ollama", 'max_tokens': 5000} #0.45
]
#arg_list = [
#    {'model_path': "mlx-community/pixtral-12b-4bit", 'model_name': "Pixtral", 'type': "mlx", 'max_tokens': 5000}, #0.87
#    {'model_path': "mlx-community/Qwen2-VL-7B-Instruct-8bit", 'model_name': "Qwen", 'type': "mlx", 'max_tokens': 5000}, #0.73
#    {'model_path': "llava:13b", 'model_name': "llava", 'type': "ollama", 'max_tokens': 5000}, #0.12
#    {'model_path': "llama3.2-vision", 'model_name': "llama", 'type': "ollama", 'max_tokens': 5000}, #0.83
#    {'model_path': "minicpm-v", 'model_name': "minicpm", 'type': "ollama", 'max_tokens': 5000}
#]


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
If the answer is a cross mark or blank, replace `Answer's digit' with `_'.
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

        for model_info in arg_list:
            model_path = model_info['model_path']
            model_name = model_info['model_name']
            model_type = model_info['type']
            max_tokens = model_info['max_tokens']
            if model_type == "mlx":
                print(f"{model_path}で{image_path}を処理中")
                output = image_to_text.process_images_with_prompt(model_path, [image_path], prompt, max_tokens)
            elif model_type == "ollama":
                print(f"{model_path}で{image_path}を処理中")
                output = image_to_text_ollama.process_images_with_prompt(model_path, [image_path], prompt, max_tokens)
            else :
                print("Error: unknown model type.")
                break
            final_output = image_to_text.extract_from_marker(output, "Final Answer")

            # テキストファイルに出力
            base, ext = os.path.splitext(image_path)
            txt_path = base + "-" + model_name + ".txt"
            mylib.write_text_file(txt_path, final_output)
#"""

#テキストファイルからデータフレームの作成
problem_length = 50
columns = ["学生番号"] + [f"Q{i:02}" for i in range(1, problem_length+1)]
df_list = []
for model_info in arg_list:
    model_name = model_info['model_name']
    df_list.append(txt_to_df.construct_df(dir_students, "_page1-" + model_name + ".txt", columns, problem_length))
df_majority = txt_to_df.majority_vote_from_list(df_list)
print(df_majority.head())
for df in df_list:
    print(txt_to_df.calculate_match_rate(df_majority, df))

#differences = []
#for row in range(df0.shape[0]):
#    for col in range(df0.shape[1]):
#        if df0.iat[row, col] != df1.iat[row, col] or df0.iat[row, col] != df2.iat[row, col]:
#        if df0.iat[row, col] != df1.iat[row, col]:
#            differences.append((row, col))

# 相違のある行と列を抽出
#if differences:
#    for row, col in differences:
#        log = f"Diff at ID '{df0.at[row,"学生番号"]}', column '{col}': df0={df0.iat[row, col]}, df1={df1.iat[row, col]}, df2={df2.iat[row, col]}"
#        print(log)
#        mylib.log_error(log, file_name=diff_log)
#else:
#    print("No objection.")


