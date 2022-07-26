#!/usr/bin/env python
# coding: utf-8

# # Malaria in Africa

# In[320]:


import pandas as pd
import os


# In[321]:


data = pd.read_csv('DatasetAfricaMalaria.csv')
malaria_data = data.copy()
malaria_data


# In[322]:


#exploring column data types
malaria_data.dtypes


# In[323]:


malaria_data.describe


# In[349]:


# change the year column to string
malaria_data['Year']=malaria_data["Year"].astype(str)
malaria_data['Year'].dtypes


# In[325]:


malaria_data.columns


# In[326]:


# renaming columns
new_columns = ["CountryName","Year","CountryCode","IncidenceOfMalaria","MalariaCasesReported",
                       "UseOfInsecticideTreatedBedNets","ChildrenWithFeverReceivingAntimalarialDrugs",'IPTofMalariaInPregnancy',
                       "PUSMDWS(%oOfpopulation)","PUSMDWS(%oOfRuralpopulation)","PUSMDWS(%oOfUrbanpopulation)","PUSMSS(%oOfpopulation)",
                       "PUSMSS(%oOfRuralpopulation)","PUSMSS(%oOfUrbanpopulation)","RuralPopulation","RuralPopulationGrowth",
                       "UrbanPopulation","UrbanPopulationGrowth","PUABDWS(%oOfpopulation)","PUABDWS(%oOfRuralpopulation)","PUABDWS(%oOfUrbanpopulation)",
                       "PUABSS(%oOfpopulation)","PUABSS(%oOfRuralpopulation)","PUABSS(%oOfUrbanpopulation)","Latitude","Longitude","Geometry"]
new_columns


# ### Column name keys 
#        'Country Name', 'Year', 'Country Code',
#        'Incidence of malaria (per 1,000 population at risk)',
#        'Malaria cases reported',
#        'Use of insecticide-treated bed nets (% of under-5 population)',
#        'Children with fever receiving antimalarial drugs (% of children under age 5 with fever)',
#        'Intermittent preventive treatment (IPT) of malaria in pregnancy (% of pregnant women)',
#        'People using safely managed drinking water services (% of population)',
#        'People using safely managed drinking water services, rural (% of rural population)',
#        'People using safely managed drinking water services, urban (% of urban population)',
#        'People using safely managed sanitation services (% of population)',
#        'People using safely managed sanitation services, rural (% of rural population)',
#        'People using safely managed sanitation services, urban  (% of urban population)',
#        'Rural population (% of total population)',
#        'Rural population growth (annual %)',
#        'Urban population (% of total population)',
#        'Urban population growth (annual %)',
#        'People using at least basic drinking water services (% of population)',
#        'People using at least basic drinking water services, rural (% of rural population)',
#        'People using at least basic drinking water services, urban (% of urban population)',
#        'People using at least basic sanitation services (% of population)',
#        'People using at least basic sanitation services, rural (% of rural population)',
#        'People using at least basic sanitation services, urban  (% of urban population)',
#        'latitude', 'longitude', 'geometry'

# In[327]:


malaria_data.columns = new_columns
malaria_data.columns


# In[328]:


pd.isna(malaria_data['IncidenceOfMalaria']).sum()


# ### Malaria cases reported by country

# In[329]:


import plotly.express as px


# In[330]:


import plotly.io as pio
pio.templates


# In[331]:


fig_1 = px.choropleth(malaria_data,locations="CountryCode",locationmode="ISO-3",animation_frame='Year',
                      title="Malaria Cases reported per country",
                    color="MalariaCasesReported", 
                    hover_name="CountryName", scope='africa',template ='seaborn'
                    )
fig_1.show()


# ### Incidence of Malaria per country

# In[332]:


fig_2 =  px.choropleth(malaria_data,locations="CountryCode",locationmode="ISO-3",animation_frame='Year',
                       title='Incidence Of Malaria per Country',labels={'IncidenceOfMalaria':'Incidence of malaria (per 1,000 population at risk)'},
                    color="IncidenceOfMalaria", 
                    hover_name="CountryName", scope='africa',template='ggplot2'
                    )
fig_2.show()


# ### 	Drop rows with missing values for no incidence of Malaria and  malaria cases reported

# In[333]:


#count the number of missing incidence of malaria
malaria_data['IncidenceOfMalaria'].isna().sum()


# In[334]:


#count the number of missing malaria cases reported
malaria_data['MalariaCasesReported'].isna().sum()


# In[353]:


# drop rows with missing values for incidence of malaria and malaria cases reported
malaria_data = malaria_data.dropna(subset=['IncidenceOfMalaria','MalariaCasesReported'])
malaria_data.reset_index(drop=True) # reset the index of the dataframe after dropping some rows


# In[352]:


malaria_data.shape


# In[336]:


# check if rows were dropped
malaria_data.isna().sum()


# In[337]:


# delete unnecessary columns
unwanted_columns = ['PUSMDWS(%oOfRuralpopulation)','PUSMDWS(%oOfUrbanpopulation)','PUSMSS(%oOfRuralpopulation)', 
                    'PUSMSS(%oOfUrbanpopulation)','PUABDWS(%oOfRuralpopulation)','PUABDWS(%oOfUrbanpopulation)',
                    'PUABSS(%oOfRuralpopulation)', 'PUABSS(%oOfUrbanpopulation)','Geometry']  
malaria_data=malaria_data.drop(columns=unwanted_columns)                                                      


# In[343]:


malaria_data


# In[350]:


malaria_data.describe()


# In[351]:


malaria_data.isna().sum()


# ## Filling some columns of interest
# ### Filling UseOfInsecticideTreatedBedNets column
# Assumptions
# Countries with no incidence of malaria would have higher numbers of UseOfInsecticideTreatedBedNets
# 

# ### Filling  ChildrenWithFeverReceivingAntimalarialDrugs 

# ### Filling IPTofMalariaInPregnancy

# ### Filling PUSMDWS(%oOfpopulation)

# ### Filling PUSMSS(%oOfpopulation) 	

# ### PUABSS(%oOfpopulation)

# ### PUABSS(%oOfpopulation)

# In[354]:


# get the number of null values for "UseOfInsecticideTreatedBedNets" per country and sort in ascending order
malaria_data["UseOfInsecticideTreatedBedNets"].isna().groupby(malaria_data['CountryName']).sum()


# ### Too many missing values for these columns:
# 
# #UseOfInsecticideTreatedBedNets                
# #ChildrenWithFeverReceivingAntimalarialDrugs   
# #IPTofMalariaInPregnancy                       
# #PUSMDWS(%oOfpopulation)                       
# #PUSMDWS(%oOfRuralpopulation)                  
# #PUSMDWS(%oOfUrbanpopulation)                  
# #PUSMSS(%oOfpopulation)                        
# #PUSMSS(%oOfRuralpopulation)                   
# #PUSMSS(%oOfUrbanpopulation) 
# 
# #To proceed with analysis, we shall assume the worst case scenario and fill the nan values with the min no of each 
# #column criteria for each country
# 
# #shall be done only for analysis relevant columns ie
# 
# #UseOfInsecticideTreatedBedNets                
# #ChildrenWithFeverReceivingAntimalarialDrugs   
# #IPTofMalariaInPregnancy                       
# #PUSMDWS(%oOfpopulation
# #PUSMSS(%oOfpopulation

# In[339]:


# assume the worst case scenario and fill the nan values with the min no of each #column criteria for each country
# for each country, get the malaria_data[UseOfInsecticideTreatedBedNets].min()


# In[340]:


column_list =['UseOfInsecticideTreatedBedNets','ChildrenWithFeverReceivingAntimalarialDrugs',
              'IPTofMalariaInPregnancy','PUSMDWS(%oOfpopulation)','PUSMSS(%oOfpopulation)']


# In[341]:


result=malaria_data["UseOfInsecticideTreatedBedNets"].groupby(malaria_data['CountryName']).min().sort_values()
result


# In[342]:


# check if above result is true
# check if the min use insecticide treated bed nets in Cameroon is 21
cameroon_data = malaria_data[malaria_data['CountryName']=='Cameroon']
cameroon_data


# In[287]:


cameroon_data[['CountryName','UseOfInsecticideTreatedBedNets']].min()


# In[223]:


dictionary_result=result.to_dict


# In[316]:


# fill the nans in each column of interest , for each country, with the min row value for that country
malaria_data['UseOfInsecticideTreatedBedNets']=malaria_data["UseOfInsecticideTreatedBedNets"].fillna()


# In[304]:


#check if nans exist in column
malaria_data['UseOfInsecticideTreatedBedNets'].isna().sum()


# In[306]:


# using a for loop
print('entering the for loop')
for s in column_list:
    result1 = malaria_data[s].groupby(malaria_data['CountryName']).min().sort_values()
    print("On column",s)
    malaria_data[s] = malaria_data[s].fillna(result)
    print('filled nans in column',s)
    print(malaria_data[s])


# ## Checking for any casual or direct  relationship  between malaria cases reported and some variables

# In[190]:


plt.figure(figsize = (10, 6))
sns.regplot(y = malaria_data["MalariaCasesReported"].notna, 
            x = malaria_data["UseOfInsecticideTreatedBedNets"].notna(), 
            data = malaria_data, 
            scatter_kws = {'color': 'k'}, # color for the points
            line_kws = {'color': 'red'}) # color for the regression line
plt.xlabel("UseOfInsecticideTreatedBedNets")
plt.ylabel("MalariaCasesReported")
plt.title("Regression plot of MalariaCasesReported vs UseOfInsecticideTreatedBedNets ", fontsize = 14, weight = "bold")
plt.show()


# In[194]:


malaria_data[malaria_data["UseOfInsecticideTreatedBedNets"].notna()]


# In[165]:


malaria_data.columns


# In[187]:


# different x axes to be used
x1 = malaria_data['UseOfInsecticideTreatedBedNets']
x2 = malaria_data['ChildrenWithFeverReceivingAntimalarialDrugs']
x3= malaria_data['IPTofMalariaInPregnancy']
# y axis
y=malaria_data['MalariaCasesReported']
# Initialise the subplot function using number of rows and columns
figure, axis = plt.subplots(3,1 ,figsize=(10,15))
axis[0].plot(x1,y)
axis[0].set_title = ('Regression plot of MalariaCasesReported vs UseOfInsecticideTreatedBedNets'
)


# In[150]:


# Comparism of number of cases of malaria reported between urban and rural areas
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


# In[162]:


df = malaria_data[['CountryName','Year','RuralPopulation','UrbanPopulation','MalariaCasesReported']]


# In[164]:


df.groupby('Year').last()


# In[ ]:




