import pandas as pd
import numpy as np

from joblib import load
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import svm

import streamlit as st

class Iajob():

    def __init__(self,arr_input):
        self.arr_input = arr_input
        self.model_f1 = load('Model/gbc_f1.joblib')
        self.model_f2 = load('Model/gbc_ph2.joblib')
        self.model_f3 = load('Model/svr_f3.joblib')
        self.ph1_succes = True
        self.ph2_succes = True
        self.probas_disp_f1 = 0.0
        self.probas_disp_f2 = 0.0
        self.res = 0


    def predict_job(self):

        df = pd.DataFrame(self.arr_input)

        ## call pipelines
        pred_f1 = self.model_f1.predict(df)
        try:
            proba_pred_f1 = self.model_f1.predict_proba(df)
        
            if pred_f1[0] == 0:
                self.ph1_succes = False
                self.probas_disp_f1 = round(proba_pred_f1[0][0]*100,2)
                print(self.ph1_succes)
                print("Confiance : ", self.probas_disp_f1, " %")
            else:
                self.ph1_succes = True
                self.probas_disp_f1 = round(proba_pred_f1[0][1]*100,2)
                print(self.ph1_succes)
                print("Confiance : ", self.probas_disp_f1, " %")
        except Exception as e:
            print(e)
        
        if pred_f1 != 0:
            
            pred_f2 = self.model_f2.predict(df)
            proba_pred_f2 = self.model_f2.predict_proba(df)
            
            if pred_f2[0] == 0:
                self.ph2_succes = False
                self.probas_disp_f2 = round(proba_pred_f2[0][0]*100,2)
                print(self.ph2_succes)
                print("Confiance : ", self.probas_disp_f2, " %")
            else :
                self.ph2_succes = True
                self.probas_disp_f2 = round(proba_pred_f2[0][1]*100,2)
                print(self.ph2_succes)
                print("Confiance : ", self.probas_disp_f2, " %")

            self.res = int(np.exp(self.model_f3.predict(df)))
            print("Esitimation du nombre de retour : ", self.res)

    def display_on_app(self):
        if self.ph1_succes :
            return self.ph1_succes, self.probas_disp_f1, self.ph2_succes,self.probas_disp_f2, self.res
        else :
            return self.ph1_succes, self.probas_disp_f1
      
