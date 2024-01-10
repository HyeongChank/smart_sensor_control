import yfinance as yf

# KOSPI 지수 가져오기
kospi_data = yf.download('^KS11', start='2022-01-01', end='2022-12-31')

# KOSDAQ 지수 가져오기
kosdaq_data = yf.download('^KQ11', start='2022-01-01', end='2022-12-31')

# 결과 출력
print("KOSPI 데이터:")
print(kospi_data.head())
print(len(kospi_data))
# print("\nKOSDAQ 데이터:")
# print(kosdaq_data.head())
