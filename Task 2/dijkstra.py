import heapq
def dijkstra(graph, start_node):
    distances = {node: float('infinity') for node in graph}
    distances[start_node] = 0
    priority_queue = [(0, start_node)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

if __name__ == "__main__":
    study_graph = {
        'A': {'B': 4, 'C': 2},
        'B': {'C': 5, 'D': 10},
        'C': {'D': 3},
        'D': {}
    }

    start_point = 'A'
    result = dijkstra(study_graph, start_point)

    for node, dist in result.items():
        print(f"Node {node}: {dist}")