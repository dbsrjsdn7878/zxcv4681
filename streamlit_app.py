import streamlit as st
import pandas as pd
import random

# ======== 💎 스타일 추가 (CSS) ========
st.markdown(
    """
    <style>
        .title {
            font-size: 40px;
            font-weight: bold;
            text-align: center;
            color: #FFD700;
            text-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);
        }
        .subtitle {
            font-size: 20px;
            text-align: center;
            color: #FFFFFF;
            padding: 10px;
        }
        .team-card {
            padding: 15px;
            border-radius: 10px;
            box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.2);
            margin-bottom: 15px;
            text-align: center;
        }
        .team1 {
            background-color: rgba(0, 102, 204, 0.8);
            color: white;
        }
        .team2 {
            background-color: rgba(204, 0, 0, 0.8);
            color: white;
        }
        .btn {
            background: linear-gradient(90deg, #ff8c00, #ff4500);
            color: white;
            border: none;
            padding: 12px;
            font-size: 18px;
            border-radius: 10px;
            cursor: pointer;
            transition: 0.3s;
            display: block;
            margin: auto;
            width: 200px;
            text-align: center;
        }
        .btn:hover {
            background: linear-gradient(90deg, #ff4500, #ff0000);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ======== 🎮 헤더 ========
st.markdown('<h1 class="title">⚔️ 롤 5대5 내전 팀 배정</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">친구들의 닉네임, 실력, 포지션을 입력하고 균형 잡힌 팀을 배정합니다!</p>', unsafe_allow_html=True)

# ======== 🏆 포지션 목록 ========
positions = ["탑", "정글", "미드", "원딜", "서폿"]

# ======== 📋 입력 데이터 ========
default_data = {
    "닉네임": [f"플레이어{i+1}" for i in range(10)],
    "실력 (1~10)": [5] * 10,
    "포지션": positions * 2  # 5개 포지션을 두 번 반복
}

df = pd.DataFrame(default_data)
edited_df = st.data_editor(df, num_rows="fixed")  # 사용자 입력 가능하도록 설정

# ======== 🏁 팀 배정 버튼 ========
if st.markdown('<button class="btn">🔥 팀 배정 시작</button>', unsafe_allow_html=True):
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

    # ======== 🔥 결과 출력 (카드 스타일) ========
    st.subheader("🏆 팀 배정 결과")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="team-card team1">', unsafe_allow_html=True)
        st.write(f"**🔵 팀 1 (총 실력 {team1_score})**")
        st.table(pd.DataFrame(team1))
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="team-card team2">', unsafe_allow_html=True)
        st.write(f"**🔴 팀 2 (총 실력 {team2_score})**")
        st.table(pd.DataFrame(team2))
        st.markdown('</div>', unsafe_allow_html=True)

    # 최종 밸런스 점검
    st.success(f"✅ 팀 간 실력 차이: {abs(team1_score - team2_score)}")
