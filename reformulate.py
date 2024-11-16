import pandas as pd

report_excel = "./correct_answer/report_summary.xlsx"

# レポートまとめファイルから2番目のシート（インデックス1）を読み込む
try:
    df_report = pd.read_excel(report_excel, sheet_name=1, header=1)
except Exception as e:
    print(f"エラーが発生しました: {e}")
    exit()

# print(df_report.columns)

