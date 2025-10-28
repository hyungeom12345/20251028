import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="국가별 연간 강수량 분석", page_icon="☔", layout="wide")

st.title("☔ 국가별 연간 강수량 분석 대시보드")
st.markdown("""
이 앱은 국가별 연도별 강수량 데이터를 시각적으로 분석합니다.  
CSV 파일을 업로드하고, 특정 연도의 강수량이 높은 국가 TOP 10을 확인해보세요.
""")

# -------------------------------
# CSV 파일 업로드
# -------------------------------
uploaded_file = st.file_uploader("📂 CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ 파일이 성공적으로 업로드되었습니다!")
    
    # 데이터 미리보기
    with st.expander("🔍 데이터 미리보기"):
        st.dataframe(df.head())
    
    # 연도 컬럼 추출 (Country 제외)
    year_cols = [col for col in df.columns if col.lower() != "country"]
    
    st.subheader("📅 분석할 연도 선택")
    selected_year = st.selectbox("분석할 연도를 선택하세요:", year_cols)
    
    # 선택한 연도 기준으로 상위 10개 국가
    top10 = df.nlargest(10, selected_year)
    
    st.markdown(f"### 🌍 {selected_year}년 강수량이 높은 국가 TOP 10")
    
    # Altair 차트
    chart = (
        alt.Chart(top10)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X(selected_year, title=f"{selected_year}년 강수량(mm)"),
            y=alt.Y("Country", sort='-x', title="국가"),
            color=alt.Color(selected_year, scale=alt.Scale(scheme='blues')),
            tooltip=["Country", selected_year]
        )
        .properties(height=500)
        .configure_axis(
            labelFontSize=12,
            titleFontSize=14
        )
        .configure_view(strokeOpacity=0)
        .configure_title(fontSize=18, fontWeight='bold')
    )
    
    st.altair_chart(chart, use_container_width=True)
    
else:
    st.warning("📄 먼저 CSV 파일을 업로드해주세요!")

st.markdown("---")
st.caption("© 2025 Rainfall Dashboard by 현겸 🌦️")
