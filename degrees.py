"""
Written by Joel Krim

This project uses The Movie Database (TMDb) REST API
Documentation: https://developers.themoviedb.org/3/getting-started/introduction
"""

import requests
import urllib.parse as ul
import time
import json
from copy import deepcopy
from pprint import pprint

key = "api_key=665e86f05c67c2031783a1a12386ece4"
endpoint = "https://api.themoviedb.org/3/"
status = "status_message"
cocast = "cocast.txt"
id_to_actor = "id_to_actor.txt"

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

    try:
        return response.get("results")[0].get("id")
    except:
        print("ERROR: The following name was either misspelled, or does not exist: ", name)
        exit()


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

    if cast is None:
        print("gotcha")

    actors = {}

    for member in cast:
        if "character" in member:
            actor_name = member.get("name")
            actor_id = member.get("id")
            actors.update({actor_id: actor_name})

    id_to_name = {}
    try:
        id_to_name = extract_json_from_file(id_to_actor)
    except:
        pass

    id_to_name.update(actors)
    write_out(id_to_name, id_to_actor)

    return actors

# map from movie's ID to title
# id_to_movie = {}


def get_costars(actor_id):

    filmog = get_actor_filmography(actor_id)

    costars = {}

    for film in filmog:
        # get cast of films
        cast = get_cast(film)
        # go through each actor in the cast
        for actor in cast:
            if str(actor_id) != str(actor):
                costars.update({actor: filmog.get(film)})
    data = {}
    try:
        data = extract_json_from_file(cocast)
    except:
        pass
    data.update({actor_id: costars})
    write_out(data, cocast)
    return costars


def target_in_costars(costars, target):
    if target in costars:
        return True
    else:
        return False


def extract_json_from_file(filename):
    return json.load(open(filename))


def write_out(data, filename):
    with open(filename, "w") as outfile:
        json.dump(data, outfile)

###############################################################
###############################################################

# get_costars("62")