import streamlit as st

# 1. 페이지 설정
st.set_page_config(layout="wide")

st.title("상담 교육 플랫폼 구조")
st.write("---")

# 2. 상단 3단 표 레이아웃
col1, col2, col3 = st.columns(3)

with col1:
    st.info("### 공급자, 생산자")
    st.markdown("<h4 style='color: red; text-align: center;'>학교 내 근무하고 있는 전문상담교사</h4>", unsafe_allow_html=True)
    st.markdown("1. 전문분야 차이 반영\n2. 내담자 특성 반영 전문가 개발\n3. 자료 및 방법 공유\n4. 자문 활동 수행")

with col2:
    st.success("### 플랫폼")
    st.markdown("<h4 style='color: green; text-align: center;'>교환가치</h4>", unsafe_allow_html=True)
    st.info("공급자와 내담자를 적절히 매칭하여 만족스러운 서비스를 제공하는 교육 플랫폼 개발")

with col3:
    st.warning("### 소비자")
    st.markdown("<h4 style='color: blue; text-align: center;'>학생 내담자</h4>", unsafe_allow_html=True)
    st.write("① 공황장애 ② 우울증 ③ ADHD ④ 대인관계 ⑤ 진로상담 등")

st.write("---")

# 3. 하단 상담 신청 기능 (여기에 이어서 추가된 것)
st.write("### 📅 실시간 상담 신청")
c_left, c_right = st.columns(2)

with c_left:
    name = st.text_input("학생 성함")
    issue = st.selectbox("상담 분야", ["우울증", "ADHD", "진로상담", "기타"])

with c_right:
    date = st.date_input("희망 날짜")
    contact = st.text_input("연락처")

if st.button("상담 신청하기"):
    if name and contact:
        st.balloons()
        st.success(f"{name}님, 신청이 완료되었습니다!")
    else:
        st.error("성함과 연락처를 입력해주세요.")