import streamlit as st

st.set_page_config(layout="wide") # 화면을 넓게 쓰도록 설정

st.title('두 번째 프로젝트: 3컬럼 레이아웃')

# 똑같은 비율의 3개 컬럼 생성
col1, col2, col3 = st.columns(3)

with col1:
    st.header("1번 기둥")
    st.write("첫 번째 영역입니다.")
    st.button("버튼 1")

with col2:
    st.header("2번 기둥")
    st.write("두 번째 영역입니다.")
    st.checkbox("체크박스")

with col3:
    st.header("3번 기둥")
    st.write("세 번째 영역입니다.")
    st.date_input("날짜 선택")