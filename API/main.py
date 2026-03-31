from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# Charger les données
df = pd.read_csv(r"C:/Users/PC/DATA/final/data_final.csv")

@app.get("/")
def home():
    return {"message": "API Pollution ATMO"}

@app.get("/data")
def get_data():
    return df.head(100).to_dict(orient="records")

@app.get("/station/{code_site}")
def get_by_station(code_site: str):
    result = df[df["code site"] == code_site]
    return result.to_dict(orient="records")

@app.get("/date/")
def get_by_date(date: str):
    result = df[df["date"] == date]
    return result.to_dict(orient="records")

@app.get("/atmo/")
def get_by_atmo(level: int):
    result = df[df["ATMO"] == level]
    return result.to_dict(orient="records")

@app.get("/date/")
def get_by_date(date: str):
    result = df[df["date"] == date]
    return result.to_dict(orient="records")