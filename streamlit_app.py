import streamlit as st
import random

# 데이트 장소 데이터
date_spots = {
    "카페": ["스타벅스", "블루보틀", "할리스커피", "빽다방", "앤티크 감성 카페"],
    "레스토랑": ["이탈리안 레스토랑", "스시 오마카세", "한정식 맛집", "바베큐 전문점", "베트남 쌀국수집"],
    "공원": ["한강공원", "서울숲", "남산공원", "어린이대공원", "경의선 숲길"],
    "액티비티": ["방탈출 카페", "VR 체험관", "보드게임 카페", "노래방", "클라이밍 체험장"],
}

# Streamlit UI
st.title("💖 데이트 장소 추천기")
st.write("오늘 어떤 장소에서 데이트하고 싶나요?")

# 사용자 입력 받기
category = st.selectbox("원하는 데이트 유형을 선택하세요", list(date_spots.keys()))
indoor_outdoor = st.radio("실내/실외 선택", ["실내", "실외", "상관없음"])

# 추천 버튼
if st.button("데이트 장소 추천받기"):
    recommended_place = random.choice(date_spots[category])
    st.success(f"🎉 추천 장소: {recommended_place}")
