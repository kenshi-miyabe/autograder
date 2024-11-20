import pandas as pd

# CSVファイルを読み込む

grade_file = "./correct_answer/grade.csv"
df = pd.read_csv(grade_file)

# Q1からQ10の文字列を"-"で結合して新しいコラムに格納
df['結合文字列'] = df[['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10']].astype(str).agg('-'.join, axis=1)

# 結果を確認（必要に応じて）
print(df.head())

# 必要なら新しいCSVに保存
df.to_csv(grade_file, index=False)
