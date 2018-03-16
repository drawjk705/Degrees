"""
Written by Joel Krim

This project uses The Movie Database (TMDb) REST API
Documentation: https://developers.themoviedb.org/3/getting-started/introduction
"""
from webbrowser import get

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

# map from movie's ID to title
# id_to_movie = {}


def get_costars(actor_id):

    # id1 = get_id_from_name(actor1)

    filmog = get_actor_filmography(actor_id)

    costars = {}

    id_to_name = {}
    try:
        id_to_name = extract_json_from_file(id_to_actor)
    except:
        pass

    for film in filmog:
        # get cast of films
        cast = get_cast(film)

        # go through each actor in the cast
        for actor in cast:
            # add to overall dict if need to
            if actor not in id_to_name:
                id_to_name.update(cast)
            if str(actor_id) != str(actor):
                costars.update({actor: cast.get(actor)})
                id_to_name.update({actor: cast.get(actor)})
    data = {}
    try:
        data = extract_json_from_file(cocast)
    except:
        pass
    data.update({actor_id: costars})
    write_out(data, cocast)
    write_out(id_to_name, id_to_actor)
    return costars


# add functionality to see the movies the 2 were in together
def check_connection(actor1, actor2, pass_num=0, path=[]):

    path.append(actor1)

    data = {}
    try:
        data = extract_json_from_file(cocast)
    except:
        pass
    # pprint(data)

    id1 = get_id_from_name(actor1)
    id2 = get_id_from_name(actor2)
    pprint(id2)

    costars = {}
    if str(id1) in data:
        costars = data.get(str(id1))
        pprint(costars)
    else:
        costars = get_costars(id1)
    if str(id2) in costars:
        path.append(actor2)
        print("HOORAY: ", path)
        return True

    for i in range(6 - pass_num):
        for costar in costars:
            if costars.get(costar) not in path:
                if check_connection(costars.get(costar), actor2, pass_num + 1, deepcopy(path)) is True:
                    return True




def extract_json_from_file(filename):
    return json.load(open(filename))


def write_out(data, filename):
    with open(filename, "w") as outfile:
        json.dump(data, outfile)

###############################################################
###############################################################

check_connection("Margot Robbie", "Joel Edgerton")