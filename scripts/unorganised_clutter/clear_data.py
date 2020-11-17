import pandas as pd
!pip install unidecode
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm_notebook
import datetime
import ast
import json
from Functions_for_clearData import func_experience, func_locality, func_education

def clearData(new_data):
##############################EDUCATION##########################################
  majors = []
  minors = []
  degrees = []

  for index, row in tqdm_notebook(new_data.iterrows()):
    major, minor, degree = func_education(row['data.education'])
    majors.append(major)
    minors.append(minor)
    degrees.append(degree)

  new_data['majors_raw']=majors
  new_data['minors_raw']=minors
  new_data['degrees_raw']=degrees

################################EXPERIENCE##########################################
  exp_years = []
  last_years = []

  reference_date = pd.to_datetime(datetime.date(2020,1,1))
  for index, row in tqdm_notebook(new_data.iterrows()):
    try:
      start_date, last_job_date = func_experience(row['data.experience'])
    except:
      exp_years.append("None")
      last_years.append("None")
      continue

    if (start_date is not None):
      exp_years_ = (float)((reference_date - start_date).days/365.)
    else:
      exp_years_ = "None"
    if (last_job_date is not None):
      last_years_ = ((float)((reference_date - last_job_date).days/365.))
    else:
      last_years_ = "None"
    
    exp_years.append(exp_years_)
    last_years.append(last_years_)

  new_data['exp_years'] = exp_years
  new_data['last_years'] = last_years

#################################LOCALITY#############################################
  localities = []
  geos = []

  for index, row in tqdm_notebook(new_data.iterrows()):
    try:
      locality, geo = func_locality(row['data.locations'])
      print(locality, geo)
    except:
      locality=None
      geo=None
    localities.append(locality)
    geos.append(geo)

  new_data['locality_raw'] = localities
  new_data['geo_raw'] = geos

###############################EXPERIENCE LEVEL#################################################
  level_mapping =  {
    "TM": ["director", "partner", "cxo", "owner"],
    "LM": ["manager", "senior"],
    "MM": ["vp"],
    "Worker": ["entry"],
    "Others": ["training", "unpaid"],}

  levels_raw = []
  unsettled_levels = []
  for x in new_data['data.primary.job.title.levels']:
    # print(x)
    if pd.isnull(x):
      levels_raw.append("None")
      continue
    # x = ast.literal_eval(x)
    if len(x)==0:
      levels_raw.append("None")
      continue

    level_ = None
    for key in ['TM', 'MM', 'LM', 'Worker', 'Others']:
      for val in level_mapping[key]:
        if x.find(val)>-1:
          level_ = key
          break
      if level_ != None:
        break
    
    if (level_!=None):
      levels_raw.append(level_)
    else:
      levels_raw.append("None")
      unsettled_levels.append(x)

  new_data['levels_raw'] = levels_raw

#############################################################################
  import ast
  majors = []
  minors = []
  degrees = []
  for index, row in new_data.iterrows():
    eval_majors = ast.literal_eval(str(row['majors_raw']))
    eval_minors = ast.literal_eval(str(row['minors_raw']))
    eval_degrees = ast.literal_eval(str(row['degrees_raw']))
    major = eval_majors[0] if (len(eval_majors)>0) else None
    minor = eval_minors[0] if (len(eval_minors)>0) else None
    degree = eval_degrees[0] if (len(eval_degrees)>0) else None

    majors.append(major)
    minors.append(minor)
    degrees.append(degree)

  new_data['majors'] = majors
  new_data['minors'] = minors
  new_data['degrees'] = degrees

  new_data = new_data.rename({
  '_id': 'id',
  'data.gender': 'gender',
  'data.primary.location.locality':'locality.1',
  'majors':'major',
  'minors':'minor',
  'geo_raw':'geo',
  'degrees':'degree',
  'data.primary.job.title.name': 'job_title',
  'levels_raw': 'level_raw',
  'data.primary.job.company.industry':'industry',
  'created_at':'converted_date',
  }, axis=1)

  return new_data