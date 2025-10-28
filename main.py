import streamlit as st
import pandas as pd
import altair as alt

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="MBTI by Country Dashboard",
    page_icon="🌍",
    layout="centered"
)

st.title("🌍 MBTI 유형별 국가 TOP 10 시각화")
st.caption("특정 MBTI 유형 비율이 높은 나라를 한눈에 볼 수 있는 대시보드입니다.")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# -----------------------------
# 인터페이스: 사용자 입력
# -----------------------------
mbti_types = [c for c in df.columns if c != "Country"]
selected_type = st.selectbox("🔍 분석할 MBTI 유형을 선택하세요:", mbti_types, index=0)

# -----------------------------
# 데이터 처리
# -----------------------------
top10 = (
    df[["Country", selected_type]]
    .sort_values(by=selected_type, ascending=False)
    .head(10)
)

# -----------------------------
# 시각화 (Altair)
# -----------------------------
bar_chart = (
    alt.Chart(top10)
    .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
    .encode(
        x=alt.X(selected_type, title=f"{selected_type} 비율", scale=alt.Scale(zero=False)),
        y=alt.Y("Country", sort='-x', title="국가"),
        color=alt.Color(selected_type, scale=alt.Scale(scheme="tealblues")),
        tooltip=["Country", selected_type]
    )
    .properties(
        width=600,
        height=400,
        title=f"{selected_type} 유형이 높은 국가 TOP 10"
    )
)

st.altair_chart(bar_chart, use_container_width=True)

# -----------------------------
# 추가 정보 표시
# -----------------------------
st.subheader("📊 데이터 미리보기")
st.dataframe(top10, use_container_width=True)

st.markdown("---")
st.caption("데이터 출처: countriesMBTI_16types.csv  |  Visualization: Altair × Streamlit")
