import requests
import os
from dotenv import load_dotenv
import json
import time
import csv
import numpy as np

load_dotenv()

RATE_LIMIT_DELAY = 0.67  # Delay in seconds between consecutive requests (1.5 requests per second)
MAX_REQUESTS = 90  # Maximum number of requests allowed per minute
API_ERR = []
ERR = []

def add_to_json(json_obj, file):
    # Convert the JSON object to a string
    json_string = json.dumps(json_obj)
    # Open the file in append mode and write the JSON object
    with open(file, 'a') as file:
        file.write(json_string + '\n')
    
    print("Added to file.")


access_token = os.getenv("ACCESS_TOKEN")


def fetch_anime_data(id):
    anime_id = id
    fields = "id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    url = f"https://api.myanimelist.net/v2/anime/{anime_id}?fields={fields}"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.raise_for_status()
            anime_data = response.json()
            # print("Anime Data:", anime_data)
            # json_data = json.dumps(anime_data, indent=4)
            return anime_data
        else:
            ERR.append(id)
            print("Error fetching anime data")
            print(response.status_code)
    except requests.exceptions.RequestException as e:
        API_ERR.append(id)
        print("API Error:", e)

# fetch_anime_data(1)

# Fetch anime data for IDs 1 to 50,000
animelist_range = (30000, 50000)

for anime_id in range(animelist_range[0], animelist_range[1]):
    print(f'Fetching anime with id {anime_id} ')
    anime_data = fetch_anime_data(anime_id)
    file = f'animelist_{animelist_range[0]}_{animelist_range[1]}.jsonl'
    if anime_data:
        # saves into json-lines
        add_to_json(anime_data, file)
    time.sleep(RATE_LIMIT_DELAY)  # Delay between consecutive requests


print(f'Errors: {ERR}, {API_ERR}')
np.savez("err-30.npz", array1=np.array(ERR), array2=np.array(API_ERR))
print("Anime data fetching completed.")
