#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython import display
get_ipython().run_line_magic('matplotlib', 'inline')

dfBostonCalendar = pd.read_csv('./Boston/calendar.csv')
dfBostonListing = pd.read_csv('./Boston/listings.csv')
dfBostonReview = pd.read_csv('./Boston/reviews.csv')
dfSeattleCalendar = pd.read_csv('./Seattle/calendar.csv')
dfSeattleListing = pd.read_csv('./Seattle/listings.csv')
dfSeattleReview = pd.read_csv('./Seattle/reviews.csv')


# In[2]:


dfBostonCalendar.head()


# In[3]:


dfBostonListing['bedrooms'].value_counts()


# In[4]:


dfBostonListing.loc[dfBostonListing.id == 5506, ['bedrooms']]


# In[5]:


dfBostonListing['id'].is_unique


# In[6]:


#convert the Boston Listing with available as 0 and nonavilable as 1 to check how many day has it been rented out
dfBostonCalendar.loc[dfBostonCalendar.available == 't', 'Rented Out'] = 0
dfBostonCalendar.loc[dfBostonCalendar.available == 'f', 'Rented Out'] = 1


# In[7]:


#Create new table that display the average day of the each listing that has been rented out
dfBostonPriceEffectAnalysis = pd.DataFrame({'Percentage Rented Out': dfBostonCalendar.groupby(['listing_id']).mean()['Rented Out']}).reset_index()


# In[8]:


dfBostonPriceEffectAnalysis.head()


# In[9]:


#left join to get the number of room to the dfBostonPriceEffectAnalysis table
dfBostonPriceEffectAnalysis.set_index('listing_id')
dfBostonPriceEffectAnalysis2 = dfBostonPriceEffectAnalysis.join(other=dfBostonListing[['id','bedrooms', 'price']].set_index('id'), how='left', on='listing_id')


# In[10]:


dfBostonPriceEffectAnalysis2.head()


# In[11]:


#conver price to float value
dfBostonPriceEffectAnalysis2['price'] = dfBostonPriceEffectAnalysis2['price'].apply(lambda x: x.replace('$','')).apply(lambda x: x.replace(',','')).astype(float)


# In[12]:


dfBostonPriceEffectAnalysis2.describe()


# In[13]:


#drop the row that has no value of bedroom
dfBostonPriceEffectAnalysis2.dropna(how='any', inplace=True)


# In[14]:


dfBostonPriceEffectAnalysis2.describe()


# In[15]:


#catgorize the price Below 150 is low price, between 150 5o 300 is mid price, above 300 is high price
dfBostonPriceEffectAnalysis2.loc[dfBostonPriceEffectAnalysis2.price <= 150, 'Price Cateogry'] = "Low Price"
dfBostonPriceEffectAnalysis2.loc[((dfBostonPriceEffectAnalysis2.price > 150) & (dfBostonPriceEffectAnalysis2.price <= 300)), 'Price Cateogry'] = "Medium Price"
dfBostonPriceEffectAnalysis2.loc[dfBostonPriceEffectAnalysis2.price > 300, 'Price Cateogry'] = "High Price"


# In[16]:


#Drop the listing id column
dfBostonPriceEffectAnalysis2.drop(['listing_id'], axis=1, inplace=True)


# In[17]:


#drop the price column
dfBostonPriceEffectAnalysis2.drop(['price'], axis=1, inplace=True)


# In[18]:


#Display the result
dfBostonPriceEffectAnalysis2.groupby(['Price Cateogry', 'bedrooms']).mean().unstack()


# In[19]:


#Answer the question for the optimized room for AirBnB
dfBostonPriceEffectAnalysis2.groupby(['bedrooms', 'Price Cateogry']).mean().unstack()


# In[20]:


#Does seattle's Airbnb has higher price tag than Boston's airbnb
dfBostonAirbnb = dfBostonListing[['bedrooms', 'price']]
dfSeattleAirbnb = dfSeattleListing[['bedrooms', 'price']]


# In[21]:


#assign location to each dataframe
dfBostonAirbnb.insert(loc=1, column='Location', value='Boston')
dfSeattleAirbnb.insert(loc=1, column='Location', value='Seattle')


# In[27]:


#Concate the two dataframe together
dfAreaAnalysis = dfSeattleAirbnb
dfAreaAnalysis = dfAreaAnalysis.append(dfBostonAirbnb, ignore_index=True)


# In[28]:


dfAreaAnalysis.info()


# In[31]:


dfAreaAnalysis['price'] = dfAreaAnalysis['price'].astype(str)
dfAreaAnalysis['price'] = dfAreaAnalysis['price'].apply(lambda x: x.replace('$','')).apply(lambda x: x.replace(',','')).astype(float)


# In[33]:


dfAreaAnalysis.groupby(['bedrooms', 'Location']).mean().unstack()


# In[ ]:
