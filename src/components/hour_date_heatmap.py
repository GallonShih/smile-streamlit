import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from typing import List


class HourDateHeatmap:
    """
    使用 Plotly 繪製 日期 vs 小時 Heatmap（X 軸是小時，Y 軸是日期，最早的日期在最上方）
    """

    def __init__(self, colorscale="Greens", cell_size=20, missing_color="rgba(220, 220, 220, 0.5)"):
        """
        初始化 Heatmap
        :param colorscale: 顏色主題 (預設 "Greens")
        :param cell_size: 每個方格的大小（控制間距）
        :param missing_color: 缺少數值時的顏色（預設為灰色）
        """
        self.colorscale = colorscale
        self.cell_size = cell_size  # 控制間距
        self.missing_color = missing_color  # 無數據的顏色

    def create_grid(self, dates: List[datetime.date], hours: List[int], counts: List[int]):
        """
        生成 日期 x 24 小時的數據矩陣（日期排序：最早的在最上方）
        """
        unique_dates = sorted(set(dates), reverse=True)  # 🔥 修正日期排序，最早的在最上方
        date_labels = [date.strftime("%Y-%m-%d") for date in unique_dates]

        grid_data = pd.DataFrame({"date": dates, "hour": hours, "count": counts})
        pivot_table = grid_data.pivot(index="date", columns="hour", values="count")
        pivot_table = pivot_table.reindex(unique_dates)

        return pivot_table, date_labels

    def plot(self, dates: List[datetime.date], hours: List[int], counts: List[int]):
        """
        使用 Plotly 繪製 Heatmap
        """
        pivot_table, date_labels = self.create_grid(dates, hours, counts)

        # 設定格子的位置
        x_vals = list(pivot_table.columns)  # 小時
        y_vals = date_labels  # 日期，已經反轉排序
        z_vals = pivot_table.values  # 數據

        # **設定 customdata，包含 count**
        custom_data = np.where(pd.isna(z_vals), "", z_vals)

        num_dates = len(y_vals)
        base_size =  num_dates * 45

        # 準備顏色映射，無數據的部分設為灰色
        colorscale = [
            [0, self.missing_color],  # 無數據 → 灰色
            [0.01, self.missing_color],  # 保持灰色
            [0.02, "rgb(237, 248, 233)"],  # 最低數據開始變色
            [1, "rgb(0, 100, 0)"],  # 高密度 → 深綠色
        ]

        # 🔥 修正 hovertemplate
        hovertemplate = (
            "📅 日期: %{y}<br>"
            "⏰ 時間: %{x}:00 - %{x}:59<br>"
            "📊 訊息數: %{customdata:,}<extra></extra>"  # `:,` 讓數字用千分位格式，不會變成 `k`
        )

        # 建立 Heatmap
        fig = go.Figure(data=go.Heatmap(
            z=z_vals,
            x=x_vals,
            y=y_vals,
            colorscale=colorscale,
            hoverinfo="x+y+z",
            hovertemplate=hovertemplate,  # ✅ 確保 hover 顯示正確
            customdata=custom_data,
            xgap=self.cell_size * 0.25,  # 控制間距
            ygap=self.cell_size * 0.25,  # 控制間距
            showscale=False,  # 隱藏顏色標尺
        ))

        # X 軸（小時）
        fig.update_xaxes(
            tickmode="array",
            tickvals=[h - 0.5 for h in range(24)],  # 中心位置在格子之間
            ticktext=[f"{h}:00" if h % 3 == 0 else "" for h in range(24)],  # 每 3 小時標一次
            tickfont=dict(size=18),  # 🔥 放大 X 軸標籤
            showgrid=False,
        )

        # Y 軸（日期）
        fig.update_yaxes(
            categoryorder="array",
            categoryarray=y_vals,  # 使用我們的排序
            autorange="reversed",  # ✅ 手動反轉 Y 軸，確保最早的日期顯示在最上方
            tickfont=dict(size=18),  # 🔥 放大 Y 軸標籤
            showgrid=False,
        )

        # 移除其他互動功能（僅保留游標資訊）
        # ✅ **確保方格為正方形**
        fig.update_layout(
            margin=dict(l=50, r=20, t=20, b=40),
            hovermode="closest",
            dragmode=False,  # 禁止拖動
            xaxis=dict(fixedrange=True, scaleanchor="y"),  # **🔥 讓 X 軸和 Y 軸保持比例**
            yaxis=dict(fixedrange=True, scaleanchor="x"),  # **🔥 讓 Y 軸和 X 軸保持比例**
            height=base_size,  # 🔥 **動態調整高度，確保格子大小**
            width=base_size,   # 🔥 **動態調整寬度，確保格子大小**
        )

        return fig
