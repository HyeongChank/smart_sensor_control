import pandas as pd
import csv

# Define the file path

data = pd.read_excel("C:/Users/jsk38/raspberrypi/data/주유소_제품별_평균판매가격.xlsx")
# Read the CSV file into a pandas DataFrame

# 헤더 출력
print(data['price'])

