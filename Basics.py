#!/usr/bin/env python
# coding: utf-8

# # Exploring Ebay car sales Data
# 
# The aim of this project is to clean the data and analyze the included used car listings. 

# In[289]:


import pandas as pd
import numpy as np

autos=pd.read_csv('autos.csv',encoding='Latin-1')


# In[290]:


#autos


# In[291]:


#autos.info()
#autos.head()


# Change the columns from camelcase to snakecase.
# Change a few wordings to more accurately describe the columns.
# 

# In[292]:


autos.columns = ['date_crawled', 'name', 'seller', 'offer_type', 'price', 'ab_test',
       'vehicle_type', 'registration_year', 'gearbox', 'power_ps', 'model',
       'odometer', 'registration_month', 'fuel_type', 'brand',
       'unrepaired_damage', 'ad_created', 'num_photos', 'postal_code',
       'last_seen']
#autos.head()



# In[293]:


autos.describe(include='all')
#autos['num_photos'].value_counts()
autos = autos.drop(["num_photos", "seller", "offer_type"], axis=1)


# # Findings from describe
# -'seller' and 'offer_type' and 'num_photos' columns are candidates to be dropped due to having mostly one value
# -price and odometer are stored as text
# 

# In[294]:


autos["price"] = (autos["price"]
                          .str.replace("$","")
                          .str.replace(",","")
                          .astype(int)
                          )

autos['odometer']=(autos['odometer']
                       .str.replace('km','')
                       .str.replace(',','')
                       .astype(int)
                  )

autos.rename(columns={'odometer' : 'odometer_km'}, inplace=True)

#autos['odometer_km']


# In[295]:


autos['price'].value_counts().sort_index(ascending=True).head()


# # Outliers
# There are some prices that is over $10 million, and about 1500 that are $5 or less

# In[296]:


autos = autos[autos["price"].between(1,351000)]
autos["price"].describe()


# In[297]:


(autos["date_crawled"]
        .str[:10]
        .value_counts(normalize=True, dropna=False)
        .sort_values()
        )


# The daily distirubtion for date crawled is pretty uniform.

# In[298]:


(autos["ad_created"]
        .str[:10]
        .value_counts(normalize=True, dropna=False)
        .sort_values()
        )


# the number of ads created is slightly higher in march and april

# In[299]:


(autos["last_seen"]
        .str[:10]
        .value_counts(normalize=True, dropna=False)
        .sort_values()
        )


# the number of last seen is slightly higher in march and april

# In[300]:


autos["registration_year"].describe()


# year 1000 and 999 are probably not accurate

# Lowest acceptable value 1927 due to earliest after cars were invented
# Highest acceptable value 2016 due to year posts were last sween

# In[301]:



# Many ways to select rows in a dataframe that fall within a value range for a column.
# Using `Series.between()` is one way.
autos = autos[autos["registration_year"].between(1900,2016)]
autos['registration_year'].value_counts(normalize=True)


# In[302]:


#autos['brand'].value_counts()
brand_counts = autos["brand"].value_counts(normalize=True)
common_brands = brand_counts[brand_counts > .05].index

#autos['brand'].index

brand_mean_prices = {}

for brand in common_brands:
    brand_only = autos[autos["brand"] == brand]
    mean_price = brand_only["price"].mean()
    brand_mean_prices[brand] = int(mean_price)
    
print(brand_mean_prices)


# In[312]:


brand_mean_mileage={}
for brand in common_brands:
    brand_only = autos[autos["brand"] == brand]
    mean_mileage = brand_only["odometer_km"].mean()
    brand_mean_mileage[brand] = int(mean_mileage)
    
bmp = pd.Series(brand_mean_prices)
bmm = pd.Series(brand_mean_mileage)
df=pd.DataFrame(bmp,columns=['brand_mean_prices'])
df['brand_mean_mileage']=bmm


# the 
