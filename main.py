import pdf_to_jpg
import os

# 設定
dir_students = './student_answers'

# pdfファイルをjpgに変換
for file_name in os.listdir(dir_students):
    if file_name.endswith(".pdf"):
        pdf_path = os.path.join(dir_students, file_name)
        pdf_to_jpg.convert_pdf_to_jpg(pdf_path)

