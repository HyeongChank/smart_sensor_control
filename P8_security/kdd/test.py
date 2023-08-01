import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest

# 데이터를 로드합니다.
data = pd.read_csv('kddcup.data_10_percent.gz', header=None)

# 'label' 열이 타겟 값입니다.
# 'normal.' 값은 정상을, 그 외의 값은 비정상을 나타냅니다.
data['target'] = (data[41] == 'normal.').astype(int)

# 타겟 값을 제외한 나머지를 피처로 사용합니다.
features = data.drop(['target', 41], axis=1)
target = data['target']

# 범주형 데이터를 원-핫 인코딩으로 변환합니다.
features = pd.get_dummies(features)

# 모든 특성 이름을 문자열로 변환합니다.
features.columns = features.columns.astype(str)

# 데이터를 학습 세트와 테스트 세트로 나눕니다.
features_train, features_test, target_train, target_test = train_test_split(
    features, target, test_size=0.2, random_state=42)

# Isolation Forest 모델을 생성하고 학습합니다.
model = IsolationForest(contamination=0.2)
model.fit(features_train)

# 테스트 세트에서 이상을 감지합니다.
pred_test = model.predict(features_test)

# 이상을 감지한 결과를 보여줍니다.
print(pred_test)
