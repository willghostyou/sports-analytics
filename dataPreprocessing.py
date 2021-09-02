#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
get_ipython().run_line_magic('matplotlib', 'notebook')


# In[2]:


# reading and processing players
players = pd.read_csv("./data/laliga_players.csv")
team_names = {'Athletic Club':"", 'Atlético de Madrid':"Ath Madrid", 'CD Leganés':"Leganes", 'D. Alavés':"Alaves",
       'FC Barcelona':"Barcelona", 'Getafe CF':"Getafe", 'Girona FC':"", 'Levante UD':"Levante",
       'R. Valladolid CF':"Valladolid", 'Rayo Vallecano':"", 'RC Celta':"Celta", 'RCD Espanyol':"Espanol",
       'Real Betis':"Betis", 'Real Madrid':"Real Madrid", 'Real Sociedad':"Sociedad", 'SD Eibar':"Eibar",
       'SD Huesca':"", 'Sevilla FC':"Sevilla", 'Valencia CF':"Valencia", 'Villarreal CF':"Villarreal"}
players = players.replace(team_names) 
players = players[players["Team"]!=""]
tnames = players["Team"].unique()
# players = players.set_index(["Team","Position"])


# In[3]:



forward = players[players["Position"]=="Forward"]
forward = forward.groupby(["Team"])[["Shots on target","Successful dribbles",'Goals scored','Goals scored per attempt']].agg(np.mean)

midfield = players[players["Position"]=="Midfielder"]
midfield = midfield.groupby(["Team"])[["Assists","Passes","Short passes","Through balls"]].agg(np.mean)
midfield

defense = players[players["Position"]=="Defender"]
defense = defense.groupby(["Team"])[["Clearances","Penalties given away","Last man","Interceptions","Tackles","Successful tackles","Unssuccessful tackles"]].agg(np.mean)
defense

goalkeeper = players[players["Position"]=="Goalkeeper"]
goalkeeper = goalkeeper.groupby(["Team"])["Long passes"].agg(np.mean)
goalkeeper
defense
forward


# In[4]:


# reading and preprocessing matches data from 09/10 to 19/20 season
matches=[]
for i in range(9,20):
    season = str(i)+str(i+1)
    source = "./data/"+season+".csv"
    match = pd.read_csv(source)
    if "Time" in match.columns:
        match = match.drop("Time", axis=1)
    matches.append(match)
team_names=[
    'Barcelona', 'Real Madrid', 'Sociedad', 'Eibar',
    'Levante', 'Sevilla', 'Valladolid', 'Getafe',
    'Villarreal', 'Valencia', 'Espanol', 'Ath Madrid',
    'Betis', 'Celta', 'Alaves',"Leganes"
        ]


def nameedit(item):
    if item in team_names:
        return item
    return ""

processed_matches = []
for match in matches:
    match.HomeTeam = match["HomeTeam"].apply(nameedit)
    match.AwayTeam = match["AwayTeam"].apply(nameedit)
    match = match[match["HomeTeam"]!=""]
    match = match[match["AwayTeam"]!=""]
    match = match.rename(columns={"HomeTeam":"Team"})
    match = match.iloc[:,:23]
    processed_matches.append(match)

    
    
merge = []
for i in processed_matches:
    x=i.merge(forward, how="left", on="Team" ).rename(columns = {"Team":"HomeTeam","AwayTeam":"Team"}).merge(forward, how = "left", on="Team")
    x=x.rename(columns = {"HomeTeam":"Team","Team":"AwayTeam"}).merge(midfield, how="left", on="Team" ).rename(columns = {"Team":"HomeTeam","AwayTeam":"Team"}).merge(midfield, how = "left", on="Team")
    x=x.rename(columns = {"HomeTeam":"Team","Team":"AwayTeam"}).merge(defense, how="left", on="Team" ).rename(columns = {"Team":"HomeTeam","AwayTeam":"Team"}).merge(defense, how = "left", on="Team")
    x=x.rename(columns = {"HomeTeam":"Team","Team":"AwayTeam"}).merge(goalkeeper, how="left", on="Team" ).rename(columns = {"Team":"HomeTeam","AwayTeam":"Team"}).merge(goalkeeper, how = "left", on="Team")
    x=x.rename(columns= {"Team":"AwayTeam"})
    merge.append(x)


# In[5]:


dfx = merge[10]
len(dfx.index)


# In[6]:


from sklearn.model_selection import train_test_split
x = dfx.drop(["HTR","FTR"],axis=1)
y = dfx["FTR"]
col = x.columns[4:]
x=x.iloc[:,4:]
for c in col:
    x[c] = x[c].astype(int)
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
le.fit(y.unique())
print(y[:5])
y = le.transform(y)
print(y[:5])
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,shuffle=False)


# In[9]:


import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop

model = tf.keras.models.Sequential([tf.keras.layers.Dense(49, activation='relu',input_shape=[len(x.columns)]),
                                    tf.keras.layers.Dense(512, activation='relu'),
                                    tf.keras.layers.Dense(512, activation='relu'),
                                    tf.keras.layers.Dense(3, activation='softmax')])
model.compile(optimizer=RMSprop(lr=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()


# In[10]:


len(x_train)
y_train


# In[13]:


model.fit(x_train,y_train,epochs=40)


# In[14]:


model.evaluate(x_test,y_test)


# In[ ]:




