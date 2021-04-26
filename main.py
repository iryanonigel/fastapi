import requests
import pandas as pd
import json

# requesting match data from API
data = requests.get('https://api.opendota.com/api/heroes/121/matchups')
match = json.loads(data.text)
# converting match data to dataframe
match_df = pd.DataFrame(match)
match_df.sort_values(by='hero_id', inplace = True)
# match data manipulation
match_final_df = match_df.groupby(['hero_id'], as_index = False).agg({'games_played':'sum','wins': 'sum',})
match_final_df['win_rate'] = match_final_df['wins'] / match_final_df['games_played'] * 100

# requesting hero data from API
data = requests.get('https://api.opendota.com/api/heroes')
heroes = json.loads(data.text)
# converting hero data to dataframe
heroes_df = pd.DataFrame(heroes)
# heroes data manipulation
heroes_df['Carry'] = 'a'
heroes_df['Nuker'] = 'a'
heroes_df['Initiator'] = 'a'
heroes_df['Disabler'] = 'a'
heroes_df['Durable'] = 'a'
heroes_df['Escape'] = 'a'
heroes_df['Support'] = 'a'
heroes_df['Pusher'] = 'a'
heroes_df['Jungler'] = 'a'

for i in range(len(heroes_df['roles'])):
    heroes_df['Carry'][i] = 'Carry' in heroes_df['roles'][i]
    heroes_df['Nuker'][i] = 'Nuker' in heroes_df['roles'][i]
    heroes_df['Initiator'][i] = 'Initiator' in heroes_df['roles'][i]
    heroes_df['Disabler'][i] = 'Disabler' in heroes_df['roles'][i]
    heroes_df['Durable'][i] = 'Durable' in heroes_df['roles'][i]
    heroes_df['Escape'][i] = 'Escape' in heroes_df['roles'][i]
    heroes_df['Support'][i] = 'Support' in heroes_df['roles'][i]
    heroes_df['Pusher'][i] = 'Pusher' in heroes_df['roles'][i]
    heroes_df['Jungler'][i] = 'Jungler' in heroes_df['roles'][i]

heroes_df['total_roles'] = heroes_df['Carry'] + heroes_df['Nuker'] + heroes_df['Initiator'] + heroes_df['Disabler'] + heroes_df['Durable'] + heroes_df['Escape'] + heroes_df['Support'] + heroes_df['Pusher'] + heroes_df['Jungler']
heroes_df.drop('roles', 1,inplace=True)

# joining match data and hero data to get the final dataframe
dota_df = pd.merge(heroes_df, match_final_df, left_on='id', right_on='hero_id', how='inner').drop('hero_id', 1)

from typing import Optional
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/") # main api
def read_root(): 
    return {'message':'Dota 2 Heroes API', 
            'version':'BETA 0.9', 
            'endpoints':{'/[hero roles]':'List of heroes filtered by [hero roles] sorted by win rate descending. For example: /carry for carry heroes',
                         '/[total hero roles]_roles':'List of heroes filtered by [total hero roles] sorted by win rate descending. For example: /2_roles for 2 role heroes',
                         '/highest_win_rate':'Show the highest win rate hero from all roles',
                         '/most_played':'Show the most played hero from all roles'
                        }
           }

@app.get("/carry") # list all carry heroes sorted from highest win rate to lowest win rate
def read_root():
    return json.loads(dota_df[dota_df['Carry']==True].sort_values(by='win_rate', ascending = False).to_json(orient="records"))

@app.get("/nuker") # list all nuker heroes sorted from highest win rate to lowest win rate
def read_root():
    return json.loads(dota_df[dota_df['Nuker']==True].sort_values(by='win_rate', ascending = False).to_json(orient="records"))

@app.get("/initiator") # list all initiator heroes sorted from highest win rate to lowest win rate
def read_root():
    return json.loads(dota_df[dota_df['Initiator']==True].sort_values(by='win_rate', ascending = False).to_json(orient="records"))

@app.get("/disabler") # list all disabler heroes sorted from highest win rate to lowest win rate
def read_root():
    return json.loads(dota_df[dota_df['Disabler']==True].sort_values(by='win_rate', ascending = False).to_json(orient="records"))

@app.get("/durable") # list all durable heroes sorted from highest win rate to lowest win rate
def read_root():
    return json.loads(dota_df[dota_df['Durable']==True].sort_values(by='win_rate', ascending = False).to_json(orient="records"))

@app.get("/escape") # list all escape heroes sorted from highest win rate to lowest win rate
def read_root():
    return json.loads(dota_df[dota_df['Escape']==True].sort_values(by='win_rate', ascending = False).to_json(orient="records"))

@app.get("/support") # list all support heroes sorted from highest win rate to lowest win rate
def read_root():
    return json.loads(dota_df[dota_df['Support']==True].sort_values(by='win_rate', ascending = False).to_json(orient="records"))

@app.get("/pusher") # list all pusher heroes sorted from highest win rate to lowest win rate
def read_root():
    return json.loads(dota_df[dota_df['Pusher']==True].sort_values(by='win_rate', ascending = False).to_json(orient="records"))

@app.get("/jungler") # list all jungler heroes sorted from highest win rate to lowest win rate
def read_root():
    return json.loads(dota_df[dota_df['Jungler']==True].sort_values(by='win_rate', ascending = False).to_json(orient="records"))

@app.get("/2_roles") # list all 2 role heroes sorted from highest win rate to lowest win rate
def read_root():
    return json.loads(dota_df[dota_df['total_roles']==2].sort_values(by='win_rate', ascending=False).to_json(orient="records"))

@app.get("/3_roles") # list all 3 role heroes sorted from highest win rate to lowest win rate
def read_root():
    return json.loads(dota_df[dota_df['total_roles']==3].sort_values(by='win_rate', ascending=False).to_json(orient="records"))

@app.get("/4_roles") # list all 4 role heroes sorted from highest win rate to lowest win rate
def read_root():
    return json.loads(dota_df[dota_df['total_roles']==4].sort_values(by='win_rate', ascending=False).to_json(orient="records"))

@app.get("/5_roles") # list all 5 role heroes sorted from highest win rate to lowest win rate
def read_root():
    return json.loads(dota_df[dota_df['total_roles']==5].sort_values(by='win_rate', ascending=False).to_json(orient="records"))

@app.get("/6_roles") # list all 6 role heroes sorted from highest win rate to lowest win rate
def read_root():
    return json.loads(dota_df[dota_df['total_roles']==6].sort_values(by='win_rate', ascending=False).to_json(orient="records"))

@app.get("/highest_win_rate") # show the highest win rate hero from all roles
def read_root():
    return json.loads(dota_df[dota_df['win_rate']==dota_df['win_rate'].max()].to_json(orient="records"))

@app.get("/most_played") # show the most played hero from all roles
def read_root():
    return json.loads(dota_df[dota_df['games_played']==dota_df['games_played'].max()].to_json(orient="records"))