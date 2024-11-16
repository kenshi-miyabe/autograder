import fitz  # PyMuPDF
from PIL import Image # Pillow
import os
import mylib

def convert_pdf_to_jpg(file_name):
    # ファイル拡張子を確認
    if not file_name.endswith('.pdf'):
        mylib.log_error("エラー: PDFファイルを指定してください．")
        return

    # PDFを開く
    pdf_document = fitz.open(file_name)
    output_files = []

    # 各ページを画像に変換
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap()  # ピクセルデータを取得

        # 画像を保存
        output_file = f"{os.path.splitext(file_name)[0]}_page{page_number + 1}.jpg"
        pix.save(output_file)
        output_files.append(output_file)

    pdf_document.close()

    print("以下のJPGファイルが作成されました：")
    for output_file in output_files:
        print(output_file)

if __name__ == "__main__":
    input_file = input("PDFファイル名を入力してください：")
    pdf_to_jpg(input_file)
