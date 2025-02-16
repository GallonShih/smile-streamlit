import streamlit as st

def paginate_data(filtered_df, rows_per_page=10):
    """ 根據目前的頁數顯示適當的資料 """
    total_rows = len(filtered_df)
    total_pages = max(1, (total_rows // rows_per_page) + (1 if total_rows % rows_per_page != 0 else 0))

    # 確保頁數有效
    if "current_page" not in st.session_state or st.session_state.current_page > total_pages:
        st.session_state.current_page = 1

    new_page = st.number_input(
        "選擇頁數",
        min_value=1,
        max_value=total_pages,
        value=st.session_state.current_page,
        step=1
    )

    # **修正：如果 `new_page` 不等於 `current_page`，立即更新並重新執行**
    if new_page != st.session_state.current_page:
        st.session_state.current_page = new_page
        st.rerun()  # **🔥 強制刷新 Streamlit，確保切換頁碼後馬上生效**

    start_idx = (st.session_state.current_page - 1) * rows_per_page
    end_idx = start_idx + rows_per_page

    return filtered_df.iloc[start_idx:end_idx], total_pages
