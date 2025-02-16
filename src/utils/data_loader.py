import pandas as pd
import os
import re

DATA_PATH = os.path.join(os.path.dirname(__file__), "../../data/messages.csv")
EMOTE_PATH = os.path.join(os.path.dirname(__file__), "../../data/emotes.csv")

def load_emote(filepath=EMOTE_PATH):
    """
    讀取 emoji 對照表
    """
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        return df
    else:
        return {}

def replace_emojis_with_html(message, emote_dict):
    """
    將訊息中的 emoji 轉換為 HTML <img> 格式，確保所有 emoji 都被替換
    """
    if not isinstance(message, str):
        return message  # 非字串內容直接返回

    # **透過 re.finditer() 找到所有符合的 emoji**
    for match in re.finditer(r":[^:]+:", message):
        emoji_code = match.group(0)  # 抓取 emoji 代碼，例如 `:face-fuchsia-tongue-out:`
        if emoji_code in emote_dict:
            img_tag = f'<img src="{emote_dict[emoji_code]}" width="24" style="vertical-align: middle;">'
            message = message.replace(emoji_code, img_tag)  # **確保替換所有相同 emoji**

    return message  # 回傳已轉換的訊息

def load_data(filepath=DATA_PATH):
    """
    讀取 CSV 並處理時間數據，並新增 `message_html` 欄位
    """
    if os.path.exists(filepath):
        df = pd.read_csv(filepath, parse_dates=["datetime"])
        df.dropna(subset=["datetime"], inplace=True)  # 過濾掉 datetime 欄位的 NaN
        df["date"] = df["datetime"].dt.date  # 提取日期
        df["hour"] = df["datetime"].dt.hour  # 提取小時

        # **載入 Emoji 對照表**
        df_emote = load_emote()
        emote_dict = dict(zip(df_emote["emoji"], df_emote["link"]))

        # **新增 `message_html` 欄位**
        df["message_html"] = df["message"].apply(lambda msg: replace_emojis_with_html(msg, emote_dict))

        return df
    else:
        return None
