import streamlit as st
import pandas as pd
import random

st.title("⚔️ 롤 5대5 내전 팀 배정")
st.write("친구들의 닉네임, 실력, 포지션을 입력하고 균형 잡힌 팀을 배정합니다!")

# 포지션 목록
positions = ["탑", "정글", "미드", "원딜", "서폿"]

# 데이터프레임을 사용해 입력을 쉽게 만듦
default_data = {
    "닉네임": [f"플레이어{i+1}" for i in range(10)],
    "실력 (1~10)": [5] * 10,
    "포지션": positions * 2  # 5개 포지션을 두 번 반복
}

df = pd.DataFrame(default_data)
edited_df = st.data_editor(df, num_rows="fixed")  # 사용자 입력 가능하도록 설정

# 팀 배정 버튼
if st.button("🔥 팀 배정 시작"):
    # 플레이어 데이터 가져오기
    players = edited_df.to_dict(orient="records")

    # 포지션별로 그룹화
    position_groups = {pos: [] for pos in positions}
    for p in players:
        position_groups[p["포지션"]].append((p["닉네임"], p["실력 (1~10)"]))

    # 각 포지션별 균형 잡힌 팀 배정
    team1, team2 = [], []
    team1_score, team2_score = 0, 0

    for pos in positions:
        sorted_players = sorted(position_groups[pos], key=lambda x: x[1], reverse=True)
        if len(sorted_players) < 2:
            st.error(f"❗ {pos} 포지션에 플레이어가 부족합니다! (최소 2명 필요)")
            break

        player1, player2 = sorted_players[:2]

        if team1_score <= team2_score:
            team1.append({"닉네임": player1[0], "포지션": pos, "실력": player1[1]})
            team2.append({"닉네임": player2[0], "포지션": pos, "실력": player2[1]})
            team1_score += player1[1]
            team2_score += player2[1]
        else:
            team1.append({"닉네임": player2[0], "포지션": pos, "실력": player2[1]})
            team2.append({"닉네임": player1[0], "포지션": pos, "실력": player1[1]})
            team1_score += player2[1]
            team2_score += player1[1]

    # 결과 출력 (표 형식)
    st.subheader("🔥 팀 배정 결과")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**🔵 팀 1 (총 실력 {team1_score})**")
        st.dataframe(pd.DataFrame(team1))

    with col2:
        st.write(f"**🔴 팀 2 (총 실력 {team2_score})**")
        st.dataframe(pd.DataFrame(team2))

    # 최종 밸런스 점검
    st.success(f"✅ 팀 간 실력 차이: {abs(team1_score - team2_score)}")
