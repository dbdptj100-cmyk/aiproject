
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="월별 기온분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월별 기온분석")
st.write("월을 선택하면 해당 월의 연도별 최고기온과 최저기온을 확인할 수 있습니다.")

# CSV 파일 경로 찾기
current_dir = Path(__file__).resolve().parent

possible_paths = [
    current_dir / "temperature.csv",
    current_dir.parent / "temperature.csv"
]

csv_path = next(
    (path for path in possible_paths if path.exists()),
    None
)

if csv_path is None:
    st.error("temperature.csv 파일을 찾을 수 없습니다.")
    st.stop()

# CSV 파일 불러오기 (한글 인코딩)
try:
    df = pd.read_csv(csv_path, encoding="cp949")
except UnicodeDecodeError:
    df = pd.read_csv(csv_path, encoding="utf-8-sig")

# 컬럼명 정리
df.columns = df.columns.astype(str).str.strip()

# 필요한 컬럼
date_col = "최고기온일자"
max_col = "최고기온(℃)"
min_col = "최저기온(℃)"

# 컬럼 확인
required_columns = [date_col, max_col, min_col]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    st.error(
        f"CSV 파일에 필요한 컬럼이 없습니다: {missing_columns}"
    )
    st.write("현재 컬럼:", df.columns.tolist())
    st.stop()

# 날짜 및 기온 데이터 정리
df[date_col] = pd.to_datetime(
    df[date_col],
    errors="coerce"
)

df[max_col] = pd.to_numeric(
    df[max_col],
    errors="coerce"
)

df[min_col] = pd.to_numeric(
    df[min_col],
    errors="coerce"
)

# 결측치 제거
df = df.dropna(
    subset=[date_col, max_col, min_col]
).copy()

# 연도와 월 추출
df["연도"] = df[date_col].dt.year
df["월"] = df[date_col].dt.month

# 월 선택
selected_month = st.selectbox(
    "분석할 월을 선택하세요.",
    options=list(range(1, 13)),
    format_func=lambda month: f"{month}월"
)

# 선택한 월의 데이터 추출
monthly_df = (
    df[df["월"] == selected_month]
    .sort_values("연도")
    .copy()
)

if monthly_df.empty:
    st.warning("선택한 월의 데이터가 없습니다.")
    st.stop()

# 그래프 생성
fig = go.Figure()

# 최고기온 (핫핑크)
fig.add_trace(
    go.Scatter(
        x=monthly_df["연도"],
        y=monthly_df[max_col],
        mode="lines+markers",
        name="최고기온",
        line=dict(
            color="#FF69B4",
            width=3
        ),
        marker=dict(size=6)
    )
)

# 최저기온 (하늘색)
fig.add_trace(
    go.Scatter(
        x=monthly_df["연도"],
        y=monthly_df[min_col],
        mode="lines+markers",
        name="최저기온",
        line=dict(
            color="#87CEEB",
            width=3
        ),
        marker=dict(size=6)
    )
)

# 그래프 제목 및 축 설정
fig.update_layout(
    title="월별 기온분석",
    xaxis_title="연도",
    yaxis_title="온도(℃)",
    legend_title="범례",
    template="plotly_white",
    hovermode="x unified",
    font=dict(
        family="Arial, sans-serif",
        size=13
    )
)

# 축 설정
fig.update_xaxes(
    showgrid=True,
    dtick=10
)

fig.update_yaxes(
    showgrid=True
)

# 그래프 출력
st.plotly_chart(
    fig,
    use_container_width=True
)

# 분석 기간 표시
st.caption(
    f"선택한 월: {selected_month}월 | "
    f"분석 기간: {monthly_df['연도'].min()}년 ~ "
    f"{monthly_df['연도'].max()}년"
)
