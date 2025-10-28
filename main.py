import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="국가별 MBTI 분석", page_icon="🌍", layout="wide")

st.title("🌍 국가별 MBTI 분포 분석 대시보드")
st.markdown("""
이 앱은 국가별 MBTI 분포 데이터를 시각적으로 분석합니다.  
CSV 파일을 업로드하고, 특정 MBTI 유형이 높은 국가 TOP 10을 확인해보세요.
""")

# 파일 업로더
uploaded_file = st.file_uploader("📂 CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.success("✅ 파일이 성공적으로 업로드되었습니다!")
    
    # 데이터 미리보기
    with st.expander("🔍 데이터 미리보기"):
        st.dataframe(df.head())

    # 컬럼에서 MBTI 유형만 추출 (Country 제외)
    mbti_cols = [col for col in df.columns if col.lower() != 'country']
    
    st.subheader("🧠 분석할 MBTI 유형 선택")
    selected_type = st.selectbox("분석할 MBTI 유형을 선택하세요:", mbti_cols)

    # 선택한 유형 기준으로 정렬
    top10 = df.nlargest(10, selected_type)

    st.markdown(f"### 🌐 {selected_type} 유형이 높은 국가 TOP 10")

    # Altair 시각화
    chart = (
        alt.Chart(top10)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X(selected_type, title=f"{selected_type} 비율(%)"),
            y=alt.Y("Country", sort='-x', title="국가"),
            color=alt.Color(selected_type, scale=alt.Scale(scheme='tealblues')),
            tooltip=["Country", selected_type]
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
st.caption("© 2025 MBTI World Insight Dashboard by 현겸 🧭")
