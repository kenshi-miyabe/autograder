
# pdfからjpgを作る
# jpgから文字を読み取りtxtファイルに保存
# txtファイルを集計し，多数決をとってdfを作成
# dfからcsvファイルと，エラー処理用のcsvファイルを作成

import mylib
import pdf_to_jpg
import image_to_text
import txt_to_df
import df_to_csv
import pandas as pd

# 学生の解答用紙ファイルのディレクトリ設定
dir_students = './student_answers'
summary_csv = "./correct_answer/summary.csv"
NA_csv = "./correct_answer/NA.csv"

# pdfファイルをjpgに変換
mylib.repeat_func_in_dir(dir_students, ".pdf", pdf_to_jpg.convert_pdf_to_jpg)

# 画像からテキストを抽出
# モデルを設定
#"""
arg_list = [
    {'model_path': "mlx-community/QVQ-72B-Preview-4bit", 'model_name': "QVQ", 'type': "mlx", 'max_tokens': 15000, 'temp': 0}, #0.993
    {'model_path': "mlx-community/Qwen2-VL-72B-Instruct-4bit", 'model_name': "Qwen-72B-0", 'type': "mlx", 'max_tokens': 10000, 'temp': 0.4}, #0.993
    {'model_path': "mlx-community/Qwen2-VL-72B-Instruct-4bit", 'model_name': "Qwen-72B-1", 'type': "mlx", 'max_tokens': 10000, 'temp': 0.4}, #0.993
#    {'model_path': "mlx-community/Qwen2-VL-72B-Instruct-4bit", 'model_name': "Qwen-72B-2", 'type': "mlx", 'max_tokens': 10000, 'temp': 0.4}, #0.993
#    {'model_path': "mlx-community/pixtral-12b-8bit", 'model_name': "Pixtral-0", 'type': "mlx", 'max_tokens': 5000, 'temp': 0.4}, #0.96
#    {'model_path': "mlx-community/pixtral-12b-8bit", 'model_name': "Pixtral-1", 'type': "mlx", 'max_tokens': 5000, 'temp': 0.4}, #0.96
#    {'model_path': "mlx-community/pixtral-12b-8bit", 'model_name': "Pixtral-2", 'type': "mlx", 'max_tokens': 5000, 'temp': 0.4}, #0.96
#    {'model_path': "mlx-community/Qwen2-VL-7B-Instruct-8bit", 'model_name': "Qwen-7B", 'type': "mlx", 'max_tokens': 5000}, #0.80
#    {'model_path': "llama3.2-vision:90b", 'model_name': "llama-90B", 'type': "ollama", 'max_tokens': 5000}, #0.70
#    {'model_path': "llama3.2-vision", 'model_name': "llama-11B", 'type': "ollama", 'max_tokens': 5000}, #0.81
#    {'model_path': "mlx-community/Llama-3.2-11B-Vision-Instruct-8bit", 'model_name': "llama-11B-mlx", 'type': "mlx", 'max_tokens': 5000}, #0.76
#    {'model_path': "llava:34b", 'model_name': "llava", 'type': "ollama", 'max_tokens': 5000}, #0.058
#    {'model_path': "minicpm-v", 'model_name': "minicpm", 'type': "ollama", 'max_tokens': 5000} #0.45
]
#"""
"""
arg_list = [
    {'model_path': "mlx-community/pixtral-12b-4bit", 'model_name': "Pixtral-0", 'type': "mlx", 'max_tokens': 5000, 'temp': 0.4}, #0.94
    {'model_path': "mlx-community/pixtral-12b-4bit", 'model_name': "Pixtral-1", 'type': "mlx", 'max_tokens': 5000, 'temp': 0.4}, #0.94
    {'model_path': "mlx-community/pixtral-12b-4bit", 'model_name': "Pixtral-2", 'type': "mlx", 'max_tokens': 5000, 'temp': 0.4}, #0.94
#    {'model_path': "mlx-community/Qwen2-VL-7B-Instruct-8bit", 'model_name': "Qwen-0", 'type': "mlx", 'max_tokens': 5000, 'temp': 0.4}, #0.76
#    {'model_path': "llama3.2-vision", 'model_name': "llama-0", 'type': "ollama", 'max_tokens': 5000, 'temp': 0}, #0.80
#    {'model_path': "llava:13b", 'model_name': "llava", 'type': "ollama", 'max_tokens': 5000}, #0.12
#    {'model_path': "minicpm-v", 'model_name': "minicpm", 'type': "ollama", 'max_tokens': 5000}
]
#"""

# promptを設定
prompt = """
Please extract all 50 answers from the main section as they are.

The background is white, and the text is handwritten in black ink.
The main section of the document consists of a grid with 50 questions, numbered from (1) to (50).
Each question has a single-digit handwritten answer or a cross mark `X'.
Your task is to output all 50 answers accurately in plain text directly within this response, without referencing or creating any files.

First, output the points to be noted.
Then, output the string `**Final Answer**' followed by the answers to the questions.
Format each answer on a separate line in the following style without using TeX formatting:
=====
(Question number) Answer's digit
=====
Make sure the question number is enclosed in parentheses.
If the answer is a cross mark or blank, replace `Answer's digit' with `X'.

Example final output:
=====
**Final Answer**
(1) 0
(2) 1
(3) 2
(4) X
=====

Ensure the final output is in plain text format, without TeX formatting or file references.
"""

# 画像内容をテキストに出力
mylib.repeat_func_in_dir(dir_students, "_page1.jpg", lambda path: image_to_text.process_list(arg_list, prompt, path))

# txtファイルを集計し，多数決をとってdfを作成
#"""
problem_length = 50
columns = ["学生番号"] + [f"Q{i:02}" for i in range(1, problem_length+1)]
threshold = 2/3
df_list = []
for model_info in arg_list:
    model_name = model_info['model_name']
    df_list.append(txt_to_df.construct_df(dir_students, "_page1-" + model_name + ".txt", columns, problem_length))
df_consensus = txt_to_df.consensus_df(df_list, threshold=threshold).replace("NA", pd.NA)
print(df_consensus.head())
for df in df_list:
    print(txt_to_df.calculate_match_rate(df_consensus, df))
#"""

# dfからcsvファイルと，エラー処理用のtxtファイルを作成
df_consensus.to_csv(summary_csv, index=False, encoding='utf-8-sig')
df_to_csv.list_na_locations(df_consensus, NA_csv)
