from credentials import TMDB_API_KEY
import requests


base_url = f'https://api.themoviedb.org/3/tv/{{}}?api_key={TMDB_API_KEY}'

# get tv show by id
def get_by_id(id):
    url = base_url.format(id)
    response = requests.get(url).json()
    return response

# get season of a tv show by id and number
def get_season(id, season_number):
    url = base_url.format(f'{id}/season/{season_number}')
    response = requests.get(url).json()
    return response