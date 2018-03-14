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
status = "status_message"

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

    response = requests.get(endpoint + "search/person?" + key + "&language=en-US&query=" + query).json()
    if status in response:
        check_if_ready()
        response = requests.get(endpoint + "search/person?" + key + "&language=en-US&query=" + query).json()

    id = response.get("results")[0].get("id")

    return id


def get_actor_filmography(actor_id):

    response = requests.get(endpoint + "person/" + str(actor_id) + "/movie_credits?" + key).json()
    if status in response:
        check_if_ready()
        response = requests.get(endpoint + "person/" + str(actor_id) + "/movie_credits?" + key).json()

    filmog = response.get("cast")

    films = {}

    for film in filmog:
        films.update({film.get("id"): film.get("title")})

    return films


def get_cast(film_id):

    response = requests.get(endpoint + "movie/" + str(film_id) + "/credits?" + key).json()
    if status in response:
        check_if_ready()
        response = requests.get(endpoint + "movie/" + str(film_id) + "/credits?" + key).json()

    cast = response.get("cast")

    actors = {}

    for member in cast:
        if "character" in member:
            actor_name = member.get("name")
            actor_id = member.get("id")
            actors.update({actor_id: actor_name})

    return actors


# map from actor's ID to his/her name
id_to_name = {}

# map from movie's ID to title
id_to_movie = {}

# map from actor to all of his/her costars,
# as well as in which movie they costarred
actors_to_costars = {}


def get_costars(actor1):

    id1 = get_id_from_name(actor1)

    filmog = get_actor_filmography(id1)

    costars = []

    for film in filmog:
        # get cast of films
        cast = get_cast(film)

        # go through each actor in the cast
        for actor in cast:
            # add to overall dict if need to
            if actor not in id_to_name:
                id_to_name.update(cast)
            if str(id1) != str(actor):
                costars.append(({actor: cast.get(actor)}, filmog.get(film)))
    actors_to_costars.update({id1: costars})
    return costars


def check_connection(actor1, actor2, path=[]):

    path.append(actor1)

    print(path)
    if actor1 == actor2:
        print("woo")
    if len(path) == 6:
        return

    id2 = get_id_from_name(actor2)

    costars = get_costars(actor1)
    for costar in costars:
        for key in costar[0]:
            actor = costar[0].get(key)
            if actor not in path:
                check_connection(actor, actor2, path)





def write_out():
    with open("actors.txt", "w") as outfile:
        json.dump(actors_to_costars, outfile)

#
# check_if_ready()
# # get_actor_filmography(get_id_from_name("Brad Pitt"))
# get_costars("Brad Pitt")

check_connection("Brad Pitt", "Margot Robbie")