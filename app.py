import streamlit as st
import pandas as pd
import io

# 設定網頁寬度
st.set_page_config(page_title="進階數據分析助手", layout="wide")

st.title("🧮 互動式數據分析工具")
st.write("上傳檔案後，你可以自由選擇欄位進行加總、平均或排序。")

# --- 1. 檔案上傳 ---
uploaded_file = st.file_uploader("上傳 Excel 或 CSV 檔案", type=['xlsx', 'csv'])

if uploaded_file:
    # 讀取資料
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
    
    st.subheader("1. 原始資料預覽")
    # 讓表格可以排序與篩選
    st.dataframe(df, use_container_width=True)

    st.divider()

    # --- 2. 互動式排列設定 ---
    st.subheader("2. 自定義分析設定")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        group_cols = st.multiselect("選擇要『分類』的欄位 (例如：日期、品項)", options=df.columns.tolist())
    
    with col2:
        calc_cols = st.multiselect("選擇要『計算』的數值欄位 (例如：金額、數量)", options=df.columns.tolist())
        
    with col3:
        method = st.selectbox("選擇計算方式", ["加總 (Sum)", "平均 (Mean)", "計數 (Count)", "最大值 (Max)", "最小值 (Min)"])

    # --- 3. 執行運算 ---
    if group_cols and calc_cols:
        # 對應計算方法
        method_map = {
            "加總 (Sum)": "sum",
            "平均 (Mean)": "mean",
            "計數 (Count)": "count",
            "最大值 (Max)": "max",
            "最小值 (Min)": "min"
        }
        
        # 執行 GroupBy 運算
        result_df = df.groupby(group_cols)[calc_cols].agg(method_map[method]).reset_index()
        
        # 排序功能
        sort_col = st.selectbox("選擇排序欄位", options=result_df.columns.tolist())
        sort_order = st.radio("排序方向", ["升冪 (小到大)", "降冪 (大到小)"], horizontal=True)
        
        result_df = result_df.sort_values(by=sort_col, ascending=(sort_order == "升冪 (小到大)"))

        # --- 4. 顯示結果與下載 ---
        st.success(f"✅ 已完成分析：按 {', '.join(group_cols)} 進行 {method}")
        st.dataframe(result_df, use_container_width=True)

        # 下載按鈕
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            result_df.to_excel(writer, index=False)
        
        st.download_button(
            label="📥 下載此分析結果",
            data=output.getvalue(),
            file_name="分析報表.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("💡 請在上方選擇至少一個『分類欄位』與一個『計算欄位』開始分析。")
