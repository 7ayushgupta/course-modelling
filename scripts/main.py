from process_data import processData
from clear_data import clearData
from oneHot import oneHotValue
from processColumns import processColumns, processColumnsLocationsModified, processColumnsLocationsModified2


y = pd.read_csv("/content/drive/My Drive/Revamp/Data/features_created_.csv")
# print(y.shape)
# print(y.head())

a = pd.read_csv('/content/drive/My Drive/Revamp/Data/conversionDates/Leads_April_September_datapresent.csv')
# print(a.shape)
# print(a.head())

b = pd.read_csv('/content/drive/My Drive/Revamp/Data/conversionDates/Leads_April_September_datamissing.csv')
# print(b.shape)
# print(b.head())

c = pd.concat([a,b], axis=0)
c = c.rename({'data.primary.industry':'industry'}, axis=1)
# print(c.head())

a3 = processColumnsLocationsModified(processData(clearData(c)))
# print(a3.shape)
# a3.head()

a3['record_type']=1
# print(a3.columns)
# print(y.columns)

timemerged_data = pd.concat([y, a3], axis=0)
print(timemerged_data.shape)
del y, a3

timemerged_data.record_type.value_counts()

x = pd.read_csv("/content/drive/My Drive/Revamp/Data/conversionDates/leads.csv", header=None)
x.columns = ['lead_id', 'converted_date', 'status', 'disposition']
# x.head()
#
# print(x.shape)
# print(x.converted_date.value_counts())

merged_df = pd.merge(timemerged_data, x, how='left', on='lead_id')
# merged_df.head()

merged_df.to_csv("completeData.csv")

merged_df['locality_processed'] = merged_df['locality_processed'].fillna(merged_df['locality.1'])
merged_df = merged_df.drop(['Unnamed: 0',	'Unnamed: 0.1', 'id'], axis=1, errors="ignore")
merged_df = merged_df.drop(['locality.1', 'converted_date_x', 'status_x',  'disposition_x', 'count', ], axis=1, errors="ignore")
# merged_df.head()

# merged_df.course_name.value_counts()

merged_df = processColumnsLocationsModified2(merged_df)
# merged_df.head()

merged_df = merged_df.rename({
    'converted_date_y': 'converted_date',
    'status_y':'status',
    'disposition':'disposition',
},axis=1)

merged_df.to_csv("completeData.csv")
merged_df = merged_df[(merged_df['converted_date']!='missing') & (merged_df['converted_date']!='0000-00-00 00:00:00')]
# print(merged_df.shape)
converted_dates_processed = []
unsettled_dates = []
for x in merged_df['converted_date']:
  processed_date = None
  try:
    try:
      processed_date = pd.to_datetime(x)
    except:
      processed_date = pd.to_datetime(str(x)[2:])
  except:
    unsettled_dates.append(x)
  converted_dates_processed.append(processed_date)
# print(unsettled_dates)

import numpy as np
# print(np.unique(unsettled_dates))
# print(len(unsettled_dates))
# print(pd.Series(unsettled_dates).value_counts())

merged_df['converted_date']=pd.to_datetime(converted_dates_processed)

merged_df = pd.read_csv("completeDataCleaned.csv")

merged_df['converted_date'] = pd.to_datetime(merged_df['converted_date'])
merged_df['converted_year'] = merged_df['converted_date'].dt.strftime('%Y')
merged_df['converted_year'].value_counts()

merged_df = merged_df[(merged_df['converted_date']>=pd.to_datetime("2015-01-01")) & (merged_df['converted_date']<=pd.to_datetime("2020-12-31"))]
# merged_df.head()

merged_df.to_csv("completeDataCleaned.csv")
merged_df = pd.read_csv("completeDataCleaned.csv")
# print(merged_df.shape)
merged_df = merged_df[merged_df.course_name!="missing"]
# print(merged_df.shape)
# merged_df.columns
# merged_df.record_type.value_counts()
# merged_df.status.value_counts()
merged_df = merged_df[(merged_df['status']=="dead") | (merged_df['status']=="converted")]
merged_df['record_type'] = (merged_df['status']=="converted").astype(int)

merged_df = merged_df.drop(['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1', 'Unnamed: 0.1.1.1', 'level_raw',
       'modified_id', 'course_category', 'business_type', 'industry', 'job_title', 'minor', 'major', 'geo', 'degree','status_detail', 'vendor', 'utm_campaign', 'utm_term_c',
       'utm_source_c', 'utm_contract_c', 'disposition_reason','status', 'converted_year', 'disposition_y', 'job_title_cleaned',
 ], axis=1, errors="ignore")

merged_df.to_csv("completeDataProcessed.csv")
# merged_df['record_type'].value_counts()