"""
Written by Joel Krim

This project uses The Movie Database (TMDb) REST API
Documentation: https://developers.themoviedb.org/3/getting-started/introduction
"""

import requests
import urllib.parse as ul
import time
import json
from pprint import pprint

key = "api_key=665e86f05c67c2031783a1a12386ece4"
endpoint = "https://api.themoviedb.org/3/"

def check_if_ready():
    """
    function to make sure that API is ready to process
    a new request
    :param count:
    :return:
    """

    header = requests.get(endpoint).headers

    while True:
        if "Retry-After" in header:
            print("Not ready")
            wait = header.get("Retry-After")
            time.sleep(int(wait) + 1)
        else:
            count = header.get("X-RateLimit-Remaining")
            return count
        header = requests.get(endpoint).headers



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


def get_actor_filmography(actor_id):

    response = requests.get(endpoint + "person/" + str(actor_id) + "/movie_credits?" + key).json()

    filmog = response.get("cast")

    films = {}

    for film in filmog:
        films.update({film.get("id"): film.get("title")})

    pprint(films)

# 50463

def get_cast(film_id):

    response = requests.get(endpoint + "movie/" + str(film_id) + "/credits?" + key).json()

    cast = response.get("cast")

    actors = {}

    for member in cast:
        if "character" in member:
            actor_name = member.get("name")
            actor_id = member.get("id")
            actors.update({actor_id: actor_name})

    pprint(actors)


# map from actor's ID to his/her name
id_to_name = {}

# map from movie's ID to title
id_to_movie = {}

# map from actor to all of his/her costars,
# as well as in which movie they costarred
actors_to_costars = {}


def get_costars(actor1):

    id1 = get_id_from_name(actor1)


    pass

check_if_ready()
# get_actor_filmography(get_id_from_name("Brad Pitt"))
get_cast(60308)