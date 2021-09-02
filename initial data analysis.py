#!/usr/bin/env python
# coding: utf-8

# In[2]:


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
get_ipython().run_line_magic('matplotlib', 'notebook')


# In[2]:


df = pd.read_csv("./capstone/data/laliga2019_2020.csv")
len(df["HomeTeam"].unique())


# In[3]:


df.shape


# In[4]:



hst = df["HST"]
hc = df["HC"]
fthg = df["FTHG"]


# In[5]:


plt.figure()
plt.plot(hc,"-b" ,fthg,"-r")
plt.title("cornors vs goals")
plt.legend(["cornors","goals"])
plt.gca().fill_between(range(len(hc)), hc, fthg, color="pink", alpha=0.9)


# In[6]:


xvals = range(len(hc))
plt.figure()
plt.bar(xvals, hc, color="blue")
plt.bar(xvals, fthg, color="red")


# In[7]:


barcelona = df[df["HomeTeam"]=="Barcelona"]
bhst = barcelona["HST"]
bhc = barcelona["HC"]
bfthg = barcelona["FTHG"]


# In[8]:


plt.figure()
plt.plot(bhc,"-b" ,bfthg,"-r")
plt.title("cornors vs goals")
plt.legend(["cornors","goals"])


# In[9]:


xvals = range(len(bhc))
plt.figure()
plt.bar(xvals, bhc, color="blue", width=0.3)


# In[10]:


new_xvals=[]
for item in xvals:
    new_xvals.append(item+0.3)


# In[11]:


plt.bar(new_xvals, bfthg, color="red", width=0.4)
plt.title("Barcelona cornors vs goals")
plt.legend(["cornors","goals"])


# In[93]:


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


# In[129]:


# match dataset setting up

matches = pd.read_csv("./data/1920.csv")
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
matches.HomeTeam = matches["HomeTeam"].apply(nameedit)
matches = matches[matches["HomeTeam"]!=""]
matches


# In[130]:


for team in team_names:
    if team not in tnames:
        print(team)


# In[95]:


players.columns


# In[96]:


players["Position"].unique()


# In[97]:



forward = players[players["Position"]=="Forward"]
forward = forward.groupby(["Team"])[["Shots on target","Successful dribbles",'Goals scored','Goals scored per attempt']].agg(np.mean)

midfield = players[players["Position"]=="Midfielder"]
midfield = midfield.groupby(["Team"])[["Assists","Passes","Short passes","Long passes","Through balls"]].agg(np.mean)
midfield

defense = players[players["Position"]=="Defender"]
defense = defense.groupby(["Team"])[["Clearances","Penalties given away","Last man","Interceptions","Tackles","Long passes","Successful tackles","Unssuccessful tackles"]].agg(np.mean)
defense

goalkeeper = players[players["Position"]=="Goalkeeper"]
goalkeeper = goalkeeper.groupby(["Team"])["Long passes"].agg(np.mean)
goalkeeper
defense
forward


# In[131]:


# reading and preprocessing matches data from 09/10 to 19/20 season
matches=[]
for i in range(9,20):
    season = str(i)+str(i+1)
    source = "./data/"+season+".csv"
    match = pd.read_csv(source)
    if "Time" in match.columns:
        match = match.drop("Time", axis=1)
    matches.append(match)


# In[134]:


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
    def nameedit(item):
        if item in team_names:
            return item
        return ""
    match.HomeTeam = match["HomeTeam"].apply(nameedit)
    match.AwayTeam = match["AwayTeam"].apply(nameedit)
    match = match[match["HomeTeam"]!=""]
    match = match[match["AwayTeam"]!=""]
    match = match.rename(columns={"HomeTeam":"Team"})
    match = match.iloc[:,:23]
    processed_matches.append(match)


# In[135]:


for i in range(len(matches)):
    print(matches[i].shape,processed_matches[i].shape)


# In[136]:


#checking if all the columns are same or not.
for i in range(len(matches)-1):
    print(processed_matches[i].columns == processed_matches[i+1].columns)


# In[137]:


for i in range(len(matches)):
    print(processed_matches[i].head())


# In[138]:


merge = []
for i in processed_matches:
    x=i.merge(forward, how="left", on="Team" ).rename(columns = {"Team":"HomeTeam","AwayTeam":"Team"}).merge(forward, how = "left", on="Team")
    x=x.rename(columns = {"HomeTeam":"Team","Team":"AwayTeam"}).merge(midfield, how="left", on="Team" ).rename(columns = {"Team":"HomeTeam","AwayTeam":"Team"}).merge(midfield, how = "left", on="Team")
    x=x.rename(columns = {"HomeTeam":"Team","Team":"AwayTeam"}).merge(defense, how="left", on="Team" ).rename(columns = {"Team":"HomeTeam","AwayTeam":"Team"}).merge(defense, how = "left", on="Team")
    x=x.rename(columns = {"HomeTeam":"Team","Team":"AwayTeam"}).merge(goalkeeper, how="left", on="Team" ).rename(columns = {"Team":"HomeTeam","AwayTeam":"Team"}).merge(goalkeeper, how = "left", on="Team")
    x=x.rename(columns= {"Team":"AwayTeam"})
    merge.append(x)


# In[139]:


for i in range(len(merge)-1):
    print(merge[i].columns == merge[i+1].columns)


# In[140]:


merge[10].head()


# In[ ]:




