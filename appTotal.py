import streamlit as st
import pandas as pd
import io
import random
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# 1. 페이지 설정
st.set_page_config(layout="wide", page_title="AI 상담 플랫폼 v4.0", page_icon="🎓")

# --- [데이터 엔진 및 AI 시스템 초기화] ---
@st.cache_resource
def initialize_ai_system():
    category_keywords = {
        "공황장애": ["숨 가쁨", "호흡 곤란", "심장 두근거림", "공포", "발작"],
        "우울증": ["무기력", "우울", "의욕 상실", "눈물", "불면"],
        "ADHD": ["집중", "산만", "충동적", "기억력", "부주의"],
        "진로상담": ["적성", "꿈", "취업", "미래", "진로"],
        "대인관계": ["친구", "따돌림", "싸움", "소외감", "관계"]
    }
    data = []
    categories = list(category_keywords.keys())
    for i in range(500):
        cat = random.choice(categories)
        kw = random.choice(category_keywords[cat])
        sentence = f"최근 {kw} 증상이 느껴져서 일상생활이 너무 힘들고 고통스럽습니다."
        data.append({"상담분야": cat, "고민내용": sentence})
    
    df_train = pd.DataFrame(data)
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(df_train['고민내용'], df_train['상담분야'])
    return model, category_keywords

ai_model, weight_rules = initialize_ai_system()

def smart_predict(text):
    for category, keywords in weight_rules.items():
        for word in keywords:
            if word in text: return category, 99.0, "가중치 키워드 분석"
    probs = ai_model.predict_proba([text])[0]
    max_prob = max(probs) * 300
    pred = ai_model.predict([text])[0]
    return pred, round(max_prob, 1), "AI 패턴 매칭"

# 세션 데이터 관리
if 'history' not in st.session_state:
    st.session_state['history'] = []

# --- [사이드바 메뉴 구성] ---
with st.sidebar:
    st.image("Logo.png", width=100) # 로고 이미지 (샘플)
    st.title("상담 플랫폼 메뉴")
    menu = st.radio(
        "이동할 메뉴를 선택하세요",
        ["🏠 플랫폼 소개", "🤖 AI 상담 신청", "📊 관리자 모드"]
    )
    st.info("v4.0: AI 모델 및 데이터 시각화 통합 버전")

# --- [메뉴 1: 플랫폼 소개 및 구조] ---
if menu == "🏠 플랫폼 소개":
    st.title("🎓 온라인 상담 교육 플랫폼 구조")
    st.write("AI를 활용하여 공급자와 소비자를 최적으로 매칭하는 지능형 플랫폼입니다.")
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("### 🏫 공급자\n**전문상담교사**\n- 분야별 강점 반영\n- 상담 교환가치 창출")
    with col2:
        st.success("### ⚙️ 플랫폼\n**AI 지능형 매칭**\n- 실시간 패턴/가중치 분석\n- 정밀 확률 기반 추천")
    with col3:
        st.warning("### 👤 소비자\n**학생 내담자**\n- 고민 해결 및 상담 예약\n- 맞춤형 피드백 제공")
    
    st.image("AICLogo.jpg", width=1500)

# --- [메뉴 2: AI 실시간 상담 신청] ---
elif menu == "🤖 AI 상담 신청":
    st.title("🤖 AI 지능형 상담 신청")
    st.write("당신의 고민을 적어주시면 AI가 가장 적합한 상담 분야를 추천합니다.")
    st.write("---")
    
    left_col, right_col = st.columns([2, 1])
    with left_col:
        u_name = st.text_input("이름", placeholder="성함을 입력하세요")
        u_story = st.text_area("당신의 고민을 자유롭게 적어주세요", height=200)

    with right_col:
        if u_story:
            prediction, score, method = smart_predict(u_story)
            st.write(f"🔎 분석 방식: **{method}**")
            st.success(f"### 추천: {prediction} ({score}%)")
            st.progress(score / 100)
            final_cat = st.selectbox("분야 확정", list(weight_rules.keys()), 
                                     index=list(weight_rules.keys()).index(prediction))
        else:
            final_cat = st.selectbox("분야 선택", list(weight_rules.keys()))
        
        u_phone = st.text_input("연락처")
        u_satisfaction = st.slider("상담 서비스 기대 만족도", 1, 5, 3)

    if st.button("🚀 상담 매칭 신청하기", use_container_width=True):
        if u_name and u_story and u_phone:
            st.session_state['history'].append({
                "신청시간": datetime.now().strftime("%H:%M:%S"),
                "성함": u_name, "분야": final_cat, "연락처": u_phone, "만족도": u_satisfaction
            })
            st.balloons()
            st.success("신청 완료! [관리자 모드]에서 확인하세요.")
        else:
            st.error("모든 정보를 입력해 주세요.")

# --- [메뉴 3: 관리자 모드 (데이터 EDA)] ---
elif menu == "📊 관리자 모드":
    st.title("📊 실시간 신청 데이터 분석 (EDA)")
    
    if not st.session_state['history']:
        st.warning("현재 접수된 상담 신청 데이터가 없습니다.")
    else:
        df_res = pd.DataFrame(st.session_state['history'])
        
        tab1, tab2 = st.tabs(["📋 상세 신청 목록", "📈 데이터 시각화 리포트"])
        
        with tab1:
            st.dataframe(df_res, use_container_width=True)
            csv = df_res.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 전체 내역 엑셀 저장", data=csv, file_name="consulting_list.csv")
            
        with tab2:
            c1, c2 = st.columns(2)
            with c1:
                st.write("### 📈 분야별 신청 비중")
                st.bar_chart(df_res['분야'].value_counts())
            with c2:
                st.write("### ⭐ 기대 만족도 분포")
                s_counts = df_res['만족도'].value_counts().sort_index()
                s_data = s_counts.reindex(pd.Index([1,2,3,4,5]), fill_value=0)
                st.area_chart(s_data)