import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="학원 업종 분석", layout="wide")

st.title("📊 지역별 학원 업종 분포 분석 대시보드")
st.write("CSV 파일을 업로드하면 자동으로 시각화됩니다. (UTF-8, CP949 등 자동 인식)")

# -------------------------------
# 📂 CSV 업로드
# -------------------------------
uploaded_file = st.file_uploader("⬆️ 학원교습소 CSV 파일을 업로드하세요", type=["csv"])

def read_csv_auto(file):
    """여러 인코딩 시도"""
    encodings = ["utf-8", "cp949", "euc-kr"]
    for enc in encodings:
        try:
            return pd.read_csv(file, encoding=enc)
        except UnicodeDecodeError:
            continue
    st.error("❌ 파일 인코딩을 인식할 수 없습니다. CSV를 UTF-8 또는 CP949로 저장해주세요.")
    return None

# -------------------------------
# 📊 데이터 로드 및 분석
# -------------------------------
if uploaded_file is not None:
    df = read_csv_auto(uploaded_file)

    if df is not None:
        df.columns = df.columns.str.strip()
        st.success(f"✅ 데이터 로드 완료! ({df.shape[0]}행 × {df.shape[1]}열)")
        st.write("**컬럼 예시:**", ", ".join(df.columns[:10]))

        # -------------------------------
        # ⚙️ 컬럼 자동 탐색
        # -------------------------------
        cols = df.columns.tolist()
        region_cols = [c for c in cols if any(x in c for x in ["시도", "시군구", "주소"])]
        category_cols = [c for c in cols if any(x in c for x in ["업종", "교습", "분야"])]

        if not region_cols:
            st.error("❌ CSV에 '시도', '시군구', '주소' 관련 컬럼이 없습니다.")
        if not category_cols:
            st.error("❌ CSV에 '업종', '교습', '분야' 관련 컬럼이 없습니다.")

        if region_cols and category_cols:
            st.sidebar.header("🔍 설정")
            region_col = st.sidebar.selectbox("📍 지역 컬럼 선택", region_cols)
            category_col = st.sidebar.selectbox("🏫 업종/분류 컬럼 선택", category_cols)

            # -------------------------------
            # 📈 지역별 학원 수 TOP 10
            # -------------------------------
            st.subheader("📍 지역별 학원 수 TOP 10")
            region_count = (
                df[region_col].value_counts()
                .reset_index()
                .rename(columns={"index": region_col, region_col: "학원 수"})
            )
            top_regions = region_count.head(10)

            chart_region = (
                alt.Chart(top_regions)
                .mark_bar()
                .encode(
                    x=alt.X("학원 수:Q"),
                    y=alt.Y(f"{region_col}:N", sort="-x"),
                    color=alt.Color("학원 수:Q", scale=alt.Scale(scheme="blues")),
                    tooltip=[region_col, "학원 수"]
                )
                .properties(height=400, title="지역별 학원 수 TOP 10")
            )
            st.altair_chart(chart_region, use_container_width=True)

            # -------------------------------
            # 🏫 업종별 학원 수 TOP 10
            # -------------------------------
            st.subheader("🏫 업종별 학원 수 TOP 10")
            category_count = (
                df[category_col].value_counts()
                .reset_index()
                .rename(columns={"index": category_col, category_col: "학원 수"})
            )
            top_categories = category_count.head(10)

            chart_category = (
                alt.Chart(top_categories)
                .mark_bar()
                .encode(
                    x=alt.X("학원 수:Q"),
                    y=alt.Y(f"{category_col}:N", sort="-x"),
                    color=alt.Color("학원 수:Q", scale=alt.Scale(scheme="greens")),
                    tooltip=[category_col, "학원 수"]
                )
                .properties(height=400, title="업종별 학원 수 TOP 10")
            )
            st.altair_chart(chart_category, use_container_width=True)

            # -------------------------------
            # 🎯 특정 업종의 지역별 분포
            # -------------------------------
            st.subheader("🎯 특정 업종의 지역별 분포")
            selected_category = st.selectbox("분포를 보고 싶은 업종을 선택하세요", category_count[category_col].unique())

            filtered = df[df[category_col] == selected_category]
            region_dist = (
                filtered[region_col].value_counts()
                .reset_index()
                .rename(columns={"index": region_col, region_col: "학원 수"})
            )

            chart_filtered = (
                alt.Chart(region_dist)
                .mark_bar()
                .encode(
                    x=alt.X("학원 수:Q"),
                    y=alt.Y(f"{region_col}:N", sort="-x"),
                    color=alt.Color("학원 수:Q", scale=alt.Scale(scheme="tealblues")),
                    tooltip=[region_col, "학원 수"]
                )
                .properties(height=400, title=f"'{selected_category}' 업종의 지역별 분포")
            )
            st.altair_chart(chart_filtered, use_container_width=True)

            # -------------------------------
            # 📋 데이터 미리보기
            # -------------------------------
            with st.expander("📋 데이터 미리보기"):
                st.dataframe(df.head(50))
else:
    st.info("👆 먼저 CSV 파일을 업로드해주세요.")
