import pandas as pd
import numpy as np

r = pd.read_csv('../static_data/predicted_industries_classification.csv')
r = r.set_index('Unnamed: 0')
prettify_create_mapping = {}
for i in r.index:
    prettify_create_mapping[i] = []
    for enum, j in enumerate(r.columns):
        if enum == 1:
            continue
        val = r.loc[str(i), j]
        if not pd.isnull(val):
            prettify_create_mapping[i].append(val)
workers_mapping = prettify_create_mapping

def clean_string(string):
    string = string.replace("&", "")
    string = string.replace("/", " ")
    return string

def buildMajors(industry_raw):
    industry_ = "None"
    industry_raw = clean_string(industry_raw)
    for key, value in workers_mapping.items():
        if industry_raw in value:
            industry_ = key
            break
    # if (industry_ == "None" and industry_raw != "None"):
    #     print(industry_raw)
    return industry_