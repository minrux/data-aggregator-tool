import streamlit as st
import pandas as pd
import io

# 網頁標題與正向鼓勵
st.set_page_config(page_title="數據累計助手", page_icon="📊")
st.title("🚀 自動檔案累計整理助手")
st.write("把你的檔案丟進來，剩下的交給 AI 處理，你去喝杯咖啡吧！☕️")

# 設定欄位名稱
with st.sidebar:
    st.header("⚙️ 設定參數")
    date_col = st.text_input("日期欄位名稱", "日期")
    value_col = st.text_input("累計數值欄位名稱", "金額")

# 上傳檔案區（支援多檔案）
uploaded_files = st.file_uploader("請上傳所有要整理的 Excel 或 CSV", type=['xlsx', 'csv'], accept_multiple_files=True)

if uploaded_files:
    all_data = []
    for file in uploaded_files:
        df = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)
        if date_col in df.columns and value_col in df.columns:
            all_data.append(df[[date_col, value_col]])
    
    if all_data:
        # 合併與計算
        combined_df = pd.concat(all_data, ignore_index=True)
        summary = combined_df.groupby(date_col)[value_col].sum().reset_index()
        
        # 顯示結果預覽
        st.subheader("📊 整理結果預覽")
        st.dataframe(summary)

        # 轉成 Excel 下載連結
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            summary.to_excel(writer, index=False)
        
        st.download_button(
            label="📥 下載累計報表 (Excel)",
            data=output.getvalue(),
            file_name="整理完成_累計報表.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error(f"找不到指定的欄位：'{date_col}' 或 '{value_col}'，請檢查設定！")