import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# 1. 데이터 로드 (Stage 1에서 만든 데이터)
df = pd.read_csv("counseling_data.csv")

# 2. AI 모델 설계 (텍스트 벡터화 + 분류 알고리즘)
# TF-IDF: 단어의 중요도를 계산하여 숫자로 변환
# Naive Bayes: 텍스트 분류에 효율적인 알고리즘
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# 3. 모델 학습 (고민내용 -> 상담분야 패턴 학습)
model.fit(df['고민내용'], df['상담분야'])

# 4. 모델 테스트 함수
def predict_counseling_category(user_text):
    prediction = model.predict([user_text])
    return prediction[0]

# 테스트 실행
test_text = "요즘 친구들과 자꾸 싸우게 되고 혼자 있고 싶어요."
result = predict_counseling_category(test_text)
print(f"입력 문장: {test_text}")
print(f"AI 예측 분류: {result}")