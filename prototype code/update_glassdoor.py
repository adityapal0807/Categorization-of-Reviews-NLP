import pandas as pd

df = pd.read_csv('Glassdoor.csv')
date = []
status_comb=[]
for i in range(len(df)):
    info = str(df['author_info'][i]).split('-')
    date.append(info[0])
    status_comb.append(info[1])

df['Date'] = date

location = []
status=[]
for a in status_comb:
    item = str(a).split(' in ')
    try:
        status.append(item[0])
    except:
        status.append('None')
    try:
        location.append(item[1])
    except:
        location.append('None')
    

df['Location'] = location
df['Status'] = status


df.to_csv('Glassdoor_Updated.csv')