import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

#   geting the data from data/master where all cities data merged
df = pd.read_csv('data/master_data.csv')

#  removing the rows which have empty values
df.dropna(inplace=True)

# Now One-Hot Encoding, with this i will divied the cities and location in 0,1 (False,True)
df_enco = df.get_dummies(df, columns=["City", "Location"])

#  Now seper the price for pred inX,y features and target
X = df_enco.drop("Price", axis = 1)     #Features
y = df_enco["Price"]                    #Target

#  Now Train_test data with spliting traindata in 80% and testing for 20%
