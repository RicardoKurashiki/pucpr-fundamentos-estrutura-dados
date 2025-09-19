from geopy.distance import geodesic
from graph import Graph

coords = {
    "Curitiba": {
        "id": 1,
        "coord": (-25.4284, -49.2733),
    },
    "Ponta Grossa": {
        "id": 2,
        "coord": (-25.095, -50.1619),
    },
    "Londrina": {
        "id": 3,
        "coord": (-23.3103, -51.1628),
    },
    "Maringa": {
        "id": 4,
        "coord": (-23.4205, -51.9331),
    },
    "Manoel Ribas": {
        "id": 5,
        "coord": (-24.5146, -51.6668),
    },
    "Cascavel": {
        "id": 6,
        "coord": (-24.9573, -53.459),
    },
    "São Mateus do Sul": {
        "id": 7,
        "coord": (-25.8687, -50.3841),
    },
    "Toledo": {
        "id": 8,
        "coord": (-24.7246, -53.7412),
    },
    "Araucária": {
        "id": 9,
        "coord": (-25.593, -49.4103),
    },
    "Foz do Iguaçú": {
        "id": 10,
        "coord": (-25.5469, -54.5882),
    },
}

roads = [
    ("Curitiba", "Araucária"),
    ("Curitiba", "Ponta Grossa"),
    ("Araucária", "Ponta Grossa"),
    ("Ponta Grossa", "São Mateus do Sul"),
    ("Ponta Grossa", "Manoel Ribas"),
    ("Manoel Ribas", "Maringa"),
    ("Maringa", "Londrina"),
    ("Maringa", "Cascavel"),
    ("Cascavel", "Toledo"),
    ("Toledo", "Foz do Iguaçú"),
]


def calculate_distance(coord1, coord2):
    return round(geodesic(coord1, coord2).km, 2)


def main():
    graph = Graph()
    for key, value in coords.items():
        graph.add_node(value["id"], key)

    for city1, city2 in roads:
        id1, id2 = coords[city1]["id"], coords[city2]["id"]
        dist = calculate_distance(coords[city1]["coord"], coords[city2]["coord"])
        graph.add_edge(id1, id2, dist)

    graph.show()


if __name__ == "__main__":
    main()
