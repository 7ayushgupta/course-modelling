import pandas as pd
!pip install unidecode
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm_notebook
import datetime
import ast
import json

 def func_experience(experience_json):
    eval_dict = json.loads(experience_json)
    start_dates = []
    last_job_date = None

    for iter in eval_dict:
        if iter['start_date'] is not None:
            start_date_ = pd.to_datetime(iter['start_date'])
            start_dates.append(start_date_)
        if (iter['is_primary'] == True):
            last_job_date = pd.to_datetime(iter['start_date'])
    if len(start_dates) == 0:
        start_date = None
    else:
        start_date = min(start_dates)
    # print(start_date, last_job_date, eval_dict)
    return start_date, last_job_date


 def func_locality(locality_json):
    eval_dict = json.loads(locality_json)
    geo=None
    locality=None
    for iter in eval_dict:
      if (iter['is_primary'] ==  True):
        geo=iter['geo']
        locality=iter['locality']
    return locality, geo


 def func_education(education_json):
      try:
        eval_dict = json.loads(education_json,strict=False)
        majors = []
        minors = []
        degrees = []
        for iter in eval_dict:
          majors.extend(iter['majors'])
          minors.extend(iter['minors'])
          degrees.extend(iter['degrees'])
        return majors, minors, degrees
      except:
        return [], [], []