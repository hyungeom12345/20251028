import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="학원 업종 분석", layout="wide")

st.title("📊 지역별 학원 업종 분포 분석 대시보드")
st.write("CSV 파일을 업로드하면 자동으로 시각화됩니다.")

# -------------------------------
# 📂 CSV 업로드
# -------------------------------
uploaded_file = st.file_uploader("⬆️ 학원교습소 CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding="utf-8")
    df.columns = df.columns.str.strip()

    st.success("✅ 데이터 로드 완료!")
    st.write(f"데이터 크기: {df.shape[0]}행 × {df.shape[1]}열")

    # -------------------------------
    # ⚙️ 컬럼 자동 탐색
    # -------------------------------
    cols = df.columns.tolist()
    region_cols = [c for c in cols if "시도" in c or "시군구" in c or "주소" in c]
    category_cols = [c for c in cols if "업종" in c or "교습" in c or "분야" in c]

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
