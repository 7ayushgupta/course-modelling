!pip install unidecode

def processColumns(df):

  df['locality.1']=df['locality.1'].fillna("None")
  import unidecode
  accented_string = df['locality.1'].unique()[1]
  unaccented_string = unidecode.unidecode(accented_string)
  # print(accented_string)

  locality_processed = []
  for locality in df['locality.1']:
    cleared_ = unidecode.unidecode(locality)
    cleared_ = cleared_.lower()
    locality_processed.append(cleared_)

  df['locality_processed']=locality_processed
  city_mapping = {
      "bangalore": "bengaluru",
      "bangalore rural": "bengaluru",
      "bombay byculla": "bombay",
      "mumbai suburban": "bombay",
      "lakhnau": "lucknow"
  }

  for city_string, corrected_city_string in city_mapping.items():
    df.loc[(df.locality_processed==city_string), 'locality_processed'] = corrected_city_string

  df['course_name'] = df['course_name'].astype(str)
  df= df.applymap(lambda s:s.lower() if type(s) == str else s)

  print(df.record_type.value_counts())
  #df['record_type'] = ((df.status == "converted") | (df.status == 1)).astype(int)
  print(df.record_type.value_counts())

  # features = ['course_name', 'gender','stream_processed','degree_processed','levels_processed','specialisations_processed', 'majors_processed', 'industry_processed', 'exp_years', 'last_years', 'vendor', 'utm_contract_c', 'utm_campaign', 'utm_source_c', 'status', 'status_detail', 'locality_processed', 'record_type']
  features = ['course_name', 'gender','stream_processed','degree_processed','levels_processed','specialisations_processed', 'majors_processed', 'industry_processed', 'exp_years', 'last_years','locality_processed', 'record_type']
  new_df = df[features]

  new_df['course_name'] = new_df['course_name'].replace('generic', 'missing')
  new_df['course_name'] = new_df['course_name'].replace('false', 'missing')

  new_df = new_df.fillna('missing')
  new_df = new_df.replace('None','missing')
  new_df = new_df.replace('none','missing')

  new_df = new_df[new_df.course_name!="missing"]

  return new_df

def processColumnsLocationsModified(df):
  df['locality.1']=df['data.primary.location.name'].fillna("None")
  import unidecode
  accented_string = df['locality.1'].unique()[1]
  unaccented_string = unidecode.unidecode(accented_string)
  # print(accented_string)

  locality_processed = []
  for locality in df['locality.1']:
    cleared_ = unidecode.unidecode(locality)
    cleared_ = cleared_.lower()
    cleared_ = cleared_.split(",")[0]
    locality_processed.append(cleared_)

  df['locality_processed']=locality_processed
  city_mapping = {
      "bangalore": "bengaluru",
      "bangalore rural": "bengaluru",
      "bombay byculla": "bombay",
      "mumbai suburban": "bombay",
      "lakhnau": "lucknow"
  }

  for city_string, corrected_city_string in city_mapping.items():
    df.loc[(df.locality_processed==city_string), 'locality_processed'] = corrected_city_string

  df['course_name'] = df['course_name'].astype(str)
  df= df.applymap(lambda s:s.lower() if type(s) == str else s)

  #print(df.record_type.value_counts())

  # features = ['course_name', 'gender','stream_processed','degree_processed','levels_processed','specialisations_processed', 'majors_processed', 'industry_processed', 'exp_years', 'last_years', 'vendor', 'utm_contract_c', 'utm_campaign', 'utm_source_c', 'status', 'status_detail', 'locality_processed', 'record_type']
  features = ['lead_id', 'course_name', 'gender','stream_processed','degree_processed','levels_processed','specialisations_processed', 'majors_processed', 'industry_processed', 'exp_years', 'last_years','locality_processed']#, 'record_type']
  new_df = df[features]

  new_df['course_name'] = new_df['course_name'].replace('generic', 'missing')
  new_df['course_name'] = new_df['course_name'].replace('false', 'missing')

  new_df = new_df.fillna('missing')
  new_df = new_df.replace('None','missing')
  new_df = new_df.replace('none','missing')

  # new_df = new_df[new_df.course_name!="missing"]

  return new_df


def processColumnsLocationsModified2(df):
  import unidecode
  df['locality_processed'] = df['locality_processed'].fillna("None")
  locality_processed = []
  for locality in df['locality_processed']:
    cleared_ = unidecode.unidecode(locality)
    cleared_ = cleared_.lower()
    cleared_ = cleared_.split(",")[0]
    locality_processed.append(cleared_)

  df['locality_processed']=locality_processed
  city_mapping = {
      "bangalore": "bengaluru",
      "bangalore rural": "bengaluru",
      "bombay byculla": "bombay",
      "mumbai suburban": "bombay",
      "lakhnau": "lucknow"
  }

  for city_string, corrected_city_string in city_mapping.items():
    df.loc[(df.locality_processed==city_string), 'locality_processed'] = corrected_city_string

  df['course_name'] = df['course_name'].astype(str)
  df= df.applymap(lambda s:s.lower() if type(s) == str else s)

  #print(df.record_type.value_counts())

  # features = ['course_name', 'gender','stream_processed','degree_processed','levels_processed','specialisations_processed', 'majors_processed', 'industry_processed', 'exp_years', 'last_years', 'vendor', 'utm_contract_c', 'utm_campaign', 'utm_source_c', 'status', 'status_detail', 'locality_processed', 'record_type']
  #features = ['lead_id', 'course_name', 'gender','stream_processed','degree_processed','levels_processed','specialisations_processed', 'majors_processed', 'industry_processed', 'exp_years', 'last_years','locality_processed']#, 'record_type']
  #new_df = df[features]
  new_df = df

  new_df['course_name'] = new_df['course_name'].replace('generic', 'missing')
  new_df['course_name'] = new_df['course_name'].replace('false', 'missing')

  new_df = new_df.fillna('missing')
  new_df = new_df.replace('None','missing')
  new_df = new_df.replace('none','missing')

  # new_df = new_df[new_df.course_name!="missing"]

  return new_df