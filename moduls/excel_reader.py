import pandas as pd

path = r"C:\Users\onlyn\Desktop\DATA\Monthly Destination Report - Sample.xls"
df = pd.read_excel(path)
print(df)
