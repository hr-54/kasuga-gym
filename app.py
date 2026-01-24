import streamlit as st
import pandas as pd
import os
import re

# 画面幅を広く使う設定
st.set_page_config(page_title="春日体育館 予約検索", page_icon="📅", layout="wide")

st.title("春日体育館 予約管理")

# file_schedule = "schedule_2026-01.csv"
# file_calendar="calendar_2026-01.png"
# file_gantt = "gantt_2026-01.png"
# file_monthly_summary = "monthly_summary_2026-01.png"
# file_group_schedule ="group_schedule_2026-01.png"
file_schedule = "schedule_2026-02.csv"
file_calendar="calendar_2026-02.png"
file_gantt = "gantt_2026-02.png"
file_monthly_summary = "monthly_summary_2026-02.png"
file_group_schedule ="group_schedule_2026-02.png"

# タブの作成：tab1で検索、tab2で全体図
tab1, tab2, tab3, tab4 = st.tabs(["🔍 予約を検索・確認", "カレンダー","利用時間全体像","団体別利用時間"])

# --- Tab 1: スケジュール検索 ---
with tab1:
    if os.path.exists(file_schedule):
        try:
            df = pd.read_csv(file_schedule, encoding="utf-8")
        except:
            df = pd.read_csv(file_schedule, encoding="cp932")

        # 検索窓とジャンプ機能を横に並べる
        c1, c2 = st.columns([3, 1])
        with c1:
            search = st.text_input("🔍 サークル名や日付で検索", placeholder="例: ULIS / 01-10")
        with c2:
            target_date = st.selectbox("📅 日付へジャンプ", ["全表示"] + df['Date'].tolist())

        # フィルタリング
        display_df = df.copy()
        if target_date != "全表示":
            display_df = display_df[display_df['Date'] == target_date]
        elif search:
            display_df = display_df[display_df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]

        st.markdown("---")

        # 2列レイアウトでカード形式表示
        col1, col2 = st.columns(2)
        for i, (_, row) in enumerate(display_df.iterrows()):
            target_col = col1 if i % 2 == 0 else col2
            with target_col:
                date_str = str(row['Date'])
                blocks_str = str(row['Blocks'])
                lines = blocks_str.split('\n')
                
                filtered_lines = []
                for line in lines:
                    if not search or search.lower() in line.lower() or search.lower() in date_str.lower():
                        # 「団体名 時間」を「時間 : 団体名」に変換
                        time_match = re.search(r'(\d{1,2}:\d{2}-\d{1,2}:\d{2})', line)
                        if time_match:
                            time_part = time_match.group(1)
                            team_part = line.replace(time_part, "").strip()
                            filtered_lines.append(f"<p style='margin: 1px 0; font-size: 14px;'><b>{time_part}</b> : {team_part}</p>")
                        else:
                            filtered_lines.append(f"<p style='margin: 1px 0; font-size: 14px;'>{line}</p>")

                if filtered_lines:
                    st.markdown(f"""
                    <div style="background-color: #f8f9fa; padding: 10px; border-radius: 8px; margin-bottom: 12px; border-left: 5px solid #007bff; box-shadow: 1px 1px 3px rgba(0,0,0,0.1);">
                        <h3 style="margin: 0 0 5px 0; font-size: 16px; color: #333;">📅 {date_str}</h3>
                        {"".join(filtered_lines)}
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.warning("データが見つかりません。")

# --- Tab 2: 全体把握図 ---
with tab2:
    #st.header("🗓 1月分 全体スケジュールカレンダー")
    st.header("2月分 全体スケジュールカレンダー")
    if os.path.exists(file_calendar):
        # 大きく表示
        st.image(file_calendar, use_container_width=True, caption="カレンダー")
    else:
        st.info("カレンダー画像 (calendar_2026-02.png) が見つかりません。")

# --- Tab 3: 全体把握図 ---
with tab3:
    st.header("ガントチャート")
    if os.path.exists(file_gantt):
        # 大きく表示
        st.image(file_gantt, use_container_width=True, caption="ガントチャート（全体図）")
    else:
        st.info("画像 (gantt_2026-02.png) が見つかりません。")

    st.header("公平性")
    if os.path.exists(file_monthly_summary):
        # 大きく表示
        st.image(file_monthly_summary, use_container_width=True)
    else:
        st.info("画像 (monthly_summary_2026-02.png) が見つかりません。")

#Tab 4: 団体別
with tab4:
    st.header("団体別利用時間")
    if os.path.exists(file_group_schedule):
        # 大きく表示
        st.image(file_group_schedule, use_container_width=True)
    else:
        st.info("画像 (group_schedule_2026-02.png) が見つかりません。")
