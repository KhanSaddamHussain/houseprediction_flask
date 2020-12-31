#!/usr/bin/env python
# coding: utf-8

# In[1]:
import  pickle

import pandas as pd


# In[2]:
from IPython import get_ipython

houseData=pd.read_csv('USA_Housing.csv')


# In[3]:


houseData.head()


# In[4]:


houseData.info()


# In[5]:


houseData['Price'] = houseData['Price'].astype('int64')
houseData.dtypes


# In[6]:


houseData.describe()


# In[7]:


houseData.columns


# # Data analysis for price prediction

# In[8]:


import seaborn as sns


# In[9]:


sns.pairplot(houseData)


# In[10]:


sns.distplot(houseData['Price'])


# In[11]:


sns.heatmap(houseData.corr(), annot=True)


# # Get Data Ready for trainning Model

# In[12]:


X=houseData[['Avg. Area Income','Avg. Area House Age','Avg. Area Number of Rooms','Avg. Area Number of Bedrooms','Area Population']]
Y=houseData['Price']


# # Split Data into train and test

# In[13]:


X.head()


# In[14]:


Y.head()


# In[15]:


from sklearn.model_selection import train_test_split


# In[16]:


X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.33,random_state=101)


# In[17]:


X_train.head()


# # Creating Model 

# In[25]:


# from sklearn.tree import DecisionTreeRegressor
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression


# In[26]:


# lin=DecisionTreeRegressor()
# lin=RandomForestRegressor()
# lin=KNeighborsRegressor()
lin=LinearRegression()


# In[27]:


lin.fit(X_train,Y_train)


# In[31]:


print(lin.intercept_)


# In[32]:


lin_score=lin.score(X_test,Y_test)


# In[33]:


lin_score


# # Coefficient

# In[34]:


coe_data=pd.DataFrame(lin.coef_,X.columns,columns=['Coeffcient']) 


# In[35]:


coe_data


# # Prediction

# In[36]:


pred=lin.predict(X_test)


# In[37]:


pred


# In[38]:


Y_test


# In[39]:


import matplotlib.pyplot as plt


# In[40]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[41]:


plt.scatter(Y_test,pred)


# In[42]:


sns.distplot((Y_test,pred), bins=50)


# # Regression Evaluation Metrics

# In[43]:


from sklearn import metrics


# In[44]:


import numpy as np
print('MAE',metrics.mean_absolute_error(Y_test,pred))
print('MSE',metrics.mean_squared_error(Y_test,pred))
print('RMAE',np.sqrt(metrics.mean_absolute_error(Y_test,pred)))









