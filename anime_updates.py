from bs4 import BeautifulSoup
import requests
import time 
import re
import discord

# Define the URL to search
url = "https://myanimelist.net/watch/episode"

# Make the request to the URL
response = requests.get(url)

#time.sleep(10)

# Parse the HTML content of the response
soup = BeautifulSoup(response.text, 'html.parser')
    

anime_names = soup.find_all(class_='video-info-title') 
anime_episodes = soup.find_all(class_='title di-b')

            
def get_anime_names(anime_names):
    anime_name_list = []
    for name in anime_names: 
        anime = name.find('a',class_='mr4')
        anime_name_list.append(anime.string)
    return anime_name_list 

def get_anime_episodes(anime_eps):
    anime_episode_list = []
    for ep in anime_eps:
        res = re.sub('(\d+(\.\d+)?)', r' \1 ', str(ep.text))
        anime_episode_list.append(res)
    return anime_episode_list


def get_full_list():
    name_episode_list = []
    for name in get_anime_names(anime_names):
        item_number = get_anime_names(anime_names).index(name)
        name = get_anime_names(anime_names)[item_number]
        episode = get_anime_episodes(anime_episodes)[item_number]
        name_episode_list.append(str(name))
        name_episode_list.append(str(episode))
        name_episode_list.append('------------------')

    return name_episode_list
    
def get_episode_list():
     # Check if the request was successful
    if response.status_code != 200:
        print("Failed to fetch the URL")
        return []
    
    episode_list = []
    for ep in get_anime_episodes(anime_episodes):
        item_number = get_anime_episodes(anime_episodes).index(ep)
        episode = get_anime_episodes(anime_episodes)[item_number]
        episode_list.append(str(episode))
    return episode_list
        
def get_name_list():
     # Check if the request was successful
    if response.status_code != 200:
        print("Failed to fetch the URL")
        return []
    
    name_list = []
    for name in get_anime_names(anime_names):
        item_number = get_anime_names(anime_names).index(name)
        name = get_anime_names(anime_names)[item_number]
        episode = get_anime_episodes(anime_episodes)[item_number]
        name_list.append(str(name))
    return name_list

    
            
    

    
    