import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('data/master_data.csv')

# 1. Check Price Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['Price'], bins=50, kde=True)
plt.title('Distribution of House Prices')
plt.show()

# 2. Check Area vs Price
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Area', y='Price', hue='City', alpha=0.5)
plt.title('Area vs Price across Cities')
plt.show()