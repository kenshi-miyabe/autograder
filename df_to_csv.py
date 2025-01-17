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
        lst = [col_name-2, col_name-1, col_name, col_name+1, col_name+2]
        if col_name <= 2:
            lst = [1, 2, 3, 4, 5]
        elif col_name >= 49:
            lst = [46, 47, 48, 49, 50]
        na_locations.append([df.iloc[row_idx,0],
                                df.columns[col_name], df.iloc[row_idx,col_name],
                                df.columns[lst[0]], df.iloc[row_idx,lst[0]],
                                df.columns[lst[1]], df.iloc[row_idx,lst[1]],
                                df.columns[lst[2]], df.iloc[row_idx,lst[2]],
                                df.columns[lst[3]], df.iloc[row_idx,lst[3]],
                                df.columns[lst[4]], df.iloc[row_idx,lst[4]]])

    mylib.write_to_csv(file_path, na_locations, ["学生番号", "Question", "Value", "Q-2", "V-2", "Q-1", "V-1", "Q", "V", "Q+1", "V+1", "Q+2", "V+2"])

    return