import pandas as pd
import datetime

def apply_filters(df, search_id, search_author, search_message, start_datetime, end_datetime):
    """ 根據使用者的條件過濾數據 """
    filtered_df = df.copy()

    # 過濾 ID
    if search_id:
        filtered_df = filtered_df[filtered_df["id"].astype(str) == str(search_id)]

    # 過濾作者
    if search_author:
        filtered_df = filtered_df[filtered_df["author"].str.contains(search_author, case=False, na=False)]

    # 過濾訊息
    if search_message:
        filtered_df = filtered_df[filtered_df["message"].str.contains(search_message, case=False, na=False)]

    # 過濾時間範圍
    filtered_df["datetime"] = pd.to_datetime(filtered_df["datetime"])
    filtered_df = filtered_df[(filtered_df["datetime"] >= start_datetime) & (filtered_df["datetime"] <= end_datetime)]

    return filtered_df.reset_index(drop=True)
