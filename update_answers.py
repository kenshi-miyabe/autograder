import pandas as pd

# CSVファイルを読み込む

grade_file = "./correct_answer/grade.csv"
df = pd.read_csv(grade_file)

# Q1からQ10の文字列を"-"で結合して新しいコラムに格納
non_empty_rows = (df['結合文字列'].notna())

df.loc[non_empty_rows,'結合文字列'] = df.loc[non_empty_rows,['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10']].astype(int).astype(str).agg('-'.join, axis=1)

# 結果を確認（必要に応じて）
print(df['結合文字列'])
print(df.head())

# 必要なら新しいCSVに保存
df.to_csv(grade_file, index=False, encoding='utf-8-sig')
