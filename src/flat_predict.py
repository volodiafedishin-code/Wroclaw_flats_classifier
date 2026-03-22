import joblib

model = joblib.load(r"C:\Users\volod\ml_engineer\ml_basics\flat_project\models\flats.pkl")

price_mounth=int(input('Price: '))
minutes_score=int(input('minutes to school: '))
looks=int(input('looks: '))


X =([[price_mounth, minutes_score, looks]])
print(X)
result=model.predict(X)[0]

print('result is: ',result)