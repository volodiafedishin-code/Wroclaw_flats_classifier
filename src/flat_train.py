import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report



df=pd.read_csv(r"C:\Users\volod\ml_engineer\ml_basics\flat_project\data\flats.csv")




X=df[['price/mounth','minutes_to_school','looks']]
y=df['rent']

X_train, X_test, y_train, y_test=train_test_split(X, y, test_size=0.3, random_state=42)

pipeline=Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler()),
    ('model', RandomForestClassifier(n_estimators=100, random_state=42))
])

pipeline.fit(X_train, y_train)

# 1. Дістаємо саму модель із кроку 'rf'
model = pipeline.named_steps['model']

# 2. Тепер беремо важливість
importances = model.feature_importances_

features = ['price_mounth', 'minutes_to_school', 'looks']

for name, val in zip(features, importances):
    print(f"{name}: {val:.4f}")
    
predictions = pipeline.predict(X_test)
print("Звіт про якість моделі:")
print(classification_report(y_test, predictions))

joblib.dump(pipeline, r"C:\Users\volod\ml_engineer\ml_basics\flat_project\models\flats.pkl")
print("\nМодель збережена як 'flats.pkl'. Роботу завершено! ✅")