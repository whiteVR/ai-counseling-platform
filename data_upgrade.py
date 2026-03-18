import pandas as pd
import random
from faker import Faker

fake = Faker('ko_KR')

# 1. 분야별 핵심 가중치 키워드 정의
category_keywords = {
    "공황장애": ["숨 가쁨", "호흡 곤란", "심장 두근거림", "죽을 것 같은 공포"],
    "우울증": ["무기력", "눈물", "잠만 자고 싶다", "의욕 상실"],
    "ADHD": ["집중 안 됨", "산만함", "물건 분실", "가만히 있지 못함"],
    "진로상담": ["꿈이 없다", "적성", "취업 걱정", "미래 불안"],
    "대인관계": ["친구와 다툼", "왕따", "소외감", "눈치 보임"]
}

categories = list(category_keywords.keys())

def generate_augmented_data(n=500):
    data = []
    for i in range(n):
        category = random.choice(categories)
        keywords = category_keywords[category]
        
        # 데이터 증강 핵심: 핵심 키워드를 문장에 포함시켜 가중치 학습 유도
        main_keyword = random.choice(keywords)
        context = [
            f"요즘 {main_keyword} 때문에 너무 힘들어요.",
            f"자꾸 {main_keyword} 증상이 나타나서 일상생활이 어렵습니다.",
            f"{main_keyword} 현상이 심해지고 있는데 어떻게 해야 하나요?",
            f"어제도 {main_keyword} 현상 때문에 한참을 고생했습니다."
        ]
        
        data.append({
            "ID": f"AUG_{i:03d}",
            "상담분야": category,
            "고민내용": random.choice(context)
        })
    return pd.DataFrame(data)

# 500개 데이터 생성 및 저장
df_500 = generate_augmented_data(500)
df_500.to_csv("counseling_data_500.csv", index=False, encoding='utf-8-sig')
print(" 500개의 증강 데이터가 'counseling_data_500.csv'로 저장되었습니다.")