
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 페이지 설정
st.set_page_config(
    page_title="붓꽃 품종 예측 및 알고리즘 비교",
    page_icon="🌸",
    layout="wide"
)

st.title("🌸 붓꽃 품종 예측 및 알고리즘 비교")
st.write("3가지 머신러닝 알고리즘으로 붓꽃의 품종을 예측합니다.")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("Iris.csv", encoding="cp949")

    df.columns = [
        "꽃받침길이",
        "꽃받침너비",
        "꽃잎길이",
        "꽃잎너비",
        "품종"
    ]

    return df

df = load_data()

# 사용할 데이터
X = df[["꽃잎길이", "꽃잎너비"]]
y = df["품종"]

# 학습 데이터와 테스트 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 알고리즘 생성 함수
def create_models():

    models = {
        "KNN": make_pipeline(
            StandardScaler(),
            KNeighborsClassifier(n_neighbors=5)
        ),

        "Decision Tree": DecisionTreeClassifier(
            max_depth=4,
            random_state=42
        ),

        "Random Forest": RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )
    }

    return models


models = create_models()

# 알고리즘별 정확도 평가
accuracy_results = {}

for name, model in models.items():

    model.fit(X_train, y_train)

    test_prediction = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        test_prediction
    )

    accuracy_results[name] = accuracy * 100

# 전체 데이터로 다시 학습
for model in models.values():
    model.fit(X, y)

# 입력 가능한 범위
min_length = float(df["꽃잎길이"].min())
max_length = float(df["꽃잎길이"].max())

min_width = float(df["꽃잎너비"].min())
max_width = float(df["꽃잎너비"].max())

st.divider()

# 입력 범위 안내
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

# 사용자 입력
st.divider()
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

# 사용자 입력 데이터
input_data = pd.DataFrame(
    [[petal_length, petal_width]],
    columns=["꽃잎길이", "꽃잎너비"]
)

# 알고리즘별 예측
st.divider()
st.subheader("🔍 3가지 알고리즘 예측 결과")

prediction_results = {}

for name, model in models.items():

    prediction = model.predict(input_data)[0]

    prediction_results[name] = prediction

# 결과 표시
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### KNN")
    st.success(prediction_results["KNN"])

with col2:
    st.markdown("### Decision Tree")
    st.success(prediction_results["Decision Tree"])

with col3:
    st.markdown("### Random Forest")
    st.success(prediction_results["Random Forest"])

# 결과 비교표
st.subheader("📊 알고리즘별 예측 및 정확도 비교")

result_df = pd.DataFrame({
    "알고리즘": list(prediction_results.keys()),
    "예측 품종": list(prediction_results.values()),
    "정확도(%)": [
        round(accuracy_results[name], 2)
        for name in prediction_results
    ]
})

st.dataframe(
    result_df,
    use_container_width=True,
    hide_index=True
)

# 정확도 그래프
st.subheader("📈 알고리즘별 정확도 비교")

fig2, ax2 = plt.subplots(figsize=(8, 4))

ax2.bar(
    accuracy_results.keys(),
    accuracy_results.values()
)

ax2.set_ylim(0, 105)
ax2.set_ylabel("Accuracy (%)")
ax2.set_title("Algorithm Accuracy Comparison")
ax2.grid(axis="y", alpha=0.3)

st.pyplot(fig2)

# 꽃잎 길이와 너비 그래프
st.divider()
st.subheader("📍 꽃잎 길이와 너비의 분포")

fig, ax = plt.subplots(figsize=(9, 6))

# 품종별 데이터 표시
for species in df["품종"].unique():

    subset = df[df["품종"] == species]

    ax.scatter(
        subset["꽃잎길이"],
        subset["꽃잎너비"],
        label=species,
        alpha=0.7
    )

# 사용자 입력값 노란색 별 표시
ax.scatter(
    petal_length,
    petal_width,
    color="yellow",
    edgecolors="black",
    marker="*",
    s=450,
    label="User Input",
    zorder=5
)

ax.set_xlabel("꽃잎 길이(cm)")
ax.set_ylabel("꽃잎 너비(cm)")
ax.set_title("Iris Petal Classification")
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)

st.caption("★ 노란색 별은 사용자가 입력한 꽃잎의 위치입니다.")

# 알고리즘 설명
st.divider()
st.subheader("📚 알고리즘 작동 원리")

with st.expander("1. KNN 작동 원리"):
    st.write("""
    새로운 데이터와 가장 가까운 5개의 데이터를 찾습니다.
    주변 데이터 중 가장 많이 나타나는 품종을
    최종 예측 결과로 선택합니다.
    """)

with st.expander("2. Decision Tree 작동 원리"):
    st.write("""
    꽃잎 길이와 너비를 기준으로 여러 조건을 나눕니다.
    나누어진 조건을 따라가면서 최종 붓꽃 품종을 결정합니다.
    """)

with st.expander("3. Random Forest 작동 원리"):
    st.write("""
    여러 개의 의사결정나무를 만들어 각각 품종을 예측합니다.
    각 나무의 예측 결과를 투표하여
    가장 많은 표를 얻은 품종을 최종 결과로 선택합니다.
    """)

# 원본 데이터
with st.expander("원본 데이터 확인"):
    st.dataframe(df, use_container_width=True)
