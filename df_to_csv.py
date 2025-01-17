import pandas as pd
import mylib

def list_na_locations(df, file_path):
    """
    List all NA locations in the DataFrame in the format a, b, "NA".

    Parameters:
        df (pd.DataFrame): Input DataFrame to search for NA values.

    Returns:
        list: A list of strings in the format "a, b, \"NA\"" where a is the row index,
              b is the column name, and \"NA\" indicates a missing value.
    """
    na_locations = []

    # Iterate over each cell in the DataFrame
    for row_idx, col_name in zip(*df.isna().to_numpy().nonzero()):
        row_label = df.index[row_idx]
        col_label = df.columns[col_name]
        na_locations.append([df.iloc[row_idx,0], col_label, "NA"])

    mylib.write_to_csv(file_path, na_locations, ["学生番号", "Question", "Value"])

    return