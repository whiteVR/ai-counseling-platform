import streamlit as st
import pandas as pd

st.title("📊 상담 데이터 EDA 단계")

# 데이터 불러오기
try:
    df = pd.read_csv("counseling_data.csv")

    # 1. 데이터 기본 정보
    st.subheader("1. 수집된 샘플 데이터 (상위 5개)")
    st.write(df.head())

    # 2. 분야별 상담 비중 (패턴 분석)
    st.subheader("2. 어떤 상담이 가장 많은가?")
    category_counts = df["상담분야"].value_counts()
    st.bar_chart(category_counts)

    # 3. 만족도 분포 확인
    st.subheader("3. 예상 만족도 분포")
    st.line_chart(df["만족도(예상)"])

except FileNotFoundError:
    st.error("먼저 data_gen.py를 실행하여 데이터를 생성해 주세요!")