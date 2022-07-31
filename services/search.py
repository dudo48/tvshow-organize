from credentials import TMDB_API_KEY
import requests


base_url = f'https://api.themoviedb.org/3/search/tv?api_key={TMDB_API_KEY}'

def get_by_name(name):
    url = f'{base_url}&query={name}'
    response = requests.get(url).json()
    return response['results'][0]