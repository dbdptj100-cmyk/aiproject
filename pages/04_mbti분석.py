

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="세계 MBTI 탐험",
    page_icon="🌎",
    layout="wide"
)

st.title("🌎 세계 MBTI 탐험")
st.write("국가별 MBTI 16가지 유형의 비율을 확인해 보세요!")

# MBTI 유형
MBTI_TYPES = [
    "INFJ", "ISFJ", "INTP", "ISFP",
    "ENTP", "INFP", "ENTJ", "ISTP",
    "INTJ", "ESFP", "ESTJ", "ENFP",
    "ESTP", "ISTJ", "ENFJ", "ESFJ"
]

# CSV 파일 불러오기
@st.cache_data
def load_data():
    file_path = Path(__file__).parent / "countriesMBTI_16types.csv"
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    for col in MBTI_TYPES:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df.dropna(subset=["Country"] + MBTI_TYPES)

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오지 못했습니다: {e}")
    st.stop()

# 국가 선택
countries = sorted(df["Country"].unique())

default_index = (
    countries.index("South Korea")
    if "South Korea" in countries else 0
)

country = st.selectbox(
    "🌍 국가를 선택하세요",
    countries,
    index=default_index
)

# 선택한 국가 데이터
country_data = df[df["Country"] == country].iloc[0]

values = country_data[MBTI_TYPES].astype(float)

# 퍼센트 데이터 자동 처리
if values.max() <= 1:
    values = values * 100

# 데이터 정렬
chart_df = pd.DataFrame({
    "MBTI": MBTI_TYPES,
    "비율": values.values
})

chart_df = chart_df.sort_values(
    "비율",
    ascending=False
).reset_index(drop=True)

# 색상 설정
colors = ["#EF4444"]

blue_colors = [
    "#2563EB",
    "#3977E8",
    "#5189EC",
    "#699BF0",
    "#80ADF3",
    "#98BFF7",
    "#B0D1FA",
    "#C8E3FD",
    "#DBEAFE"
]

colors += [
    blue_colors[
        min(i, len(blue_colors) - 1)
    ]
    for i in range(15)
]

# 가장 높은 MBTI
top_mbti = chart_df.iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric("선택 국가", country)
col2.metric("1위 MBTI", top_mbti["MBTI"])
col3.metric("1위 비율", f'{top_mbti["비율"]:.2f}%')

st.divider()

# 막대그래프
st.subheader(f"📊 {country} MBTI 비율")

fig = px.bar(
    chart_df,
    x="비율",
    y="MBTI",
    orientation="h",
    text=chart_df["비율"].apply(
        lambda x: f"{x:.2f}%"
    )
)

fig.update_traces(
    marker_color=colors,
    textposition="outside",
    cliponaxis=False,
    hovertemplate=(
        "<b>%{y}</b><br>"
        "비율: %{x:.2f}%"
        "<extra></extra>"
    )
)

fig.update_layout(
    height=650,
    showlegend=False,
    yaxis=dict(autorange="reversed"),
    xaxis_title="MBTI 비율 (%)",
    yaxis_title="MBTI 유형",
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# 순위표
st.subheader("🏆 MBTI 순위")

ranking = chart_df.copy()
ranking.index = range(1, 17)
ranking.index.name = "순위"
ranking["비율"] = ranking["비율"].apply(
    lambda x: f"{x:.2f}%"
)

st.dataframe(
    ranking,
    use_container_width=True
)

st.caption(
    "※ 본 자료는 국가별 MBTI 비율을 시각화한 참고용 데이터입니다."
)
countriesMBTI_16types.csv
