import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import os  

#   geting the data from data/master where all cities data merged
df = pd.read_csv('data/master_data.csv')

#  removing the rows which have empty values
df.dropna(inplace=True)

# 1. Remove "Impossible" Houses
# A room should be at least 300 sq.ft. If not, it's likely an error.
df = df[df['Area'] / df['No. of Bedrooms'] > 300]

# 2. Filter out very rare BHKs
# If a BHK type has less than 10 houses, it's better to remove it 
# so it doesn't confuse the AI.
bhk_counts = df['No. of Bedrooms'].value_counts()
valid_bhk = bhk_counts[bhk_counts > 10].index
df = df[df['No. of Bedrooms'].isin(valid_bhk)]

# Now One-Hot Encoding, with this i will divied the cities and location in 0,1 (False,True)
df_enco = pd.get_dummies(df, columns=["City", "Location"])

#  Now seper the price for pred inX,y features and target
X = df_enco.drop("Price", axis = 1)     #Features
y = df_enco["Price"]                    #Target

#  Now Train_test data with spliting traindata in 80% and testing for 20%
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size= 0.2, random_state=42)

# Initialize the Model here n_estimators=100 means my model are going to use 100 Decision Trees (agents) for getting a desicison 
model = RandomForestRegressor(n_estimators=100, random_state=42)

# here my model actualy learn the data and get train
model.fit(X_train,y_train)

#  now the time to get accuracy 
accuracy = model.score(X_test, y_test)

perce = round((accuracy*100),2) # this will give R^2 score 

# Now the time t save the result:
joblib.dump(model,"models/house_model.pkl")
joblib.dump(X.columns,"models/model_columns.pkl")