import yfinance as yf
import pandas as pd
# KOSPI 지수 가져오기
kospi_data = yf.download('^KS11', start='2022-01-01', end='2022-12-31')

# KOSDAQ 지수 가져오기
kosdaq_data = yf.download('^KQ11', start='2022-01-01', end='2022-12-31')

df = pd.DataFrame(kospi_data)
df2 = pd.DataFrame(kosdaq_data)
### index열인 date를 포함하여 open 열을 추출 ###
df_subset = df[['Open']].reset_index()
df_subset2 = df2[['Open']].reset_index()
# 'Open' 열의 이름을 변경
df_subset.rename(columns={'Open': 'kospi_Open'}, inplace=True)
df_subset2.rename(columns={'Open': 'kosdaq_Open'}, inplace=True)

df_subset['Date'] = pd.to_datetime(df_subset['Date'])

### 'Date' 열을 원하는 날짜 형식으로 포맷팅 ###
df_subset['Date'] = df_subset['Date'].dt.strftime('%Y%m%d')
df_subset['kosdaq'] = df_subset2['kosdaq_Open']
# 엑셀로 저장
excel_filename = 'data/kospi_open_data.xlsx'
df_subset.to_excel(excel_filename, index=False)
