import streamlit as st
import random
import itertools

st.title("⚔️ 롤 5대5 내전 팀 밸런스 자동 배정")
st.write("친구들의 닉네임과 실력을 입력하면 자동으로 균형 잡힌 팀을 배정합니다!")

# 플레이어 입력 받기
players = []
skills = {}

st.subheader("🔹 플레이어 입력")
for i in range(10):
    name = st.text_input(f"플레이어 {i+1} 닉네임", key=f"name_{i}")
    skill = st.slider(f"{name} 실력 (1~10)", 1, 10, 5, key=f"skill_{i}")
    if name:
        players.append(name)
        skills[name] = skill

# 팀 배정 버튼
if st.button("팀 배정 시작"):
    if len(players) != 10:
        st.error("❗ 10명의 플레이어 정보를 입력해주세요!")
    else:
        # 실력 기준으로 정렬
        sorted_players = sorted(skills.items(), key=lambda x: x[1], reverse=True)
        
        # 균형 잡힌 팀 구성
        team1, team2 = [], []
        team1_score, team2_score = 0, 0

        for name, skill in sorted_players:
            if team1_score <= team2_score:
                team1.append((name, skill))
                team1_score += skill
            else:
                team2.append((name, skill))
                team2_score += skill
        
        # 결과 출력
        st.subheader("🔥 팀 배정 결과")
        st.write(f"**팀 1 (총 실력 {team1_score})**")
        for p in team1:
            st.write(f"- {p[0]} (실력 {p[1]})")
        
        st.write(f"\n**팀 2 (총 실력 {team2_score})**")
        for p in team2:
            st.write(f"- {p[0]} (실력 {p[1]})")

        # 최종 밸런스 점검
        st.success(f"✅ 팀 간 실력 차이: {abs(team1_score - team2_score)}")
