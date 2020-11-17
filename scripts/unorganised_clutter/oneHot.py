def oneHotValue(data_df):
  data_df['last_years']= data_df['last_years'].replace('missing', np.nan)
  data_df['exp_years']= data_df['exp_years'].replace('missing', np.nan)
  data_df['last_years']=data_df['last_years'].astype(float)
  data_df['exp_years']=data_df['exp_years'].astype(float)

  df = pd.concat(
      [pd.get_dummies(data_df['gender'], prefix='gender'),
      pd.get_dummies(data_df['stream_processed'], prefix='stream_processed'),
      pd.get_dummies(data_df['degree_processed'], prefix='degree_processed'),
      pd.get_dummies(data_df['levels_processed'], prefix='levels_processed'),
      pd.get_dummies(data_df['specialisations_processed'], prefix='specialisations_processed'),
      pd.get_dummies(data_df['industry_processed'], prefix='industry_processed'),
      pd.get_dummies(data_df['course_name'], prefix='course_name'),
      pd.get_dummies(data_df['majors_processed'], prefix='majors_processed'),
      ],axis=1)

  df['record_type'] = data_df['record_type']
  df['last_years'] = data_df['last_years'].fillna(data_df['last_years'].mean())
  df['exp_years'] = data_df['exp_years'].fillna(data_df['exp_years'].mean())

  return df