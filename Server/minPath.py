"""Simple travelling salesman problem between cities."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print('Objective: {} miles'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Route distance: {}miles\n'.format(route_distance)

def getSolution(manager, routing, solution):
    RA = []
    index = routing.Start(0)
    while not routing.IsEnd(index):
        RA.append(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
    return RA

def main(distanceMatrix):
    """Entry point of the program."""
    # Instantiate the data problem.
    data = {}
    data["distance_matrix"] = distanceMatrix
    data['num_vehicles'] = 1
    data['depot'] = 0

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    return getSolution(manager,routing,solution)


if __name__ == '__main__':
    distanceMatrix = [[0, 2086, 3242, 3331, 9165, 24737, 25172, 19199],
                      [1156, 0, 1156, 3611, 10440, 26012, 26448, 10719],
                      [2312, 1156, 0, 2884, 8937, 24509, 24944, 9563],
                      [5400, 4244, 3518, 0, 5890, 22734, 23169, 11802],
                      [10778, 10212, 8795, 6327, 0, 18795, 19344, 13223],
                      [30372, 29806, 28389, 25921, 23532, 0, 18879, 33823],
                      [17645, 16489, 15333, 27188, 24790, 20628, 0, 14944],
                      [13536, 10572, 9416, 23135, 13391, 30161, 15128, 0], ]

    print(main(distanceMatrix))