import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest

# 범주형 데이터를 원-핫 인코딩으로 변환합니다.
df = pd.read_csv('network_log_data.csv')
df = pd.get_dummies(df, columns=['protocol_type', 'service', 'flag'])
# 'label' 열이 타겟 값입니다.
# 'normal.' 값은 정상을, 그 외의 값은 비정상을 나타냅니다.
df['target'] = (df['label'] == 'normal.').astype(int)

# 타겟 값을 제외한 나머지를 피처로 사용합니다.
features = df.drop(['target', 'label'], axis=1)
target = df['target']

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

# Isolation Forest는 이상치를 -1, 정상치를 1로 표시하므로 이를 우리의 타겟 값과 동일하게 맞춰줍니다.
pred_test = (pred_test == 1).astype(int)

# 이상을 감지한 결과를 보여줍니다.
print(pred_test)
