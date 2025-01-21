import os
import io
import fitz  # PyMuPDF
from PIL import Image, ImageEnhance # Pillow
import mylib

def convert_pdf_to_jpg(file_name, contrast_ratio=3.0):
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

        # 一時的な画像ファイルに保存
        temp_file = f"temp_page{page_number + 1}.png"
        pix.save(temp_file)

        # PILで画像を開き、コントラストを調整
        with Image.open(temp_file) as img:
            enhancer = ImageEnhance.Contrast(img)
            enhanced_img = enhancer.enhance(contrast_ratio)  # コントラスト倍率（例: 2.0で2倍）
            
            # JPGとして保存
            output_file = f"{os.path.splitext(file_name)[0]}_page{page_number + 1}.jpg"
            enhanced_img.save(output_file, format='JPEG')
            output_files.append(output_file)
        
        # 一時ファイルを削除
        os.remove(temp_file)

    pdf_document.close()

    print("以下のJPGファイルが作成されました：")
    for output_file in output_files:
        print(output_file)

import os
from PIL import Image, ImageEnhance
import fitz  # PyMuPDFを使用

def convert_pdf_to_png(file_name, img_size =(1448, 2048), dpi=72, contrast_ratio=3.0):
    # ファイル拡張子を確認
    if not file_name.endswith('.pdf'):
        print("エラー: PDFファイルを指定してください．")
        return

    # PDFを開く
    pdf_document = fitz.open(file_name)
    output_files = []

    # 各ページを画像に変換
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        
        # 画像サイズを指定してピクセルデータを取得
        zoom = dpi / 72
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        # PIL用のバイトデータに変換
        img_data = pix.tobytes("png")
        with Image.open(io.BytesIO(img_data)) as img:
            img = img.resize(img_size)

            # コントラストを調整
            enhancer = ImageEnhance.Contrast(img)
            enhanced_img = enhancer.enhance(contrast_ratio)
            
            # PNGとして保存
            output_file = f"{os.path.splitext(file_name)[0]}_page{page_number + 1}.png"
            enhanced_img.save(output_file, format='PNG')
            output_files.append(output_file)

    pdf_document.close()

    print("以下のPNGファイルが作成されました：")
    for output_file in output_files:
        print(output_file)



if __name__ == "__main__":
    #input_file = input("PDFファイル名を入力してください：")
    input_file = "./student_answers/158R248028-MINUTE-2412031628.pdf"
    convert_pdf_to_jpg(input_file)
