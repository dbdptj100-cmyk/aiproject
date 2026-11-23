
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

# 페이지 설정
st.set_page_config(
    page_title="붓꽃 품종 예측",
    page_icon="🌸",
    layout="wide"
)

st.title("🌸 붓꽃 품종 예측 프로그램")
st.write("꽃잎의 길이와 너비를 입력하면 붓꽃의 품종을 예측합니다.")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("Iris.csv", encoding="cp949")

    # 첫 번째 열 이름 정리
    df.columns = [
        "꽃받침길이",
        "꽃받침너비",
        "꽃잎길이",
        "꽃잎너비",
        "품종"
    ]

    return df

df = load_data()

# 입력 범위 설정
min_length = float(df["꽃잎길이"].min())
max_length = float(df["꽃잎길이"].max())

min_width = float(df["꽃잎너비"].min())
max_width = float(df["꽃잎너비"].max())

# 입력 안내
st.subheader("📌 입력 가능한 값의 범위")

col1, col2 = st.columns(2)

with col1:
    st.info(
        f"꽃잎 길이: {min_length} ~ {max_length} cm"
    )

with col2:
    st.info(
        f"꽃잎 너비: {min_width} ~ {max_width} cm"
    )

st.divider()

# 사용자 입력
st.subheader("🌷 꽃잎 크기 입력")

col1, col2 = st.columns(2)

with col1:
    petal_length = st.number_input(
        "꽃잎 길이(cm)",
        min_value=min_length,
        max_value=max_length,
        value=1.4,
        step=0.1
    )

with col2:
    petal_width = st.number_input(
        "꽃잎 너비(cm)",
        min_value=min_width,
        max_value=max_width,
        value=0.2,
        step=0.1
    )

# KNN 분류 모델
X = df[["꽃잎길이", "꽃잎너비"]]
y = df["품종"]

model = make_pipeline(
    StandardScaler(),
    KNeighborsClassifier(n_neighbors=5)
)

model.fit(X, y)

# 품종 예측
input_data = pd.DataFrame(
    [[petal_length, petal_width]],
    columns=["꽃잎길이", "꽃잎너비"]
)

prediction = model.predict(input_data)[0]

# 예측 결과
st.subheader("🔍 예측 결과")

st.success(f"예측된 붓꽃 품종은 **{prediction}** 입니다!")

# 그래프
st.subheader("📊 꽃잎 길이와 너비의 분포")

fig, ax = plt.subplots(figsize=(9, 6))

# 품종별 산점도
for species in df["품종"].unique():
    subset = df[df["품종"] == species]

    ax.scatter(
        subset["꽃잎길이"],
        subset["꽃잎너비"],
        label=species,
        alpha=0.7
    )

# 사용자 입력 위치: 노란색 별
ax.scatter(
    petal_length,
    petal_width,
    color="yellow",
    edgecolors="black",
    marker="*",
    s=400,
    label="사용자 입력값",
    zorder=5
)

ax.set_xlabel("꽃잎 길이(cm)")
ax.set_ylabel("꽃잎 너비(cm)")
ax.set_title("붓꽃 품종별 꽃잎 크기 분포")
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)

st.caption("★ 노란색 별은 사용자가 입력한 꽃잎의 위치입니다.")

# 데이터 확인
with st.expander("원본 데이터 확인하기"):
    st.dataframe(df)
