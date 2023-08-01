import pandas as pd
import numpy as np

# 데이터 샘플 수
num_samples = 1000

# 'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes' 피처 생성
duration = np.random.choice(60, num_samples)  # 연결 기간은 0~59초 사이
protocol_type = np.random.choice(['tcp', 'udp', 'icmp'], num_samples)
service = np.random.choice(['http', 'ftp', 'ssh'], num_samples)
flag = np.random.choice(['SF', 'S0', 'S1'], num_samples)
src_bytes = np.random.choice(1000, num_samples)  # 소스에서 대상 호스트로 보낸 바이트
dst_bytes = np.random.choice(1000, num_samples)  # 대상 호스트에서 소스로 보낸 바이트

# "attack." 연결의 src_bytes는 크게 설정
src_bytes[-100:] = np.random.choice(1000, 100) + 10000  # 마지막 100개 샘플은 공격

# 데이터 프레임 생성
df = pd.DataFrame({
    'duration': duration,
    'protocol_type': protocol_type,
    'service': service,
    'flag': flag,
    'src_bytes': src_bytes,
    'dst_bytes': dst_bytes,
    'label': 'normal.'
})

# 마지막 100개 샘플의 레이블을 'attack.'으로 설정
df.loc[df.index[-100:], 'label'] = 'attack.'

# 데이터 프레임 출력
print(df)
df.to_csv("network_log_data.csv", index=False)
