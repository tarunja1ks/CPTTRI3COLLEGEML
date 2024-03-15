import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib
class datamodel:
    
    def __init__(self):
        self.model = joblib.load("College_prediction.pkl")
    def readfile(self):
        self.data=pd.read_csv("student_admission_dataset.csv")
        print(self.data.head())
    def preprocessing(self):
        self.X=self.data[['GPA','SAT_Score','Extracurricular_Activities']]
        self.Y=self.data['Admission_Status']
    def train(self):
        self.model=LogisticRegression()
        self.model.fit(self.X,self.Y)
    def predict(self, GPA, SAT_SCORE, EXTRACIRICULAR):
        return self.model.predict([[GPA, SAT_SCORE, EXTRACIRICULAR]])[0]
    
    def exportmodel(self):
        joblib.dump(self.model,"College_prediction.pkl")
    
    
    
    
Model=datamodel()
print(Model.predict(4.0,1600,8))
