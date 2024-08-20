import streamlit as st
import pandas as pd
import numpy as np
import json

def load_json(json_file):
    with open(json_file, 'r') as file:
        json_data = json.load(file)
    return json_data

data = load_json("TestSchoolData/testData.json")
df = pd.DataFrame.from_dict(data, orient='columns')
print(df)
st.title('Fabula Scoreboard')
#df = pd.read_csv("TestSchoolData/testData.csv", names=['Rank', 'School Name', 'Score'])

st.table(df)