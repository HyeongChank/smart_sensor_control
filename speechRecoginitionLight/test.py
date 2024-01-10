import requests
import pandas as pd
from datetime import datetime, timedelta


# start_date_str = '20230101'
# end_date_str = '20231231'

# # 문자열을 날짜로 변환
# start_date = datetime.strptime(start_date_str, '%Y%m%d')
# end_date = datetime.strptime(end_date_str, '%Y%m%d')

# # 1일씩 증가하면서 날짜 생성
# current_date = start_date
# date_list = []

# while current_date <= end_date:
#     date_list.append(current_date.strftime('%Y%m%d'))
#     current_date += timedelta(days=1)


key = 'DaYD4HqMAnLfFMtrGVb5FDSGASJak3Wi'
searchdate = '20230105'
data = 'AP03'

url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey='+key+'&searchdate='+searchdate+'&data='+data

response = requests.get(url)
result = response.json()
rawdata = pd.DataFrame(result)
print(rawdata.columns)
print(rawdata.info())
print(rawdata)

# cmoney_list = []
# for i in date_list:
#     searchdate = str(i)
#     url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey='+key+'&searchdate='+searchdate+'&data='+data

#     response = requests.get(url)
#     result = response.json()
#     rawdata = pd.DataFrame(result)

#     if 'cur_nm' in rawdata.columns:

#         changemoney = rawdata.loc[rawdata['cur_nm'] == '미국 달러', 'ttb'].values
#         print(changemoney)
#         cmoney_list.append(changemoney)
#     else:
#         print('none')
#         cmoney_list.append('none')
# print(len(cmoney_list))
        


