"""
Written by Joel Krim

This project uses The Movie Database (TMDb) REST API
Documentation: https://developers.themoviedb.org/3/getting-started/introduction
"""

import requests
import urllib.parse as ul
from pprint import pprint

key = "api_key=665e86f05c67c2031783a1a12386ece4"
endpoint = "https://api.themoviedb.org/3/"

# map from actor's ID to his/her name
id_to_name = {}

# map from movie's ID to title
id_to_movie = {}

# map from actor to all of his/her costars,
# as well as in which movie they costarred
actors_to_costars = {}

def get_id_from_name(name):
    """
    retrieve ID from actor's name
    :param name: the actor's name
    :return: the actor's ID -- as a string
    """

    query = ul.quote(name)

    print(query)

    response = requests.get(endpoint + "search/person?" + key + "&language=en-US&query=" + query).json()

    id = response.get("results")[0].get("id")

    return id

get_id_from_name("Liam Neeson")