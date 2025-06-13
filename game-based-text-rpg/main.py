from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")

# code reuse
def load_json(file_name):
    with open(os.path.join(DATA_DIR, file_name), "r") as file:
        return json.load(file)

@app.get("/")
def read_root():
    return {"message": "API ready"}

@app.get("/enemies")
def get_enemies():
    return load_json("enemies.json")

@app.get("/items")
def get_items():
    return load_json("items.json")

@app.get("/jobs")
def get_jobs():
    return load_json("jobs.json")
