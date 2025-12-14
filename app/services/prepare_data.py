import pandas as pd


def download_google_sheet(sheet_id: str) -> pd.DataFrame:
    """
    Download Google Sheet as CSV and return as a DataFrame.
    """
    url = (f"https://docs.google.com/spreadsheets/d/"
           f"{sheet_id}/export?format=csv")
    df = pd.read_csv(url)
    return df


def map_columns(df: pd.DataFrame, column_map: dict) -> pd.DataFrame:
    """
    Rename columns according to column_map.
    """
    return df.rename(columns=column_map)


def explode_values(
        df: pd.DataFrame,
        value_prefix: str = "value"
) -> pd.DataFrame:
    """
    Transform rows according to the task rules:
    - For each value column, repeat rows max(value) times
    - Set value columns to 1 or 0 depending on iteration
    """
    value_columns = [col for col in df.columns if col.startswith(value_prefix)]
    new_rows_list = []

    for row in df.itertuples(index=False):
        max_count = max(getattr(row, col) for col in value_columns)
        for i in range(1, max_count + 1):
            row_values = {
                f"{col}": 1 if getattr(row, col) >= i else 0
                for col in value_columns
            }
            new_row = {
                col: getattr(row, col)
                for col in df.columns
                if col not in value_columns
            }
            new_row.update(row_values)

            new_row["long"] = float(
                str(new_row["long"]).replace(",", ".")
            )
            new_row["lat"] = float(
                str(new_row["lat"]).replace(",", ".")
            )
            new_rows_list.append(new_row)

    new_df = pd.DataFrame(new_rows_list, columns=df.columns)
    return new_df


def save_to_csv(df: pd.DataFrame, path: str):
    """
    Save DataFrame to CSV.
    """
    df.to_csv(path, index=False)


def prepare_data(sheet_id: str, output_path: str = "prepared_data.csv"):
    df = download_google_sheet(sheet_id)

    column_map = {
        "Дата": "date_1",
        "Область": "Область",
        "Місто": "city",
        "Значення 1": "value_1",
        "Значення 2": "value_2",
        "Значення 3": "value_3",
        "Значення 4": "value_4",
        "Значення 5": "value_5",
        "Значення 6": "value_6",
        "Значення 7": "value_7",
        "Значення 8": "value_8",
        "Значення 9": "value_9",
        "Значення 10": "value_10",
        "long": "long",
        "lat": "lat",
    }

    df = map_columns(df, column_map)
    exploded_df = explode_values(df)
    save_to_csv(exploded_df, output_path)
