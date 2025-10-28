import streamlit as st
import pandas as pd
import altair as alt

# -------------------------------
# 📂 데이터 로드
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("학원교습소정보_2021년01월31일기준.csv", encoding="utf-8")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# -------------------------------
# 🏷️ 기본 정보
# -------------------------------
st.title("📊 지역별 학원 업종 분포 분석 대시보드")
st.write("2021년 1월 기준 전국 학원교습소 데이터를 활용하여, 지역별·업종별로 학원의 분포를 분석합니다.")

# -------------------------------
# ⚙️ 데이터 컬럼 정리
# -------------------------------
cols = df.columns.tolist()
st.sidebar.header("🔍 데이터 선택")

# 지역 관련 컬럼 자동 탐색
region_cols = [c for c in cols if "시도" in c or "시군구" in c or "주소" in c]
category_cols = [c for c in cols if "업종" in c or "교습" in c or "분야" in c]

region_col = st.sidebar.selectbox("📍 지역 컬럼 선택", region_cols)
category_col = st.sidebar.selectbox("🏫 업종/분류 컬럼 선택", category_cols)

# -------------------------------
# 📈 지역별 학원 수
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
        x=alt.X("학원 수:Q", title="학원 수"),
        y=alt.Y(f"{region_col}:N", sort="-x", title="지역"),
        color=alt.Color("학원 수:Q", scale=alt.Scale(scheme="blues")),
        tooltip=[region_col, "학원 수"]
    )
    .properties(height=400, title="지역별 학원 수 TOP 10")
)
st.altair_chart(chart_region, use_container_width=True)

# -------------------------------
# 🏫 업종별 학원 수
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
        x=alt.X("학원 수:Q", title="학원 수"),
        y=alt.Y(f"{category_col}:N", sort="-x", title="업종"),
        color=alt.Color("학원 수:Q", scale=alt.Scale(scheme="tealblues")),
        tooltip=[category_col, "학원 수"]
    )
    .properties(height=400, title="업종별 학원 수 TOP 10")
)
st.altair_chart(chart_category, use_container_width=True)

# -------------------------------
# 🎯 특정 업종 선택 시 지역별 분포
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
        x=alt.X("학원 수:Q", title="학원 수"),
        y=alt.Y(f"{region_col}:N", sort="-x"),
        color=alt.Color("학원 수:Q", scale=alt.Scale(scheme="greens")),
        tooltip=[region_col, "학원 수"]
    )
    .properties(height=400, title=f"'{selected_category}' 업종의 지역별 분포")
)
st.altair_chart(chart_filtered, use_container_width=True)

# -------------------------------
# 📊 데이터 테이블
# -------------------------------
with st.expander("📋 원본 데이터 보기"):
    st.dataframe(df.head(50))
