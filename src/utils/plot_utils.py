import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def generate_line_chart(df):
    """ 產生訊息數量隨時間變化的折線圖 📈 """

    # 確保 dataframe 有資料
    if df.empty:
        return go.Figure()

    full_data = df.dropna(subset=["count"])
    min_date = full_data["date"].min()
    max_date = full_data["date"].max()

    # **建立折線圖**
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=full_data["datetime"],
            y=full_data["count"],
            mode="lines",
            line=dict(width=3, color="green"),  # 🔥 線條顏色 & 粗細
            hovertemplate="🕒 時間: %{x} <br>📊 訊息數: %{y:,}<extra></extra>",
        )
    )

    # **X 軸標籤格式**
    tick_format = "%Y-%m-%d %h:%M" if (max_date - min_date).days > 1 else "%h:%M"

    # **設定 X 軸**
    fig.update_xaxes(
        showgrid=True,
        tickformat=tick_format,
        tickangle=45,  # **避免過密時，標籤傾斜**
        tickmode="auto",
        tickfont=dict(size=18),  # 🔥 放大 X 軸標籤
    )

    # **設定 Y 軸**
    fig.update_yaxes(
        showgrid=True,
        tickfont=dict(size=18),  # 🔥 放大 Y 軸標籤
    )

    # **美化 Layout**
    fig.update_layout(
        margin=dict(l=40, r=20, t=40, b=40),
        hovermode="x unified",  # **Hover 顯示對應 X 軸資訊**
        dragmode=False,
        plot_bgcolor="rgba(255,255,255,1)",  # **白色背景**
    )

    return fig


def generate_top_users_chart(filtered_df):
    """
    產生訊息數最多的 Top 5 使用者條形圖

    :param filtered_df: 已篩選的 DataFrame，包含 id, author, message
    :return: None（直接使用 Streamlit 繪製圖表）
    """

    # 確保 DataFrame 不是空的
    if filtered_df.empty:
        st.warning("⚠️ 目前篩選條件下，沒有足夠的數據來顯示前 5 名。請嘗試調整篩選條件！")
        return

    # **計算前 5 名發送訊息最多的使用者**
    # **計算所有用戶的訊息數**
    top_users = (
        filtered_df.groupby(["id", "author"])
        .size()
        .reset_index(name="message_count")
        .sort_values(by="message_count", ascending=False)  # **🔥 訊息數最多的在最上方**
    )
    total_cnt = top_users.shape[0]

    # **取得前 5 名的最小訊息數**
    min_top5_count = top_users["message_count"].iloc[min(5, len(top_users)) - 1]  # **第 5 名的數量**

    # **篩選所有訊息數 ≥ 第 5 名的**
    top_users = top_users[top_users["message_count"] >= min_top5_count]

    top_users["message_count_str"] = top_users["message_count"].apply(lambda x: f"{x:,}")

    # **建立條形圖**
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=top_users["message_count"][::-1],
            y=top_users["author"][::-1],
            text=top_users["message_count_str"][::-1],
            textposition="inside",
            orientation="h",  # **橫向條形圖**
            marker=dict(color="green"),  # **🔥 所有條形圖使用相同顏色**
        )
    )

    # **調整 UI**
    fig.update_layout(
        xaxis_title="訊息數",
        yaxis_title="",
        height=400,
        margin=dict(l=40, r=40, t=50, b=40),
        hovermode=False,
        dragmode=False,  # 禁止拖動
        xaxis=dict(showgrid=True, title_font=dict(size=16), tickfont=dict(size=14)),  # 加大 X 軸字體
        yaxis=dict(showgrid=False, title_font=dict(size=16), tickfont=dict(size=16)),  # 加大 Y 軸字體
    )

    # **顯示圖表**
    st.subheader(f"🏆 訊息數量最多的 Top 5 使用者 (總共 {total_cnt:,} 位使用者)")
    st.plotly_chart(fig, use_container_width=True)