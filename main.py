import os
import pandas as pd
import mylib
#import pdf_to_jpg
#import image_to_text
#import check
import reformulate

# 学生の解答用紙ファイルのディレクトリ設定
dir_students = './student_answers'
problem_length = 15

# pdfファイルをjpgに変換
for file_name in sorted(os.listdir(dir_students)):
    if file_name.endswith(".pdf"):
        pdf_path = os.path.join(dir_students, file_name)
        print(f"{pdf_path}を処理中")
        pdf_to_jpg.convert_pdf_to_jpg(pdf_path)


# 画像からテキストを抽出
# モデル名、プロンプトを設定
model_path = "mlx-community/Qwen2-VL-7B-Instruct-4bit"
prompt_list = []
prompt_list.append("Provide the student ID (starting with 158R).")
prompt_list.append("The student's grade is 1, 2, 3 or 4, the student's class is 16. Then, what is the student's number?")
prompt_list.append("The answers to problems (1) through (5) are written in uppercase letters of the alphabet. State what each of them is in the format `(problem-number) letter'.")
prompt_list.append("The answers to problems (6) through (10) are written in lowercase letters of the alphabet. State what each of them is in the format `(problem-number) letter'.")
prompt_list.append("The answers to problems (11) through (15) are written as single-digit numbers. State what each of them is in the format `(problem-number) digit'.")
#prompt_list.append("The answers for problems (16)-(20) are written as fractions. Provide each of them in the format `(problem-number) ?/?'.")

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
#prompt0 = """
#Read the following and output the student ID followed by answers (1) to (15) separated by commas in this order.
#(e.g., 158R228020, A, B, C, D, E, F, G, H, I, J, K, L, M, N, O)
#=====
#"""
prompt0 = """
Read the following input and extract the student ID
followed by the answers to questions (1) through (15).
Output the result in the specified format:
student ID, followed by the answers separated by commas.
For example: 158R228020, A, B, C, D, E, F, G, H, I, J, K, L, M, N, O.
"""
answer_file = "./correct_answer/answer.txt"


for file_name in sorted(os.listdir(dir_students)):
    if file_name.endswith("_page1.txt"):
        txt_path = os.path.join(dir_students, file_name)
        print(f"{txt_path}を処理中")
        content = mylib.read_text_file(txt_path)
        prompt = prompt0 + content
        student_answer = check.generate_with_prompt(model_path, prompt)
        student_answer_list = check.text_to_list(student_answer, problem_length+1)
        student_answer_list.insert(0, os.path.basename(txt_path)[:10])

        correct_answer = mylib.read_text_file(answer_file)
        correct_answer_list = check.text_to_list(correct_answer, problem_length+2)
        
        grade_list = check.compare_lists(correct_answer_list, student_answer_list)
        
        # テキストファイルに出力
        base, ext = os.path.splitext(txt_path)
        txt_path = base + "-grade.txt"
        mylib.write_to_csv(txt_path, [student_answer_list, grade_list], None)


# Excelファイルと同じ行になるように成績を整形
report_excel = "./correct_answer/report_summary.xlsx"
df_report = mylib.read_excel(report_excel, sheet_name=0, header=1, dtype=str)

# 学生の成績
df_student = reformulate.read_second_row_from_all_txt(dir_students)
df_student.columns = ["ファイル名", "学生番号"] + [f"Q{i}" for i in range(1, problem_length+1)]  # Q1～Q15
#print(df_student)

merged_df = pd.merge(df_report, df_student, on="学生番号", how="left")
print(merged_df.head())

# データフレームをCSVファイルとして保存
output_file = "./correct_answer/grade.csv"  # 保存するファイル名
merged_df.to_csv(output_file, index=False, encoding="utf-8-sig")



