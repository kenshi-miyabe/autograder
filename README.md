
# autograder

自動採点スクリプト

# 使い方

## 準備するもの

以下の3つを準備する．

- Mac
    - AppleSilicon搭載で，メモリは64GB以上
    - MLXなど必要なライブラリをインストール
    - brewで入れたOpenBLASがpkconfigから見つからない場合以下でパスを設定する
```bash
export PKG_CONFIG_PATH="$(brew --prefix openblas)/lib/pkgconfig:$PKG_CONFIG_PATH"
```
- 解答用紙
    - pdf形式
    - ファイル名の最初の10文字は学生番号
    - (1)から(50)までの問題の解答が書かれている
    - 解答は0から9までの1桁の数字もしくは空欄を意味する「X」
    - './student_answers'ディレクトリに配置する
- 名簿
    - xlsx形式
    - 「学生番号」の列がある
    - 「フィードバックファイル名」の列に解答用紙のファイル名が入っている
    - './correct_answer/report_summary.xlsx'に配置する

## 実行1: main1_read.py

- pdfからcsvファイル2つを作成する
- csvはcorrect_answerディレクトリに保存される
- summary.csvは結果，NA.csvはエラー処理用
- VLMモデルを何回か実行し，しきい値(デフォルト5/7)以上であれば採用し，そうでなければエラーとする
- モデルのデフォルトは，QVQ, Qwen2-VL-72B(3回), Pixtral-12B(3回)の合計7回

## エラー処理

- NA.csvと解答用紙のpdfファイルを見ながら，手動で解答をNA.csvに入力する

## 実行2: main2_csv.py

- summary.csvとNA.csvからgrade.csvを作成する
- csvは学生番号順に並んでいるが，grade.csvは出席番号順に並ぶ（report_summary.xlsxの順）

## 実行3: main2_rename.py

- 途中経過のファイルの削除
- grade.csvから各個人の結果のファイルを作成する
- ファイル名はもとのファイル名の拡張子をpdfからtxtに変更したもの

# 参考

- 解答用紙の形式はとても重要．問題番号の文字，横にも縦にも一定程度の間隔を空けること．
- 空欄はハルシネーションを起こす可能性が高い．何らかの文字が書いてあったほうが良い．今回は「X」を使用した．
- 文字が薄いと認識されない．コントラストを上げる処理を入れてある．
- VLMのモデルはQVQは99%くらいの精度があるが，処理時間が1ファイル10分くらいかかる．Qwen2-VL-72B, Pixtral-12Bは95%くらいの精度だが2分くらい．
- 普段の開発環境はAppleSilicon搭載のMacでメモリ16GBでも，小さいサイズのモデルを動かすことで可能である．エラーが多いので実運用は難しいだろうが，コードを書くために試しに動かすのには却って良い．小さいサイズだと処理が速いのでその点も良い．
- しきい値を高くすると誤認識が減るがエラー処理が増える．現在の組み合わせであれば，数人あたり1個のエラー処理で済む．
- プロンプトも大事．現在のプロンプトは以下．
    - 英語で書くこと．
    - 最初に何をするかを書く．
    - 次に何がどのように書かれているかの情報を入れる．
    - 出力の形式を指定する．最終出力の前に注意点を自分で書かせるのも有効．
    - 出力の例を書く．
    - エラーが起こりやすい点については最後にもう一度注意する．
```
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
```
