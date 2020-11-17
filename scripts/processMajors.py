import pandas as pd
import numpy as np

r = pd.read_csv('../static_data/majors_mapping.csv')
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
majors_mapping = prettify_create_mapping

def buildMajors(major_raw):
    major_ = "None"
    if major_raw == "None":
        major_ = "None"
    else:
        for major_group, val in majors_mapping.items():
            if major_raw in val:
                major_ = major_group
                break
    return major_