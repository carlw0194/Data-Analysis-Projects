#!/usr/bin/env python
# coding: utf-8

# # Malaria in Africa

# In[2]:


import pandas as pd
import os


# In[3]:


data = pd.read_csv('DatasetAfricaMalaria.csv')
malaria_data = data.copy()
malaria_data


# In[4]:


#exploring column data types
malaria_data.dtypes


# In[5]:


malaria_data.describe()


# In[6]:


# change the year column to string
malaria_data['Year']=malaria_data["Year"].astype(str)
malaria_data['Year'].dtypes


# In[7]:


malaria_data.columns


# In[8]:


# renaming columns
new_columns = ["CountryName","Year","CountryCode","IncidenceOfMalaria","MalariaCasesReported",
                       "UseOfInsecticideTreatedBedNets","ChildrenWithFeverReceivingAntimalarialDrugs",'IPTofMalariaInPregnancy',
                       "PUSMDWS(%oOfpopulation)","PUSMDWS(%oOfRuralpopulation)","PUSMDWS(%oOfUrbanpopulation)","PUSMSS(%oOfpopulation)",
                       "PUSMSS(%oOfRuralpopulation)","PUSMSS(%oOfUrbanpopulation)","RuralPopulation","RuralPopulationGrowth",
                       "UrbanPopulation","UrbanPopulationGrowth","PUABDWS(%oOfpopulation)","PUABDWS(%oOfRuralpopulation)","PUABDWS(%oOfUrbanpopulation)",
                       "PUABSS(%oOfpopulation)","PUABSS(%oOfRuralpopulation)","PUABSS(%oOfUrbanpopulation)","Latitude","Longitude","Geometry"]
new_columns


# In[9]:


# renaming the columns
malaria_data.columns = new_columns
malaria_data.columns


# In[12]:


import plotly.express as px # import library for plotting graphs
import plotly.io as pio # import plotly templates
pio.templates


# ## Incidence of Malaria(per 1000 of population at risk) per country

# In[13]:


figg = px.choropleth(malaria_data,locations="CountryCode",locationmode="ISO-3",animation_frame='Year',
                      title="Incidence of Malaria(per 1000 of population at risk) per country",
                    color="IncidenceOfMalaria", 
                    hover_name="CountryName", scope='africa',template ='presentation'
                    )
figg.show()


# ### Malaria cases reported by country

# In[14]:


fig_1 = px.choropleth(malaria_data,locations="CountryCode",locationmode="ISO-3",animation_frame='Year',
                      title="Malaria Cases reported per country",
                    color="MalariaCasesReported", 
                    hover_name="CountryName", scope='africa',template ='seaborn'
                    )
fig_1.show()


# ### 	Drop rows with missing values for no incidence of Malaria and  malaria cases reported

# In[15]:


#count the number of missing incidence of malaria
malaria_data['IncidenceOfMalaria'].isna().sum()


# In[16]:


#count the number of missing malaria cases reported
malaria_data['MalariaCasesReported'].isna().sum()


# In[17]:


# drop rows with missing values for incidence of malaria and malaria cases reported
malaria_data = malaria_data.dropna(subset=['IncidenceOfMalaria','MalariaCasesReported'])
malaria_data.reset_index(drop=True) # reset the index of the dataframe after dropping some rows


# In[383]:


# check if rows were dropped
malaria_data.isna().sum()


# ## Filling some columns of interest
# ### Filling UseOfInsecticideTreatedBedNets column
# 
# 
# 

# In[21]:


# assuming the worst case for all countries and filling the nan values with the min[column value] for each country 
malaria_data['UseOfInsecticideTreatedBedNets']=malaria_data.groupby('CountryName')['UseOfInsecticideTreatedBedNets'].apply(lambda gp : gp.fillna(gp.min()))


# In[22]:


malaria_data['UseOfInsecticideTreatedBedNets'].isna().sum()


# ### Filling  ChildrenWithFeverReceivingAntimalarialDrugs 

# In[23]:


malaria_data['ChildrenWithFeverReceivingAntimalarialDrugs']=malaria_data.groupby('CountryName')['ChildrenWithFeverReceivingAntimalarialDrugs'].apply(lambda gp : gp.fillna(gp.min()))


# In[24]:


malaria_data['ChildrenWithFeverReceivingAntimalarialDrugs'].isna().sum()


# ### Deleting columns with too many missing values
# Columns with too many missing values are unworkable with, hence we drop them.
# 

# In[28]:


malaria_data.drop(columns=['IPTofMalariaInPregnancy','PUSMDWS(%oOfpopulation)','PUSMSS(%oOfpopulation)'])
malaria_data


# In[29]:


# further data exploration
malaria_data["UseOfInsecticideTreatedBedNets"].isna().groupby(malaria_data['CountryName']).sum()


# In[30]:


# check if above result is true
# check if the min use insecticide treated bed nets in Cameroon is 21
cameroon_data = malaria_data[malaria_data['CountryName']=='Cameroon']
cameroon_data


# In[287]:


cameroon_data[['CountryName','UseOfInsecticideTreatedBedNets']].min()


# ## Checking for any casual or direct  relationship  between malaria cases reported and some variables

# In[32]:


import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


# In[33]:


plt.figure(figsize = (8, 5))
sns.regplot(y = "MalariaCasesReported", 
            x = "UseOfInsecticideTreatedBedNets", 
            data = malaria_data, 
            scatter_kws = {'color': 'k'}, # color for the points
            line_kws = {'color': 'red'}) # color for the regression line
plt.xlabel("UseOfInsecticideTreatedBedNets")
plt.ylabel("MalariaCasesReported")
plt.title("Regression plot of MalariaCasesReported vs UseOfInsecticideTreatedBedNets ", fontsize = 14, weight = "bold")
plt.show()


# In[34]:


# malaria cases vs children taking antimalarial
plt.figure(figsize = (8, 5))
sns.regplot(y = "MalariaCasesReported", 
            x = "ChildrenWithFeverReceivingAntimalarialDrugs", 
            data = malaria_data, 
            scatter_kws = {'color': 'k'}, # color for the points
            line_kws = {'color': 'red'}) # color for the regression line
plt.xlabel("ChildrenWithFeverReceivingAntimalarialDrugs")
plt.ylabel("MalariaCasesReported")
plt.title("Regression plot of MalariaCasesReported vs UseOfInsecticideTreatedBedNets ", fontsize = 14, weight = "bold")
plt.show()


# ### Trend of Malaria Cases Reported  in Africa

# In[39]:


plt.figure(figsize = (8, 5))
sns.lineplot(y = "MalariaCasesReported", 
            x = "Year", 
            data = malaria_data,)
plt.xlabel("Year")
plt.ylabel("MalariaCasesReported")
plt.title("Trend of Malaria Cases reported in Africa between 2007 and 2017  ", fontsize = 14, weight = "bold")
plt.show()


# ### Trend of IncidenceOfMalaria( per 1000 of population at risk) in Africa between 2007 and 2017

# In[40]:


plt.figure(figsize = (8, 5))
sns.lineplot(y = "IncidenceOfMalaria", 
            x = "Year", 
            data = malaria_data,)
plt.xlabel("Year")
plt.ylabel("IncidenceOfMalaria")
plt.title("Trend of IncidenceOfMalaria( per 1000 of population at risk) in Africa between 2007 and 2017  ", fontsize = 14, weight = "bold")
plt.show()

