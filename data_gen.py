import pandas as pd
import random
from faker import Faker

# 한글 데이터 생성을 위한 설정
fake = Faker('ko_KR')

# 1. 상담 분야 정의 (이미지 내용 반영)
categories = [
    "공황장애", "우울증", "분노조절장애", "ADHD", "성 상담", 
    "대인관계", "진로상담", "위기 상담(자해/자살)", "가족 상담", "특수아 상담"
]

# 2. 데이터 생성을 위한 함수
def generate_sample_data(n=50):
    data = []
    for i in range(1, n + 1):
        category = random.choice(categories)
        # 분야별 가상 고민 문구 샘플
        complaints = {
            "공황장애": "사람 많은 곳에 가면 숨이 막히고 가슴이 뛰어요.",
            "우울증": "최근 아무것도 하기 싫고 무기력함이 지속됩니다.",
            "ADHD": "수업 시간에 집중하기가 너무 힘들고 자꾸 딴생각이 나요.",
            "진로상담": "내가 뭘 잘하는지 모르겠고 미래가 불안해요.",
            "대인관계": "친구들과 자꾸 오해가 생기고 어울리기가 힘듭니다."
        }
        
        data.append({
            "ID": f"STUDENT_{i:03d}",
            "이름": fake.name(),
            "상담분야": category,
            "고민내용": complaints.get(category, "상담이 필요한 상황입니다."),
            "신청일자": fake.date_between(start_date='-30d', end_date='today'),
            "만족도(예상)": random.randint(1, 5) # EDA 패턴 분석용
        })
    return pd.DataFrame(data)

# 3. 데이터 생성 및 CSV 저장
df_samples = generate_sample_data(50)
df_samples.to_csv("counseling_data.csv", index=False, encoding='utf-8-sig')

print(" 50개의 샘플 데이터가 'counseling_data.csv'로 저장되었습니다.")