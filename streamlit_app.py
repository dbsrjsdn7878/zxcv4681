import streamlit as st
import random

st.title("⚔️ 롤 5대5 내전 팀 밸런스 + 포지션 배정")
st.write("친구들의 닉네임, 실력, 포지션을 입력하면 자동으로 균형 잡힌 팀을 배정합니다!")

# 포지션 목록
positions = ["탑", "정글", "미드", "원딜", "서폿"]

# 플레이어 데이터 저장
players = []
player_data = {}

st.subheader("🔹 플레이어 입력")

for i in range(10):
    name = st.text_input(f"플레이어 {i+1} 닉네임", key=f"name_{i}")
    skill = st.slider(f"{name} 실력 (1~10)", 1, 10, 5, key=f"skill_{i}")
    position = st.selectbox(f"{name} 희망 포지션", positions, key=f"position_{i}")
    
    if name:
        players.append(name)
        player_data[name] = {"skill": skill, "position": position}

# 팀 배정 버튼
if st.button("팀 배정 시작"):
    if len(players) != 10:
        st.error("❗ 10명의 플레이어 정보를 모두 입력해주세요!")
    else:
        # 포지션별로 정렬
        position_groups = {pos: [] for pos in positions}

        for name, data in player_data.items():
            position_groups[data["position"]].append((name, data["skill"]))

        # 각 포지션별 균형 잡힌 팀 배정
        team1, team2 = [], []
        team1_score, team2_score = 0, 0

        for pos in positions:
            if len(position_groups[pos]) < 2:
                st.error(f"❗ {pos} 포지션에 플레이어가 부족합니다! (최소 2명 필요)")
                break

            # 해당 포지션에서 실력 기준 정렬 후 배정
            sorted_players = sorted(position_groups[pos], key=lambda x: x[1], reverse=True)
            player1, player2 = sorted_players[:2]  # 상위 2명 선택

            if team1_score <= team2_score:
                team1.append((player1[0], pos, player1[1]))
                team2.append((player2[0], pos, player2[1]))
                team1_score += player1[1]
                team2_score += player2[1]
            else:
                team1.append((player2[0], pos, player2[1]))
                team2.append((player1[0], pos, player1[1]))
                team1_score += player2[1]
                team2_score += player1[1]

        # 결과 출력
        st.subheader("🔥 팀 배정 결과")
        st.write(f"**팀 1 (총 실력 {team1_score})**")
        for p in team1:
            st.write(f"- {p[0]} ({p[1]}) - 실력 {p[2]}")

        st.write(f"\n**팀 2 (총 실력 {team2_score})**")
        for p in team2:
            st.write(f"- {p[0]} ({p[1]}) - 실력 {p[2]}")

        # 최종 밸런스 점검
        st.success(f"✅ 팀 간 실력 차이: {abs(team1_score - team2_score)}")
