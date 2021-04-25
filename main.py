import requests
import pandas as pd
import json
from tqdm import tqdm
pd.set_option('display.max_columns', None)


match = []
for i in tqdm(range (121, 122)):
    url = 'https://api.opendota.com/api/heroes/' + str(i) + '/matchups'
    data = requests.get(url)
    match_temp = json.loads(data.text)
    match.extend(match_temp)

match_df = pd.DataFrame(match)


match_df.sort_values(by='hero_id', inplace = True)



match_final_df = match_df.groupby(
['hero_id'], as_index = False
).agg(
{
'games_played':'sum',
'wins': 'sum',
}
)



match_final_df['win_rate'] = match_final_df['wins'] / match_final_df['games_played'] * 100



match_final_df



data = requests.get('https://api.opendota.com/api/heroes')
heroes = json.loads(data.text)



heroes_df = pd.DataFrame(heroes)



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





dota_df = pd.merge(heroes_df, match_final_df, left_on='id', right_on='hero_id', how='inner').drop('hero_id', 1)





dota_df.sort_values(by='games_played', ascending=False)





main = json.loads(dota_df.to_json(orient="records"))






from typing import Optional
from fastapi import FastAPI
import uvicorn




app = FastAPI()

@app.get("/")
def read_root():
    return main

@app.get("/carry")
def read_root():
    return json.loads(dota_df[dota_df['Carry']==True].to_json(orient="records"))

@app.get("/nuker")
def read_root():
    return json.loads(dota_df[dota_df['Nuker']==True].to_json(orient="records"))

@app.get("/initiator")
def read_root():
    return json.loads(dota_df[dota_df['Initiator']==True].to_json(orient="records"))

@app.get("/disabler")
def read_root():
    return json.loads(dota_df[dota_df['Disabler']==True].to_json(orient="records"))

@app.get("/durable")
def read_root():
    return json.loads(dota_df[dota_df['Durable']==True].to_json(orient="records"))

@app.get("/escape")
def read_root():
    return json.loads(dota_df[dota_df['Escape']==True].to_json(orient="records"))

@app.get("/support")
def read_root():
    return json.loads(dota_df[dota_df['Support']==True].to_json(orient="records"))

@app.get("/pusher")
def read_root():
    return json.loads(dota_df[dota_df['Pusher']==True].to_json(orient="records"))

@app.get("/jungler")
def read_root():
    return json.loads(dota_df[dota_df['Jungler']==True].to_json(orient="records"))

@app.get("/highest_win_rate")
def read_root():
    return json.loads(dota_df[dota_df['win_rate']==dota_df['win_rate'].max()].to_json(orient="records"))

@app.get("/most_played")
def read_root():
    return json.loads(dota_df[dota_df['games_played']==dota_df['games_played'].max()].to_json(orient="records"))