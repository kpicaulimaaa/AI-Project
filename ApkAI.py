import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pickle

# Memuat dataset
data = pd.read_csv('Liverdiease.csv')

# Mengganti nilai missing pada kolom Albumin_and_Globulin_Ratio dengan median
data['Albumin_and_Globulin_Ratio'].fillna(data['Albumin_and_Globulin_Ratio'].median(), inplace=True)

# Mengganti nilai kategori pada kolom Gender
data['Gender'] = data['Gender'].apply(lambda x: 1 if x == 'Male' else 0)

# Memisahkan fitur dan target
X = data.drop('Dataset', axis=1)
y = data['Dataset'].apply(lambda x: 1 if x == 2 else 0) # 1: Liver Disease, 0: No Liver Disease

# Membagi data menjadi data latih dan data uji
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standarisasi data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Melatih model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Menyimpan model dan scaler dengan pickle
with open('liver_model.pkl', 'wb') as file:
    pickle.dump(model, file)
with open('scaler.pkl', 'wb') as file:
    pickle.dump(scaler, file)

