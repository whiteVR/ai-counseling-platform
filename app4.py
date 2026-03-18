import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(layout="wide")

st.title("상담 교육 플랫폼 구조")
st.write("---")

# 2. 상단 3단 표 레이아웃 (기존 내용 유지)
col1, col2, col3 = st.columns(3)
with col1:
    st.info("### 공급자, 생산자")
    st.markdown("1. 전문분야 차이 반영\n2. 내담자 특성 반영 전문가 개발")
with col2:
    st.success("### 플랫폼")
    st.info("공급자와 내담자를 적절히 매칭하는 플랫폼 개발")
with col3:
    st.warning("### 소비자")
    st.write("① 공황장애 ② 우울증 ③ ADHD 등")

st.write("---")

# 3. 하단 상담 신청 기능 및 엑셀 저장
st.write("### 📅 실시간 상담 신청")

# 세션 상태(Session State)를 이용해 신청 데이터를 임시 저장합니다.
if 'consultation_data' not in st.session_state:
    st.session_state['consultation_data'] = []

c_left, c_right = st.columns(2)

with c_left:
    name = st.text_input("학생 성함")
    issue = st.selectbox("상담 분야", ["우울증", "ADHD", "진로상담", "대인관계", "기타"])

with c_right:
    date = st.date_input("희망 날짜")
    contact = st.text_input("연락처")

# 신청 버튼 클릭 시 동작
if st.button("상담 신청하기"):
    if name and contact:
        # 데이터 리스트에 추가
        new_data = {
            "신청시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "성함": name,
            "상담분야": issue,
            "희망날짜": date.strftime("%Y-%m-%d"),
            "연락처": contact
        }
        st.session_state['consultation_data'].append(new_data)
        st.balloons()
        st.success(f"{name}님, 신청 목록에 추가되었습니다!")
    else:
        st.error("성함과 연락처를 입력해주세요.")

# 4. 저장된 데이터 보여주기 및 엑셀 다운로드
if st.session_state['consultation_data']:
    st.write("---")
    st.write("### 📊 현재 신청 현황")
    
    # 리스트를 판다스 데이터프레임으로 변환
    df = pd.DataFrame(st.session_state['consultation_data'])
    st.table(df) # 화면에 표로 출력

    # 엑셀 파일로 변환 (바이너리 데이터)
    import io
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='상담신청목록')
    
    excel_data = output.getvalue()

    # 다운로드 버튼 생성
    st.download_button(
        label="📥 신청 내역 엑셀로 내보내기",
        data=excel_data,
        file_name=f"상담신청현황_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    # 5. 상담 분야별 통계 차트
    st.write("---")
    st.write("### 📈 상담 분야별 신청 현황")

    if not df.empty:
        # 상담분야별로 개수를 세어 차트용 데이터 만들기
        chart_data = df['상담분야'].value_counts()
        
        # 스트림릿 기본 막대 차트 출력
        st.bar_chart(chart_data)
        
        # 좀 더 자세한 수치를 보고 싶다면
        col_count, col_dummy = st.columns([1, 2])
        with col_count:
            st.dataframe(chart_data.rename("신청 건수"))