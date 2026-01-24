import pandas as pd 

df = pd.read_csv("../data/Bangalore.csv")
print(df.head())

print(df.info())
print(df.isnull().sum())

print(df.describe())