import pandas as pd
from sklearn.preprocessing import LabelEncoder

def engineer_features(df):
    # Convert 'City' to One-Hot Encoding
    df = pd.get_dummies(df, columns=['City'], drop_first=True)
    
    # 'Area/Locality' has too many unique values for One-Hot.
    # We use Label Encoding to turn them into unique integers.
    le = LabelEncoder()
    df['Area'] = le.fit_transform(df['Area'].astype(str))
    
    return df, le

# This script will be called during training.