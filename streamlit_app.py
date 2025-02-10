import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pykrx import stock

st.title("📈 한국 주식 데이터 시각화")

# 주식 종목 코드 입력
ticker = st.text_input("005930")

# 날짜 선택
start_date = st.date_input("2024-10-31")
end_date = st.date_input("2024-12-25")

if st.button("데이터 가져오기"):
    df = stock.get_market_ohlcv_by_date(start_date.strftime("%Y%m%d"),
                                        end_date.strftime("%Y%m%d"),
                                        ticker)

    # 주가 차트
    fig, ax = plt.subplots()
    ax.plot(df.index, df["종가"], label="종가", color="blue")
    ax.set_title(f"{ticker} 주가 추이")
    ax.legend()
    st.pyplot(fig)

    st.write(df.tail())  # 최근 데이터 출력
