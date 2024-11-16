import os
import pandas as pd
import mylib
import pdf_to_jpg
import image_to_text
import check
import reformulate

# 設定
dir_students = './student_answers'

# pdfファイルをjpgに変換
for file_name in sorted(os.listdir(dir_students)):
    if file_name.endswith(".pdf"):
        pdf_path = os.path.join(dir_students, file_name)
        print(f"{pdf_path}を処理中")
        pdf_to_jpg.convert_pdf_to_jpg(pdf_path)

# 画像からテキストを抽出
# モデル名、画像パス、プロンプトを設定
model_path = "mlx-community/Qwen2-VL-7B-Instruct-4bit"
prompt_list = []
number_list = []
#prompt = "「?年?組?番号」の?の部分を読み取り，以下の形式で出力せよ．\n"
#prompt = prompt + "年の前の数字, 組の前の数字, 番号の前の数字"
#prompt = prompt + "(例)\n 1, 1, 001"
#prompt_list.append(prompt)
#number_list.append(3)
#prompt = "学生番号(Student's ID)を読み取り以下の形式で出力せよ．\n"
#prompt = prompt + "?は1文字の数字で，???R??????"
#prompt = prompt + "(例)\n 111R111111"
#prompt_list.append(prompt)
#number_list.append(1)
prompt = "(1)から(5)の解答を読み取り答えのみ以下の形式で出力せよ．\n"
prompt = prompt + "(1)の答, (2)の答,..., (5)の答"
prompt = prompt + "（例)\n a, a, a, a, a"
prompt_list.append(prompt)
number_list.append(5)
prompt = "(6)から(10)の解答を読み取り答えのみ以下の形式で出力せよ．\n"
prompt = prompt + "(6)の答, (7)の答,..., (10)の答"
prompt = prompt + "（例)\n a, a, a, a, a"
prompt_list.append(prompt)
number_list.append(5)

for file_name in sorted(os.listdir(dir_students)):
    if file_name.endswith("_page1.jpg"):
        image_path = os.path.join(dir_students, file_name)
        base, ext = os.path.splitext(file_name)
        file_name_txt = base + ".txt"

        print(f"{image_path}を処理中")
        output_list = image_to_text.process_images_with_prompt(model_path, [image_path], prompt_list)
        
        # 出力リストを整形
        output_list_long = []
        for output_item, number_item in zip(output_list, number_list):
            items = output_item.split(",")
            while len(items) < number_item:
                items.append("")
            output_list_long = output_list_long + items[:number_item]
        output_list_long = [file_name[:10], file_name_txt] + [item.strip() for item in output_list_long]
        print(output_list_long)

        # テキストファイルに出力
        base, ext = os.path.splitext(image_path)
        txt_path = base + ".txt"
        mylib.write_to_csv(txt_path, output_list_long, mode='w')

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
df_student.columns = ["学生番号", "ファイル名"] + [f"Q{i}" for i in range(1, 11)]  # Q1～Q10
print(df_student)

merged_df = pd.merge(df_report, df_student, on="学生番号", how="left")
print(merged_df.head())

# データフレームをCSVファイルとして保存
output_file = "./correct_answer/grade.csv"  # 保存するファイル名
merged_df.to_csv(output_file, index=False, encoding="utf-8-sig")



