
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="서울 버스 운행 분석",
    page_icon="🚌",
    layout="wide"
)

st.title("🚌 서울특별시 버스 운행 분석")
st.write("서울특별시 버스 출발시간 데이터를 분석합니다.")

# CSV 파일 불러오기
df = pd.read_csv(
    "서울특별시_버스 운행 출발시간 (2).csv",
    encoding="cp949"
)

# 출발시간을 시간으로 변환
df["출발시간"] = pd.to_datetime(
    df["출발시간"],
    format="%H:%M:%S"
)

df["시간대"] = df["출발시간"].dt.hour

# 주요 정보
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("전체 운행 횟수", f"{len(df)}회")

with col2:
    st.metric("운행 노선 수", f"{df['노선_ID'].nunique()}개")

with col3:
    st.metric("운행 차량 수", f"{df['차량_ID'].nunique()}대")

st.divider()

# 시간대별 운행 횟수
st.subheader("1. 시간대별 버스 운행 횟수")

time_count = df["시간대"].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(10, 5))
time_count.plot(kind="bar", ax=ax)

ax.set_title("시간대별 버스 운행 횟수")
ax.set_xlabel("출발 시간")
ax.set_ylabel("운행 횟수")
ax.grid(axis="y", alpha=0.3)

st.pyplot(fig)

# 노선별 운행 횟수
st.subheader("2. 노선별 운행 횟수")

route_count = df["노선_ID"].value_counts()

fig2, ax2 = plt.subplots(figsize=(10, 5))
route_count.plot(kind="bar", ax=ax2)

ax2.set_title("노선별 버스 운행 횟수")
ax2.set_xlabel("노선 ID")
ax2.set_ylabel("운행 횟수")
ax2.grid(axis="y", alpha=0.3)

st.pyplot(fig2)

# 노선 선택
st.subheader("3. 노선별 상세 정보")

selected_route = st.selectbox(
    "노선을 선택하세요.",
    sorted(df["노선_ID"].unique())
)

filtered_df = df[df["노선_ID"] == selected_route]

st.write(f"선택한 노선: {selected_route}")
st.write(f"총 운행 횟수: {len(filtered_df)}회")

st.dataframe(filtered_df, use_container_width=True)

# 전체 데이터
st.subheader("4. 전체 버스 운행 데이터")
st.dataframe(df, use_container_width=True)

