import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib
class datamodel:
    
    def __init__(self): # Loading in the model file(this includes all weights after training)
        self.model = joblib.load("College_prediction.pkl")
    def readfile(self):
        self.data=pd.read_csv("student_admission_dataset.csv")
        print(self.data.head())
    def preprocessing(self):# this is loading in the file stuff into X and Y
        self.X=self.data[['GPA','SAT_Score','Extracurricular_Activities']]
        self.Y=self.data['Admission_Status']
    def train(self): # this is actually trianing the model
        self.model=LogisticRegression()
        self.model.fit(self.X,self.Y)
    def predict(self, GPA, SAT_SCORE, EXTRACIRICULAR): # this is prediciton function
        return self.model.predict([[GPA, SAT_SCORE, EXTRACIRICULAR]])[0]
    
    def exportmodel(self): #after trianing we have to export the file again
        joblib.dump(self.model,"College_prediction.pkl")
    
    def create(self, new_data):
        self.data = self.data.append(new_data, ignore_index=True)
        
    def read(self):
        return self.data
    
    def update(self, index, updated_data):
        self.data.loc[index] = updated_data
        
    def delete(self, index):
        self.data.drop(index, inplace=True)
    
    
Model=datamodel()# sample class thing
Model.exportmodel()
print(Model.predict(4.0,1600,8))# sample Prediction
