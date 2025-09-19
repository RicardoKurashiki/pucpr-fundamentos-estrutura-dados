import time
import heapq
from collections import deque
from geopy.distance import geodesic


# --- Função Heurística (mantida) ---
def heuristic(node_coord, goal_coord):
    """Calcula a distância geodésica (em linha reta) entre dois pontos."""
    return geodesic(node_coord, goal_coord).km


# --- Nova Função Auxiliar para Reconstruir o Caminho ---
def reconstruct_path(came_from, current_id):
    """Reconstrói o caminho do final para o início usando o dicionário came_from."""
    path = [current_id]
    while current_id in came_from:
        current_id = came_from[current_id]
        path.insert(0, current_id)
    return path


# --- Algoritmos de Busca (Versão Corrigida) ---

def dijkstra(graph, start_id, goal_id):
    start_time = time.time()

    pq = [(0, start_id)]  # Fila de prioridade: (custo, id_no)
    came_from = {}
    cost_so_far = {start_id: 0}

    nodes_expanded = 0
    max_frontier_size = 1

    while pq:
        max_frontier_size = max(max_frontier_size, len(pq))
        cost, current_id = heapq.heappop(pq)

        nodes_expanded += 1

        if current_id == goal_id:
            path = reconstruct_path(came_from, current_id)
            return {
                "name": "Dijkstra", "path": path, "cost": round(cost, 2),
                "nodes_expanded": nodes_expanded, "max_frontier_size": max_frontier_size,
                "execution_time": time.time() - start_time
            }

        for neighbor_id in graph.get_neighbors(current_id):
            new_cost = cost_so_far[current_id] + graph.get_edge_weight(current_id, neighbor_id)
            if neighbor_id not in cost_so_far or new_cost < cost_so_far[neighbor_id]:
                cost_so_far[neighbor_id] = new_cost
                priority = new_cost
                heapq.heappush(pq, (priority, neighbor_id))
                came_from[neighbor_id] = current_id

    return None


def greedy_search(graph, start_id, goal_id):
    start_time = time.time()
    goal_node = graph.get_node(goal_id)

    pq = [(0, start_id)]  # Fila de prioridade: (heuristica, id_no)
    came_from = {}
    visited = {start_id}

    nodes_expanded = 0
    max_frontier_size = 1

    current_id = start_id
    while pq:
        max_frontier_size = max(max_frontier_size, len(pq))
        _, current_id = heapq.heappop(pq)
        nodes_expanded += 1

        if current_id == goal_id:
            path = reconstruct_path(came_from, current_id)
            cost = 0
            for i in range(len(path) - 1):
                cost += graph.get_edge_weight(path[i], path[i + 1])
            return {
                "name": "Greedy Search", "path": path, "cost": round(cost, 2),
                "nodes_expanded": nodes_expanded, "max_frontier_size": max_frontier_size,
                "execution_time": time.time() - start_time
            }

        for neighbor_id in graph.get_neighbors(current_id):
            if neighbor_id not in visited:
                visited.add(neighbor_id)
                came_from[neighbor_id] = current_id
                neighbor_node = graph.get_node(neighbor_id)
                h = heuristic(neighbor_node.coord, goal_node.coord)
                heapq.heappush(pq, (h, neighbor_id))

    return None


def a_star(graph, start_id, goal_id):
    start_time = time.time()
    goal_node = graph.get_node(goal_id)

    pq = [(0, start_id)]  # Fila de prioridade: (f_score, id_no)
    came_from = {}
    g_score = {node.id: float('inf') for node in graph.nodes}
    g_score[start_id] = 0

    nodes_expanded = 0
    max_frontier_size = 1

    while pq:
        max_frontier_size = max(max_frontier_size, len(pq))
        _, current_id = heapq.heappop(pq)
        nodes_expanded += 1

        if current_id == goal_id:
            path = reconstruct_path(came_from, current_id)
            return {
                "name": "A* Search", "path": path, "cost": round(g_score[current_id], 2),
                "nodes_expanded": nodes_expanded, "max_frontier_size": max_frontier_size,
                "execution_time": time.time() - start_time
            }

        for neighbor_id in graph.get_neighbors(current_id):
            tentative_g_score = g_score[current_id] + graph.get_edge_weight(current_id, neighbor_id)
            if tentative_g_score < g_score.get(neighbor_id, float('inf')):
                came_from[neighbor_id] = current_id
                g_score[neighbor_id] = tentative_g_score
                neighbor_node = graph.get_node(neighbor_id)
                h = heuristic(neighbor_node.coord, goal_node.coord)
                f_score = tentative_g_score + h
                heapq.heappush(pq, (f_score, neighbor_id))

    return None


# As funções de BFS e DFS não precisam de alteração
def depth_first_search(graph, start_id, goal_id):
    start_time = time.time()
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
                "name": "DFS", "path": path, "cost": round(cost, 2),
                "nodes_expanded": nodes_expanded, "max_frontier_size": max_frontier_size,
                "execution_time": time.time() - start_time
            }
        for neighbor_id in graph.get_neighbors(current_id):
            if neighbor_id not in visited:
                visited.add(neighbor_id)
                stack.append((neighbor_id, path + [neighbor_id]))
    return None


def breadth_first_search(graph, start_id, goal_id):
    start_time = time.time()
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
                "name": "BFS", "path": path, "cost": round(cost, 2),
                "nodes_expanded": nodes_expanded, "max_frontier_size": max_frontier_size,
                "execution_time": time.time() - start_time
            }
        for neighbor_id in graph.get_neighbors(current_id):
            if neighbor_id not in visited:
                visited.add(neighbor_id)
                queue.append((neighbor_id, path + [neighbor_id]))
    return None