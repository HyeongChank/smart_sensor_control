from flask import Flask, request, jsonify
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    new_log = pd.DataFrame(data, index=[0])

    # 원-핫 인코딩 수행
    new_log = pd.get_dummies(new_log, columns=['protocol_type', 'service', 'flag'])
    # 학습 데이터에 있는 모든 범주형 변수에 대해 원-핫 인코딩된 열이 존재하도록 함
    for col in features_train.columns:
        if col not in new_log.columns:
            new_log[col] = 0

    # 학습 데이터의 열 순서와 동일하게 맞춤
    new_log = new_log[features_train.columns]
    pred_new_log = model.predict(new_log)
    if pred_new_log[0] == -1:
        return jsonify('Anomaly')
    else:
        return jsonify('Normal')


if __name__ == '__main__':

    df = pd.read_csv('network_log_data.csv')
    df = pd.get_dummies(df, columns=['protocol_type', 'service', 'flag'])
    # 'label' 열이 타겟 값
    df['target'] = (df['label'] == 'normal.').astype(int)
    print(df)
    # 타겟 값을 제외한 나머지를 피처로 사용
    features = df.drop(['target', 'label'], axis=1)
    target = df['target']
    # 모든 특성 이름을 문자열로 변환
    features.columns = features.columns.astype(str)
    features_train, features_test, target_train, target_test = train_test_split(
        features, target, test_size=0.2, random_state=42)
    model = IsolationForest(contamination=0.2)
    model.fit(features_train)

    app.run(port=5000, debug=True)
