import pandas as pd

# مسیر فایل CSV خود را وارد کنید
file_path = 'C:/Users/Bartar/OneDrive/Apps/Desktop/projects/drugs_medogram/drug/search_drug/management/commands/drugs.csv'

# خواندن فایل CSV
df = pd.read_csv(file_path)

# نمایش نام ستون‌ها برای بررسی
print(df.columns)