import pandas as pd
import datetime
import joblib


def fetch(district,mandal):
    df=pd.read_csv("after_combining.csv")
    month=int(datetime.datetime.now().strftime("%m"))
    for i in range(len(df)):
        if(df.iloc[i].mandal==mandal and df.iloc[i].district==district and df.iloc[i].month==month):
            return(df.iloc[i].to_dict())
    return None

def predictor(data):
    ran_model=joblib.load("crop_model.pkl")
    des_model=joblib.load("old_crop_model.pkl")
    return([*des_model.predict([data]),*ran_model.predict([data])])