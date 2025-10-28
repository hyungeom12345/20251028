import streamlit as st
import pandas as pd
import altair as alt

# 페이지 설정
st.set_page_config(page_title="MBTI World Trends Explorer", page_icon="🌐", layout="wide")

# 제목
st.markdown("""
# 🌐 **MBTI World Trends Explorer**
세계 각국의 MBTI 분포를 탐험해보세요.  
어떤 나라가 **INTJ**가 가장 많고, 어디는 **ENFP**가 넘치는지 알아볼까요?
""")

# 파일 업로드
uploaded_file = st.file_uploader("📂 MBTI 데이터 (CSV) 업로드", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ 데이터 업로드 완료!")

    # 데이터 구조 확인
    with st.expander("🔍 데이터 미리보기"):
        st.dataframe(df.head())

    # MBTI 유형 선택
    mbti_types = [col for col in df.columns if col.lower() != "country"]
    selected_type = st.selectbox("🧠 분석할 MBTI 유형을 선택하세요:", mbti_types)

    # TOP 10 국가 선택
    top10 = df.nlargest(10, selected_type).copy()
    top10[selected_type] = top10[selected_type].round(2)

    st.markdown(f"## 🌏 {selected_type} 유형이 가장 많은 TOP 10 국가")

    # ✅ Altair 시각화 (색상 스킴 변경: "mint" → "tealblues")
    chart = (
        alt.Chart(top10)
        .mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10)
        .encode(
            x=alt.X(selected_type, title=f"{selected_type} 비율 (%)"),
            y=alt.Y("Country", sort='-x', title="국가"),
            color=alt.Color(
                selected_type,
                scale=alt.Scale(scheme="tealblues"),  # 안정적 색상 팔레트
                legend=None
            ),
            tooltip=["Country", selected_type]
        )
        .properties(height=450)
        .configure_view(strokeWidth=0)
        .configure_axis(
            labelFontSize=12,
            titleFontSize=14,
            grid=False
        )
    )

    st.altair_chart(chart, use_container_width=True)

    # 사이드 카드 형태로 표시
    st.markdown("### 🏅 국가별 세부 정보")
    cols = st.columns(5)
    for i, (country, value) in enumerate(zip(top10["Country"], top10[selected_type])):
        with cols[i % 5]:
            st.metric(label=f"🌎 {country}", value=f"{value}%", delta_color="off")

    # 하단 통계
    st.markdown("---")
    st.markdown(f"""
    ### 📈 {selected_type} 요약 통계
    - 평균 비율: **{df[selected_type].mean():.2f}%**
    - 최고 비율: **{df[selected_type].max():.2f}%**
    - 최저 비율: **{df[selected_type].min():.2f}%**
    """)

else:
    st.info("👋 먼저 MBTI CSV 파일을 업로드하세요. 예: `countriesMBTI_16types.csv`")

st.markdown("---")
st.caption("✨ Created by 현겸 | Streamlit + Altair | 2025")
