import json
import requests

def get_matches_data_from_api(): 
    url = "https://v3.football.api-sports.io/fixtures?league=4&season=2020&next=50&timezone=Europe/Paris"

    payload={}
    headers = {
    'x-rapidapi-key': '59938c7e1ab38da9019c628471af8bed',
    'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


get_matches_data_from_api()