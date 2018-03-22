from pprint import pprint
import degrees as d

def check_connection(actor1, actor2):
    """
    BFS search to find shortest path
    from one actor to another
    :param actor1: start actor's name
    :param actor2: target actor's name
    :return:
    """

    data = {}
    try:
        data = d.extract_json_from_file(d.cocast)
    except:
        pass

    id1 = d.get_id_from_name(actor1)
    id2 = d.get_id_from_name(actor2)

    pred = {actor1: None}

    queue = [id1]

    count = 0

    while len(queue) > 0:
        current = queue.pop(0)
        costars = {}
        if str(current) in data:
            costars = data.get(str(current))
        else:
            costars = d.get_costars(str(current))
            print("\t\t\t Found someone new... ")
        if costars is not None:
            for costar in costars:
                id_to_name = d.extract_json_from_file(d.id_to_actor)
                name = id_to_name.get(str(costar))
                if name not in pred:
                    queue.append(costar)
                    id_to_name = d.extract_json_from_file(d.id_to_actor)
                    pred.update({name: (id_to_name.get(str(current)), costars.get(costar))})
                    if str(costar) == str(id2):
                        print("Found it")
                        path = []
                        curr = id_to_name.get(str(costar))
                        while pred.get(curr) is not None:
                            path.insert(0, (curr, pred.get(curr)[1]))
                            curr = pred.get(curr)[0]
                        path.insert(0, actor1)
                        print(path)
                        if len(path) > 6:
                            print("Could not do in 6 degrees or fewer")
                        return
        count += 1
        print("pass = ", count)
    print("Can't do it")


check_connection("John Wayne", "Margot Robbie")