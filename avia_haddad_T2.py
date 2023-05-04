#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import re
from datetime import datetime,timedelta
import matplotlib.pyplot as plt


# קריאת קובץ הנתונים 

# In[2]:


path = "C:\\Users\\אביה חדאד\\Desktop\\תואר ראשון\\שנה ג\\כרייה וניתוח נתונים מתקדם פייתון\\מטלות\\מטלה 2\\"
filename = "matala2_cosmetics_2019-Nov.csv"

datafile =  path + filename
data = pd.read_csv(datafile)


#   ###                                                                             סעיף 1

# In[3]:


data= data.sort_values(["user_id", "user_session","event_type"])
data['event_time'] = pd.to_datetime(data['event_time'])
data['duration_to_next_event'] = 0  
data['duration_to_next_event'] = abs((data['event_time'].shift(-1) - data['event_time']).dt.total_seconds().fillna(0))

data.head()



# ### סעיף 2 

# In[4]:


data['event_time'] = pd.to_datetime(data['event_time'])
data = data.sort_values(['user_id', 'event_time'])
data['diff_time'] = data.groupby('user_id')['event_time'].diff()
true_false = data['diff_time'] > timedelta(days=5)
diff_by_userid = true_false.groupby(data['user_id']).cumsum()
data['diff_days'] = diff_by_userid
data['funnel_number'] = data['diff_days'] + 1
data = data.drop(columns=['diff_time', 'diff_days'])
data


# ### סעיף 3

# In[5]:



data['identical_session'] = np.where(data['user_session'].shift() == data['user_session'],0,1)
data['index_in_funnel'] = data.groupby(['user_id','funnel_number'])['identical_session'].cumsum()
data  = data.drop(['identical_session'], axis=1)


# In[6]:


data.head()


# ### סעיף 4 

# In[7]:


data['price'] = data['price'].astype(str)
data['price'] = data['price'].str.extract('(\d+\.\d+)').astype(float)
data


# ### סעיף 5 

# In[8]:


data['event_type'].unique()


# In[9]:


import matplotlib.pyplot as plt

event_type_counts = data['event_type'].value_counts()
plt.bar(event_type_counts.index, event_type_counts.values)
plt.xlabel('Event Type')
plt.ylabel('Number of Occurrences')
plt.title('Event Type Counts')
plt.show()


# ### סעיף 6 

# In[10]:


data.sort_values(by=['event_time'],inplace = True)
data['list_of_view'] = data.apply(lambda row: row['product_id'] if row['event_type'] == 'view' else None, axis=1)
data['list_of_added_to_cart'] = data.apply(lambda row: row['product_id'] if row['event_type'] == 'cart' else None, axis=1)
data['list_of_purchased'] = data.apply(lambda row: row['product_id'] if row['event_type'] == 'purchase' else None, axis=1)
data['events_per_visit'] = data.groupby(['user_id', 'user_session'])['event_type'].transform('count')
session_duration = data[['user_session', 'duration_to_next_event']].groupby('user_session').sum()
session_duration = session_duration.rename(columns={'duration_to_next_event': 'session_duration'})
data = data.merge(session_duration, on='user_session', how='left')

session_data = data.groupby(['user_id', 'user_session','funnel_number','index_in_funnel','events_per_visit','session_duration']).agg({'list_of_view': lambda x: list(x.dropna()),'list_of_added_to_cart': lambda x: list(x.dropna()),'list_of_purchased': lambda x: list(x.dropna()),}).reset_index()

session_data


# In[ ]:




