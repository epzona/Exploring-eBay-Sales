#!/usr/bin/env python
# coding: utf-8

# # Clean and Analyze Employee exit survey
# In this project, I will analyze the data to explore the following:
# -Are employees who only worked for the institutes for a short period of time resigning due to some kind of dissatisfaction? What about employees who have been there longer?
# -Are younger employees resigning due to some kind of dissatisfaction? What about older employees?

# In[ ]:





# In[73]:


import pandas as pd
import numpy as np
dete_survey=pd.read_csv('dete_survey.csv')
tafe_survey=pd.read_csv('tafe_survey.csv')


# In[74]:


#dete_survey.info()
#dete_survey.head()
#tafe_survey.info()
#tafe_survey.head()
#dete_survey['Business Unit'].value_counts()
#tafe_survey['Contributing Factors. Interpersonal Conflict'].value_counts()


# Looking at the dete_survey, many of the responses are boolean.
# With the tafe_survey,there are many NaN values and long string free response answers.

# In[75]:


#Reading the DETE survey again to read 'Not stated' values as NaN
dete_survey=pd.read_csv('dete_survey.csv',na_values='Not Stated')

#print(tafe_survey.columns[17:66])
#drop useless columns
dete_survey_updated=dete_survey.drop(dete_survey.columns[28:49],axis=1)
tafe_survey_updated=tafe_survey.drop(tafe_survey.columns[17:66],axis=1)


# In[76]:


#renaming the DETE survey columns to all lowercase, replace spaces with underscores, and remove whitespace
dete_survey_updated.columns=dete_survey_updated.columns.str.lower().str.replace(' ','_').str.strip()
#dete_survey_updated.columns

new_colnames={'Record ID':'id',
            'CESSATION YEAR':'cease_date',
             'Reason for ceasing employment':'separationtype',
             'Gender What is your Gender?':'gender',
              'CurrentAge. Current Age':'age',
              'Employment Type. Employment Type':'employment_status',
              'Classification. Classification':'position',
              'LengthofServiceOverall. Overall Length of Service at Institute (in years)':'institute_service'
             }
tafe_survey_updated=tafe_survey_updated.rename(new_colnames,axis=1)
#tafe_survey_updated.head()
#dete_survey_updated.head()


# # The column names in the DETE survey were changed to make it easier to read
# # The column names in the TAFE survey were renamed to shorter names

# In[77]:


#Look at the different types of separation in the TAFE survey
#tafe_survey_updated['separationtype'].value_counts()

#Look at the different types of separation in the DETE survey
#dete_survey_updated.columns
#dete_survey_updated['separationtype'].value_counts()

tafe_resignations=tafe_survey_updated[tafe_survey_updated['separationtype']=='Resignation'].copy()
dete_resignations=dete_survey_updated[dete_survey_updated['separationtype'].str.contains('Resignation')].copy()




# # Checking the years in the dete and tafe df for logical inconsistencies

# In[78]:



# Extract the years and convert them to a float type
dete_resignations['cease_date'] = dete_resignations['cease_date'].str.replace(r'[0-9][0-9]/','')
dete_resignations['cease_date'] = dete_resignations['cease_date'].astype("float")
#dete_resignations['dete_start_date'].value_counts()
#tafe_resignations['cease_date'].value_counts()


# In[79]:


#There is no column that sho\ws time in workplace so I will use the start end dates to calculate 
dete_resignations['institute_service']=dete_resignations['cease_date']-dete_resignations['dete_start_date']
#dete_resignations['institute_service']


# In[80]:


#dete_survey_updated['job_dissatisfaction'].value_counts()
#tafe_survey_updated['Contributing Factors. Dissatisfaction'].unique()


def update_vals(val):
    if pd.isnull(val):
        return np.nan
    elif val=='-':
        return False
    else:
        return True
    
tafe_resignations['dissatisfied'] = tafe_resignations[['Contributing Factors. Dissatisfaction', 'Contributing Factors. Job Dissatisfaction']].applymap(update_vals).any(1, skipna=False)
tafe_resignations_up = tafe_resignations.copy()

# Update the values in columns related to dissatisfaction to be either True, False, or NaN
dete_resignations['dissatisfied'] = dete_resignations[['job_dissatisfaction',
       'dissatisfaction_with_the_department', 'physical_work_environment',
       'lack_of_recognition', 'lack_of_job_security', 'work_location',
       'employment_conditions', 'work_life_balance',
       'workload']].any(1, skipna=False)
dete_resignations_up = dete_resignations.copy()



# In[81]:


dete_resignations_up['institute']='DETE'
tafe_resignations_up['institute']='TAFE'

# Combine the dataframes
combined = pd.concat([dete_resignations_up, tafe_resignations_up], ignore_index=True)
# Verify the number of non null values in each column
#print(combined.notnull().sum().sort_values())

#drop any columns >500 null values
combined_updated=combined.dropna(thresh=500,axis=1).copy()
#combined_updated.head()


# In[82]:


combined_updated['institute_service']=combined_updated['institute_service'].astype('str')
combined_updated['institute_service'].value_counts()
combined_updated['institute_service_up'] = combined_updated['institute_service'].astype('str').str.extract(r'(\d+)')
combined_updated['institute_service_up'] = combined_updated['institute_service_up'].astype('float')


#career stage function converts the number of years to a string based on amount of years of experience
def career_stage(num):
    if pd.isnull(num):
        return np.nan
    elif num<3:
        return 'New'
    elif num >=3.0 and num<7:
        return 'Experienced'
    elif num >=7.0 and num <11:
        return 'Established'
    else:
        return 'Veteran'

combined_updated['service_cat']=combined_updated['institute_service_up'].apply(career_stage)

combined_updated['service_cat'].value_counts()


# In[84]:


get_ipython().magic('matplotlib inline')
#check the number of NaN values
#combined_updated['dissatisfied'].value_counts(dropna=False)
combined_updated['dissatisfied']=combined_updated['dissatisfied'].fillna(False)

pt=pd.pivot_table(combined_updated,values='dissatisfied',columns='service_cat')
pt.plot(kind='bar')

