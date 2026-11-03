
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="서울 관광지 TOP 10",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ 외국인이 좋아하는 서울 관광지 TOP 10")
st.write("서울의 대표 관광지 10곳을 지도에서 확인해 보세요!")

places = [
    {
        "name": "명동",
        "lat": 37.5636,
        "lon": 126.9850,
        "desc": "화장품, 패션 상점과 다양한 길거리 음식으로 유명한 쇼핑 거리입니다."
    },
    {
        "name": "남산서울타워",
        "lat": 37.5512,
        "lon": 126.9882,
        "desc": "서울의 아름다운 전경과 야경을 감상할 수 있는 대표 랜드마크입니다."
    },
    {
        "name": "코엑스",
        "lat": 37.5116,
        "lon": 127.0592,
        "desc": "쇼핑과 전시를 즐길 수 있으며 별마당도서관이 유명합니다."
    },
    {
        "name": "강남역",
        "lat": 37.4979,
        "lon": 127.0276,
        "desc": "다양한 맛집과 카페, 쇼핑 공간이 모여 있는 서울의 대표 번화가입니다."
    },
    {
        "name": "홍대",
        "lat": 37.5563,
        "lon": 126.9236,
        "desc": "거리 공연과 K-팝, 개성 있는 상점들을 경험할 수 있는 문화 거리입니다."
    },
    {
        "name": "남대문시장",
        "lat": 37.5592,
        "lon": 126.9777,
        "desc": "한국의 전통시장 분위기와 다양한 먹거리를 경험할 수 있습니다."
    },
    {
        "name": "동대문디자인플라자",
        "lat": 37.5671,
        "lon": 127.0095,
        "desc": "독특한 건축 디자인과 다양한 전시 및 문화행사를 즐길 수 있습니다."
    },
    {
        "name": "북촌한옥마을",
        "lat": 37.5826,
        "lon": 126.9830,
        "desc": "한국의 전통 한옥과 아름다운 골목길을 볼 수 있는 관광 명소입니다."
    },
    {
        "name": "경복궁",
        "lat": 37.5796,
        "lon": 126.9770,
        "desc": "조선 시대의 대표 궁궐로 한국의 역사와 전통문화를 체험할 수 있습니다."
    },
    {
        "name": "서울숲·성수",
        "lat": 37.5444,
        "lon": 127.0374,
        "desc": "자연을 즐길 수 있는 서울숲과 트렌디한 카페거리가 유명합니다."
    }
]

# 서울 지도 만들기
m = folium.Map(
    location=[37.5665, 126.9850],
    zoom_start=12
)

# 관광지 마커 표시
for i, place in enumerate(places, 1):
    folium.Marker(
        location=[place["lat"], place["lon"]],
        popup=f"""
        <b>TOP {i}. {place['name']}</b><br>
        {place['desc']}
        """,
        tooltip=f"TOP {i}. {place['name']}",
        icon=folium.Icon(
            color="red",
            icon="info-sign"
        )
    ).add_to(m)

# 지도 출력
st.subheader("📍 서울 관광지 지도")

st_folium(
    m,
    width=None,
    height=550,
    use_container_width=True
)

st.divider()

# 관광지 설명
st.subheader("✨ 서울 관광지 TOP 10 소개")

for i, place in enumerate(places, 1):
    with st.expander(f"TOP {i}. {place['name']}"):
        st.write(place["desc"])
        st.caption(
            f"위도: {place['lat']} / 경도: {place['lon']}"
        )

st.divider()

st.markdown(
    "🌏 **서울의 다양한 관광지를 방문하고 "
    "한국의 문화와 매력을 경험해 보세요!**"
)
