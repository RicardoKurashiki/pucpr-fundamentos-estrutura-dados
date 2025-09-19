import time
import heapq
from collections import deque
from geopy.distance import geodesic


# --- Função Heurística (Distância em linha reta) ---
# Usada pelo Greedy e A*
def heuristic(node_coord, goal_coord):
    """Calcula a distância geodésica (em linha reta) entre dois pontos."""
    return geodesic(node_coord, goal_coord).km


def reconstruct_path(came_from, current_id):
    """Reconstrói o caminho a partir do dicionário came_from."""
    path = [current_id]
    while current_id in came_from:
        current_id = came_from[current_id]
        path.insert(0, current_id)
    return path


# --- Algoritmos de Busca ---

def dijkstra(graph, start_id, goal_id):
    start_time = time.time()

    # Fila de prioridade: (custo, id_no, caminho)
    pq = [(0, start_id, [])]
    visited = set()

    # Métricas
    nodes_expanded = 0
    max_frontier_size = 1

    while pq:
        max_frontier_size = max(max_frontier_size, len(pq))

        cost, current_id, path = heapq.heappop(pq)

        if current_id in visited:
            continue

        visited.add(current_id)
        nodes_expanded += 1

        new_path = path + [current_id]

        if current_id == goal_id:
            return {
                "name": "Dijkstra",
                "path": new_path,
                "cost": round(cost, 2),
                "nodes_expanded": nodes_expanded,
                "max_frontier_size": max_frontier_size,
                "execution_time": time.time() - start_time
            }

        for neighbor_id in graph.get_neighbors(current_id):
            if neighbor_id not in visited:
                weight = graph.get_edge_weight(current_id, neighbor_id)
                heapq.heappush(pq, (cost + weight, neighbor_id, new_path))

    return None  # Caminho não encontrado


def greedy_search(graph, start_id, goal_id):
    start_time = time.time()
    goal_node = graph.get_node(goal_id)

    # Fila de prioridade: (heuristica, id_no, caminho_ate_agora, custo_ate_agora)
    pq = [(0, start_id, [], 0)]
    visited = set()

    nodes_expanded = 0
    max_frontier_size = 1

    while pq:
        max_frontier_size = max(max_frontier_size, len(pq))

        _, current_id, path, cost = heapq.heappop(pq)

        if current_id in visited:
            continue

        visited.add(current_id)
        nodes_expanded += 1

        new_path = path + [current_id]

        if current_id == goal_id:
            return {
                "name": "Greedy Search",
                "path": new_path,
                "cost": round(cost, 2),
                "nodes_expanded": nodes_expanded,
                "max_frontier_size": max_frontier_size,
                "execution_time": time.time() - start_time
            }

        for neighbor_id in graph.get_neighbors(current_id):
            if neighbor_id not in visited:
                neighbor_node = graph.get_node(neighbor_id)
                h = heuristic(neighbor_node.coord, goal_node.coord)
                weight = graph.get_edge_weight(current_id, neighbor_id)
                heapq.heappush(pq, (h, neighbor_id, new_path, cost + weight))

    return None


def a_star(graph, start_id, goal_id):
    start_time = time.time()
    goal_node = graph.get_node(goal_id)

    # Fila de prioridade: (f_score, g_score, id_no, caminho)
    # f_score = g_score + h_score
    pq = [(0, 0, start_id, [])]
    visited = set()

    nodes_expanded = 0
    max_frontier_size = 1

    while pq:
        max_frontier_size = max(max_frontier_size, len(pq))

        f_score, g_score, current_id, path = heapq.heappop(pq)

        if current_id in visited:
            continue

        visited.add(current_id)
        nodes_expanded += 1

        new_path = path + [current_id]

        if current_id == goal_id:
            return {
                "name": "A* Search",
                "path": new_path,
                "cost": round(g_score, 2),
                "nodes_expanded": nodes_expanded,
                "max_frontier_size": max_frontier_size,
                "execution_time": time.time() - start_time
            }

        for neighbor_id in graph.get_neighbors(current_id):
            if neighbor_id not in visited:
                weight = graph.get_edge_weight(current_id, neighbor_id)
                new_g_score = g_score + weight

                neighbor_node = graph.get_node(neighbor_id)
                h = heuristic(neighbor_node.coord, goal_node.coord)
                new_f_score = new_g_score + h

                heapq.heappush(pq, (new_f_score, new_g_score, neighbor_id, new_path))
    return None


def depth_first_search(graph, start_id, goal_id):
    start_time = time.time()

    # Pilha (Stack): (id_no, caminho_ate_agora)
    stack = [(start_id, [start_id])]
    visited = {start_id}

    nodes_expanded = 0
    max_frontier_size = 1

    while stack:
        max_frontier_size = max(max_frontier_size, len(stack))
        current_id, path = stack.pop()
        nodes_expanded += 1

        if current_id == goal_id:
            cost = 0
            for i in range(len(path) - 1):
                cost += graph.get_edge_weight(path[i], path[i + 1])
            return {
                "name": "DFS",
                "path": path,
                "cost": round(cost, 2),
                "nodes_expanded": nodes_expanded,
                "max_frontier_size": max_frontier_size,
                "execution_time": time.time() - start_time
            }

        for neighbor_id in graph.get_neighbors(current_id):
            if neighbor_id not in visited:
                visited.add(neighbor_id)
                stack.append((neighbor_id, path + [neighbor_id]))

    return None


def breadth_first_search(graph, start_id, goal_id):
    start_time = time.time()

    # Fila (Queue): (id_no, caminho_ate_agora)
    queue = deque([(start_id, [start_id])])
    visited = {start_id}

    nodes_expanded = 0
    max_frontier_size = 1

    while queue:
        max_frontier_size = max(max_frontier_size, len(queue))
        current_id, path = queue.popleft()
        nodes_expanded += 1

        if current_id == goal_id:
            cost = 0
            for i in range(len(path) - 1):
                cost += graph.get_edge_weight(path[i], path[i + 1])
            return {
                "name": "BFS",
                "path": path,
                "cost": round(cost, 2),
                "nodes_expanded": nodes_expanded,
                "max_frontier_size": max_frontier_size,
                "execution_time": time.time() - start_time
            }

        for neighbor_id in graph.get_neighbors(current_id):
            if neighbor_id not in visited:
                visited.add(neighbor_id)
                queue.append((neighbor_id, path + [neighbor_id]))

    return None