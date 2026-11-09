
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# 페이지 설정
st.set_page_config(
    page_title="월별 기온분석",
    page_icon="🌡️",
    layout="wide"
)

# 제목
st.title("🌡️ 월별 기온분석")
st.write("원하는 월을 선택하여 연도별 최고기온과 최저기온을 비교해 보세요.")

# CSV 파일 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "temperature.csv")

# 데이터 불러오기
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(CSV_PATH, encoding="cp949")
    except UnicodeDecodeError:
        df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")

    # 날짜 변환
    df["일시"] = pd.to_datetime(df["일시"], errors="coerce")

    # 연도와 월 추출
    df["연도"] = df["일시"].dt.year
    df["월"] = df["일시"].dt.month

    # 기온 데이터 숫자형 변환
    df["최고기온(℃)"] = pd.to_numeric(
        df["최고기온(℃)"], errors="coerce"
    )

    df["최저기온(℃)"] = pd.to_numeric(
        df["최저기온(℃)"], errors="coerce"
    )

    return df


# 데이터 실행
try:
    df = load_data()

    # 월 선택
    month = st.selectbox(
        "📅 분석할 월을 선택하세요.",
        range(1, 13),
        format_func=lambda x: f"{x}월"
    )

    # 선택한 월 데이터 추출
    filtered_df = df[df["월"] == month].copy()

    # 결측치 제거
    filtered_df = filtered_df.dropna(
        subset=["연도", "최고기온(℃)", "최저기온(℃)"]
    )

    # 연도별 기온 정리
    yearly_df = (
        filtered_df.groupby("연도")
        .agg({
            "최고기온(℃)": "max",
            "최저기온(℃)": "min"
        })
        .reset_index()
        .sort_values("연도")
    )

    # 그래프 출력
    if not yearly_df.empty:

        fig = go.Figure()

        # 최고기온 (핫핑크)
        fig.add_trace(go.Scatter(
            x=yearly_df["연도"],
            y=yearly_df["최고기온(℃)"],
            mode="lines+markers",
            name="최고기온",
            line=dict(color="hotpink", width=2),
            marker=dict(size=6)
        ))

        # 최저기온 (파란색)
        fig.add_trace(go.Scatter(
            x=yearly_df["연도"],
            y=yearly_df["최저기온(℃)"],
            mode="lines+markers",
            name="최저기온",
            line=dict(color="blue", width=2),
            marker=dict(size=6)
        ))

        # 그래프 설정
        fig.update_layout(
            title={
                "text": f"{month}월별 기온분석",
                "x": 0.5
            },
            xaxis_title="연도",
            yaxis_title="온도(℃)",
            legend_title="범례",
            hovermode="x unified",
            template="plotly_white"
        )

        # 그래프 화면 출력
        st.plotly_chart(fig, use_container_width=True)

        # 데이터 표
        with st.expander("📊 분석 데이터 확인하기"):
            st.dataframe(yearly_df, use_container_width=True)

    else:
        st.warning("선택한 월에 분석할 데이터가 없습니다.")

except FileNotFoundError:
    st.error("temperature.csv 파일을 찾을 수 없습니다. 상위 폴더에 파일이 있는지 확인하세요.")

except Exception as e:
    st.error(f"데이터 처리 중 오류가 발생했습니다: {e}")
