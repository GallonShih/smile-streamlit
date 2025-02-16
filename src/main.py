import streamlit as st
import numpy as np
import pandas as pd
from components.hour_date_heatmap import HourDateHeatmap
from utils.data_loader import load_data, load_emote
from utils.filter_utils import apply_filters
from utils.pagination_utils import paginate_data
from utils.plot_utils import generate_line_chart, generate_top_users_chart
import datetime

# 設定 Streamlit 頁面
st.set_page_config(page_title="後宮甄嬛傳：直撥留言", layout="wide")

# 載入資料
if "df" not in st.session_state:
    st.session_state.df = load_data()

df = st.session_state.df  # 取得資料

if "df_emote" not in st.session_state:
    st.session_state.df_emote = load_emote()

df_emote = st.session_state.df_emote  # 取得資料

# Heatmap 標題
st.title("🌨️ 那年杏花微雨，你說你是果郡王 ☔")

if df is not None:

    # **📌 Tabs 設計**
    tab1, tab2 = st.tabs(["📊 分析圖表", "🎨 YouTube Emoji 對照表"])

    # ✅ **📊 第一個分頁**
    with tab1:
        # 初始化小時
        all_hours = list(range(24))

        # Session State 初始化
        if "filtered_df" not in st.session_state:
            st.session_state.filtered_df = df[["id", "author", "datetime", "message", "message_html", "hour", "date"]].copy()

        if "current_page" not in st.session_state:
            st.session_state.current_page = 1

        if "filtered_dates" not in st.session_state:
            st.session_state.filtered_dates = sorted(df["date"].unique())

        # 🔹 **定義函數: 更新篩選狀態**
        def update_filter():
            st.session_state["apply_filter"] = True
            st.session_state["current_page"] = 1  # 篩選後回到第一頁

        # 🔹 **篩選功能（即時更新）**
        with st.expander("🔍 篩選條件", expanded=True):
            col0, col1, col2 = st.columns(3)

            with col0:
                search_id = st.text_input("ID", placeholder="輸入作者ID", on_change=update_filter)
            with col1:
                search_author = st.text_input("作者", placeholder="輸入作者名稱", on_change=update_filter)
            with col2:
                search_message = st.text_input("訊息", placeholder="輸入訊息內容", on_change=update_filter)

            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("開始日期", value=df["date"].min(), key="start_date", on_change=update_filter)
                start_time = st.time_input("開始時間", value=datetime.time(0, 0), key="start_time", on_change=update_filter)
            with col2:
                end_date = st.date_input("結束日期", value=df["date"].max(), key="end_date", on_change=update_filter)
                end_time = st.time_input("結束時間", value=datetime.time(23, 59), key="end_time", on_change=update_filter)

            start_datetime = datetime.datetime.combine(start_date, start_time)
            end_datetime = datetime.datetime.combine(end_date, end_time)

            # 篩選按鈕
            if st.button("篩選"):
                st.session_state.filtered_df = apply_filters(df, search_id, search_author, search_message, start_datetime, end_datetime)
                st.session_state.current_page = 1  # 篩選後回到第一頁

        # 🔹 **即時更新 `filtered_df`**
        if st.session_state.get("apply_filter", False):
            filtered_df = apply_filters(df, search_id, search_author, search_message, start_datetime, end_datetime)
            if not filtered_df.empty:
                st.session_state["filtered_dates"] = sorted(filtered_df["date"].unique())
            else:
                st.session_state["filtered_dates"] = sorted(df["date"].unique())

            st.session_state.filtered_df = filtered_df
            st.session_state.apply_filter = False

        filtered_df = st.session_state.filtered_df
        filtered_dates = st.session_state["filtered_dates"]

        # 計算 Heatmap 數據
        heatmap_data = filtered_df.groupby(["date", "hour"]).size().reset_index(name="count")
        # **確保 Heatmap 顯示完整時間範圍**
        date_range = pd.date_range(start=start_date, end=end_date).date  # 🔥 生成開始到結束日期的完整範圍
        full_grid = pd.DataFrame([(date, hour) for date in date_range for hour in all_hours], columns=["date", "hour"])  # 24 小時完整顯示
        full_grid = full_grid.merge(heatmap_data, on=["date", "hour"], how="left").fillna(0)  # 填補沒有資料的時間段
        # **轉換成 datetime 進行篩選**
        full_grid["datetime"] = pd.to_datetime(full_grid["date"].astype(str) + " " + full_grid["hour"].astype(str) + ":00")

        # **過濾範圍外的數據，將數值改為 None**
        full_grid["count"] = full_grid.apply(
            lambda row: row["count"] if start_datetime <= row["datetime"] <= end_datetime else np.nan,
            axis=1
        )

        # 繪製 Heatmap
        heatmap = HourDateHeatmap(colorscale="Greens")
        st.subheader("📊 日期 vs 小時 Heatmap")
        st.plotly_chart(heatmap.plot(full_grid["date"].tolist(), full_grid["hour"].tolist(), full_grid["count"].tolist()), use_container_width=True)

        # **📈 新增折線圖**
        st.subheader("📈 訊息數量變化趨勢")
        line_chart = generate_line_chart(full_grid)
        st.plotly_chart(line_chart, use_container_width=True)

        # 訊息資料標題
        st.subheader("📋 訊息資料")

        # 顯示篩選後的結果筆數
        st.write(f"篩選後共有 {len(filtered_df):,} 筆資料")

        # **分頁顯示**
        paginated_df, total_pages = paginate_data(filtered_df)

        # st.data_editor(
        #     paginated_df[["id", "author", "datetime", "message"]].astype({"datetime": "str"}),  
        #     use_container_width=True,
        #     disabled=True,
        #     column_config={
        #         "id": st.column_config.TextColumn(width="small"),
        #         "author": st.column_config.TextColumn(width="small"),
        #         "datetime": st.column_config.TextColumn(width="small"),
        #         "message": st.column_config.TextColumn(width="large", help="訊息內容"),
        #     },
        # )
        st.markdown(
            paginated_df[["id", "author", "datetime", "message_html"]].to_html(escape=False, index=False),  # ✅ **確保 HTML 不轉義，顯示圖片**
            unsafe_allow_html=True
        )

        # **分頁顯示**
        st.write(f"第 {st.session_state.current_page:,} 頁，共 {total_pages:,} 頁")

        generate_top_users_chart(filtered_df)
    
    # ✅ **📜 第二個分頁**
    with tab2:
        # **轉換圖片連結為 HTML**
        df_emote["emoji_image"] = df_emote["link"].apply(lambda x: f'<img src="{x}" width="32">')

        # **顯示表格**
        st.markdown(
            df_emote[["emoji", "emoji_image", "count"]]
            .assign(count=df_emote["count"].apply(lambda x: f"{x:,}"))
            .to_html(escape=False, index=False),
            unsafe_allow_html=True
        )
else:
    st.error("❌ 找不到 `data/messages.csv`，請確認檔案是否存在！")
