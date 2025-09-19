import time
import heapq  # Biblioteca para implementar a fila de prioridade (min-heap)
from collections import deque  # Biblioteca para implementar a fila (queue) de forma eficiente
from geopy.distance import geodesic
import psutil  # Importado para medição de tempo de CPU
import tracemalloc # Importado para profiling de memória


# --- Função Heurística ---
def heuristic(node_coord, goal_coord):
    """
    Calcula a 'heurística', que é uma estimativa de custo do nó atual até o nó final.
    Neste caso, usamos a distância em linha reta (geodésica), que é uma boa estimativa
    para um mapa. Ela nunca superestima a distância real da estrada.
    """
    return geodesic(node_coord, goal_coord).km


# --- Função Auxiliar para Reconstruir o Caminho ---
def reconstruct_path(came_from, current_id):
    """
    Refaz o caminho do final para o início.
    O dicionário 'came_from' funciona como um "mapa de migalhas de pão",
    onde cada nó aponta para o nó de onde ele veio.
    """
    # Começamos pelo final
    path = [current_id]
    # Enquanto o nó atual estiver no nosso mapa 'came_from', significa que ele tem um "pai"
    while current_id in came_from:
        # O nó atual passa a ser o seu "pai", voltando um passo no caminho
        current_id = came_from[current_id]
        # Inserimos o "pai" no início da lista, para manter a ordem correta
        path.insert(0, current_id)
    return path


# --- Algoritmos de Busca ---

def dijkstra(graph, start_id, goal_id):
    """
    Algoritmo de Dijkstra: Encontra o caminho mais barato (menor custo) do início ao fim.
    Ele é "guloso" em relação ao custo JÁ percorrido. Sempre explora o nó com o menor
    custo acumulado desde o início.
    """
    # --- Início do Profiling ---
    process = psutil.Process()
    tracemalloc.start()
    cpu_time_start = process.cpu_times()

    # 1. Inicialização
    # Fila de prioridade (min-heap). Armazena (prioridade, id_do_no). A prioridade baixa sai primeiro.
    # A prioridade para Dijkstra é o custo total desde o início (g_score).
    pq = [(0, start_id)]

    # Dicionário para rastrear o caminho, guardando {id_filho: id_pai}
    came_from = {}

    # Dicionário para guardar o menor custo encontrado ATÉ AGORA para chegar em cada nó.
    cost_so_far = {start_id: 0}

    # Métricas
    nodes_expanded = 0
    max_frontier_size = 1

    path_found = None  # Variável para guardar o resultado
    # 2. Loop Principal
    # O loop continua enquanto houver nós na fronteira para serem explorados.
    while pq:
        # Atualiza o tamanho máximo que a fronteira já atingiu.
        max_frontier_size = max(max_frontier_size, len(pq))

        # Pega o nó da fronteira que tem o MENOR custo (menor prioridade). Esta é a essência do Dijkstra.
        cost, current_id = heapq.heappop(pq)

        nodes_expanded += 1

        # Se chegamos ao objetivo, a busca terminou!
        if current_id == goal_id:
            # Reconstrói o caminho e retorna os resultados.
            path_found = reconstruct_path(came_from, current_id)
            break # Encerra o loop ao encontrar o caminho

        # 3. Explorar Vizinhos
        # Para cada vizinho conectado ao nó atual...
        for neighbor_id in graph.get_neighbors(current_id):
            # Calcula o custo para chegar neste vizinho através do nó ATUAL.
            new_cost = cost_so_far[current_id] + graph.get_edge_weight(current_id, neighbor_id)

            # A CONDIÇÃO MAIS IMPORTANTE:
            # Se nunca visitamos esse vizinho OU encontramos um caminho MAIS BARATO para ele...
            if neighbor_id not in cost_so_far or new_cost < cost_so_far[neighbor_id]:
                # ...então registramos esse novo caminho como o melhor até agora.
                cost_so_far[neighbor_id] = new_cost
                priority = new_cost
                # E o adicionamos na fronteira para ser explorado no futuro.
                heapq.heappush(pq, (priority, neighbor_id))
                # E guardamos que chegamos a este vizinho a partir do nó atual.
                came_from[neighbor_id] = current_id

    # --- Fim do Profiling e Coleta de Métricas ---
    cpu_time_end = process.cpu_times()
    mem_peak = tracemalloc.get_traced_memory()[1] # Pega o valor de pico
    tracemalloc.stop()

    # Cálculo das métricas de performance
    cpu_time = (cpu_time_end.user - cpu_time_start.user) + (cpu_time_end.system - cpu_time_start.system)
    memory_peak_kb = round(mem_peak / 1024, 2)

    if path_found:
        return {
            "name": "Dijkstra", "path": path_found, "cost": round(cost_so_far[goal_id], 2),
            "nodes_expanded": nodes_expanded, "max_frontier_size": max_frontier_size,
            "cpu_time": cpu_time, "memory_peak_kb": memory_peak_kb
        }
    return None  # Se o loop terminar e não encontrarmos o objetivo, não há caminho.


def greedy_search(graph, start_id, goal_id):
    """
    Busca Gulosa (ou Ambiciosa): Tenta chegar o mais rápido possível no objetivo.
    Ele é "guloso" em relação ao futuro. Sempre escolhe o nó que PARECE estar mais
    perto do final, ignorando o custo que já teve para chegar até ali. É rápido, mas não garante o melhor caminho.
    """
    # --- Início do Profiling ---
    process = psutil.Process()
    tracemalloc.start()
    cpu_time_start = process.cpu_times()
    goal_node = graph.get_node(goal_id)

    # 1. Inicialização
    # A prioridade aqui é SÓ a heurística (distância em linha reta até o fim).
    pq = [(0, start_id)]
    came_from = {}
    visited = {start_id}  # Usamos um 'visited' simples pois não precisamos re-visitar nós.

    nodes_expanded = 0
    max_frontier_size = 1

    path_found = None
    # 2. Loop Principal
    while pq:
        max_frontier_size = max(max_frontier_size, len(pq))

        # Pega o nó que PARECE estar mais perto do objetivo.
        _, current_id = heapq.heappop(pq)
        nodes_expanded += 1

        if current_id == goal_id:
            path_found = reconstruct_path(came_from, current_id)
            break

        # 3. Explorar Vizinhos
        for neighbor_id in graph.get_neighbors(current_id):
            if neighbor_id not in visited:
                visited.add(neighbor_id)
                came_from[neighbor_id] = current_id
                neighbor_node = graph.get_node(neighbor_id)
                # A prioridade é a distância do VIZINHO até o FIM.
                h = heuristic(neighbor_node.coord, goal_node.coord)
                heapq.heappush(pq, (h, neighbor_id))

    cpu_time_end = process.cpu_times()
    mem_peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    cpu_time = (cpu_time_end.user - cpu_time_start.user) + (cpu_time_end.system - cpu_time_start.system)
    memory_peak_kb = round(mem_peak / 1024, 2)

    if path_found:
        cost = sum(graph.get_edge_weight(path_found[i], path_found[i + 1]) for i in range(len(path_found) - 1))
        return {
            "name": "Greedy Search", "path": path_found, "cost": round(cost, 2),
            "nodes_expanded": nodes_expanded, "max_frontier_size": max_frontier_size,
            "cpu_time": cpu_time, "memory_peak_kb": memory_peak_kb
        }
    return None


def a_star(graph, start_id, goal_id):
    """
    A* (A-Estrela): O melhor dos dois mundos. Combina a segurança do Dijkstra com a
    velocidade do Greedy. Ele avalia os nós usando uma soma:
    f_score = g_score + h_score
    g_score = custo real desde o início (o que o Dijkstra usa)
    h_score = custo estimado até o fim (o que o Greedy usa)
    """
    # --- Início do Profiling ---
    process = psutil.Process()
    tracemalloc.start()
    cpu_time_start = process.cpu_times()

    # --- Lógica do Algoritmo ---
    goal_node = graph.get_node(goal_id)

    # 1. Inicialização
    # A prioridade é o f_score (g_score + h_score).
    pq = [(0, start_id)]
    came_from = {}

    # g_score é o mesmo que o 'cost_so_far' do Dijkstra.
    g_score = {node.id: float('inf') for node in graph.nodes}
    g_score[start_id] = 0

    nodes_expanded = 0
    max_frontier_size = 1

    path_found = None
    # 2. Loop Principal (muito parecido com o Dijkstra)
    while pq:
        max_frontier_size = max(max_frontier_size, len(pq))

        # Pega o nó com o menor f_score (a melhor combinação de custo+heurística)
        _, current_id = heapq.heappop(pq)
        nodes_expanded += 1

        if current_id == goal_id:
            path_found = reconstruct_path(came_from, current_id)
            break

        # 3. Explorar Vizinhos
        for neighbor_id in graph.get_neighbors(current_id):
            # O cálculo do g_score (custo para chegar no vizinho) é igual ao do Dijkstra.
            tentative_g_score = g_score[current_id] + graph.get_edge_weight(current_id, neighbor_id)

            if tentative_g_score < g_score.get(neighbor_id, float('inf')):
                # Se encontramos um caminho melhor, atualizamos tudo.
                came_from[neighbor_id] = current_id
                g_score[neighbor_id] = tentative_g_score

                # A "mágica" do A* acontece aqui:
                neighbor_node = graph.get_node(neighbor_id)
                h = heuristic(neighbor_node.coord, goal_node.coord)
                f_score = tentative_g_score + h  # A prioridade combina o custo real com a estimativa.

                heapq.heappush(pq, (f_score, neighbor_id))

        # --- Fim do Profiling e Coleta de Métricas ---
        cpu_time_end = process.cpu_times()
        mem_peak = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()

        cpu_time = (cpu_time_end.user - cpu_time_start.user) + (cpu_time_end.system - cpu_time_start.system)
        memory_peak_kb = round(mem_peak / 1024, 2)

        if path_found:
            return {
                "name": "A* Search", "path": path_found, "cost": round(g_score[goal_id], 2),
                "nodes_expanded": nodes_expanded, "max_frontier_size": max_frontier_size,
                "cpu_time": cpu_time, "memory_peak_kb": memory_peak_kb
            }
        return None

def depth_first_search(graph, start_id, goal_id):
    """
    Busca em Profundidade (DFS): Explora um caminho até o mais fundo possível antes
    de voltar e tentar outro. Usa uma Pilha (Stack).
    Não é bom para achar caminhos mais curtos, mas é simples e usa pouca memória.
    """
    # --- Início do Profiling ---
    process = psutil.Process()
    tracemalloc.start()
    cpu_time_start = process.cpu_times()

    # Pilha (Stack LIFO - Último a entrar, primeiro a sair).
    # Armazena (id_do_no, caminho_feito_ate_aqui)
    stack = [(start_id, [start_id])]
    visited = {start_id}

    nodes_expanded = 0
    max_frontier_size = 1

    path_found = None
    while stack:
        max_frontier_size = max(max_frontier_size, len(stack))
        # .pop() remove o último item adicionado, o que causa o comportamento de "mergulhar fundo".
        current_id, path = stack.pop()
        nodes_expanded += 1

        if current_id == goal_id:
            path_found = path
            break

        for neighbor_id in graph.get_neighbors(current_id):
            if neighbor_id not in visited:
                visited.add(neighbor_id)
                # Adiciona o vizinho no topo da pilha. Ele será o próximo a ser explorado.
                stack.append((neighbor_id, path + [neighbor_id]))

    cpu_time_end = process.cpu_times()
    mem_peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    cpu_time = (cpu_time_end.user - cpu_time_start.user) + (cpu_time_end.system - cpu_time_start.system)
    memory_peak_kb = round(mem_peak / 1024, 2)

    if path_found:
        cost = sum(graph.get_edge_weight(path_found[i], path_found[i+1]) for i in range(len(path_found) - 1))
        return {
            "name": "Greedy Search", "path": path_found, "cost": round(cost, 2),
            "nodes_expanded": nodes_expanded, "max_frontier_size": max_frontier_size,
            "cpu_time": cpu_time, "memory_peak_kb": memory_peak_kb
        }
    return None


def breadth_first_search(graph, start_id, goal_id):
    """
    Busca em Largura (BFS): Explora todos os vizinhos de um nó antes de seguir
    para o próximo nível. Usa uma Fila (Queue).
    Garante o caminho com o MENOR NÚMERO DE ARESTAS, mas não necessariamente o menor custo.
    """
    # --- Início do Profiling ---
    process = psutil.Process()
    tracemalloc.start()
    cpu_time_start = process.cpu_times()

    # Fila (Queue FIFO - Primeiro a entrar, primeiro a sair).
    queue = deque([(start_id, [start_id])])
    visited = {start_id}

    nodes_expanded = 0
    max_frontier_size = 1

    path_found = None
    while queue:
        max_frontier_size = max(max_frontier_size, len(queue))
        # .popleft() remove o item mais antigo, o que causa a exploração "em camadas".
        current_id, path = queue.popleft()
        nodes_expanded += 1

        if current_id == goal_id:
            path_found = path
            break

        for neighbor_id in graph.get_neighbors(current_id):
            if neighbor_id not in visited:
                visited.add(neighbor_id)
                # Adiciona o vizinho no final da fila. Ele só será explorado depois de todos
                # os outros que já estavam lá.
                queue.append((neighbor_id, path + [neighbor_id]))

    cpu_time_end = process.cpu_times()
    mem_peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    cpu_time = (cpu_time_end.user - cpu_time_start.user) + (cpu_time_end.system - cpu_time_start.system)
    memory_peak_kb = round(mem_peak / 1024, 2)

    if path_found:
        cost = sum(graph.get_edge_weight(path_found[i], path_found[i + 1]) for i in range(len(path_found) - 1))
        return {
            "name": "BFS", "path": path_found, "cost": round(cost, 2),
            "nodes_expanded": nodes_expanded, "max_frontier_size": max_frontier_size,
            "cpu_time": cpu_time, "memory_peak_kb": memory_peak_kb
        }
    return None