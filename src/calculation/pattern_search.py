from typing import Callable

def find_local_maximum(f: Callable, args_amount: int, starting_point: list, h: list, eps: float, decrease_h: bool):
    fp = f(*starting_point)

    varying_point = starting_point.copy()
    for i in range(0, args_amount):
        while True:
            varying_point1 = varying_point.copy()
            varying_point1[i] -= h[i]
            fp1 = f(*varying_point1)

            varying_point2 = varying_point.copy()
            varying_point2[i] += h[i]
            fp2 = f(*varying_point2)

            if fp1 > fp2 and fp1 > fp:
                varying_point = varying_point1
                if not decrease_h:
                    break

            if fp2 > fp1 and fp2 > fp:
                varying_point = varying_point2
                if not decrease_h:
                    break

            if decrease_h:
            # if fp > fp1 and fp > fp2 and decrease_h:
                h[i] = h[i] * 0.5

            if h[i] < eps or not decrease_h:
                break

    return varying_point

def adjust_point_if_exceeds_search_scope(p: list, min_values: list, max_values: list):
    for i in range(0, len(p)):
        if p[i] < min_values[i]:
            p[i] = min_values[i]
        if p[i] > max_values[i]:
            p[i] = max_values[i]

def find_maximum_md(f: Callable, args_amount: int, p: list, min_values: list, max_values: list, h: list, eps: float):
    """
    :param f: Testing function
    :param args_amount: Amount of variable parameters within the testing function
    :param p: Starting point coordinates
    :param h: List of starting step lengths per coordinate
    :param eps: Minimal step length
    :return:
    """

    points = [p, find_local_maximum(f, args_amount, p, h.copy(), eps, True)]
    print(points)

    iterations = 0
    while True:
        direction_vector = []
        for i in range(0, args_amount):
            direction_vector.append(round((points[len(points) - 1][i] - points[len(points) - 2][i]) * 2, 10))

        if direction_vector == [0 for x in range(0, args_amount)]:
            result = find_local_maximum(f, args_amount, points[len(points) - 1], h.copy(), eps, True)
            adjust_point_if_exceeds_search_scope(result, min_values, max_values)
            return result

        candidate_point = []
        for i in range(0, args_amount):
            coordinate_value = points[len(points) - 2][i] + direction_vector[i]
            candidate_point.append(coordinate_value)
            adjust_point_if_exceeds_search_scope(candidate_point, min_values, max_values)

        extremum_around_candidate_point = find_local_maximum(f, args_amount, candidate_point, h.copy(), eps, False)

        iterations += 1
        if candidate_point == extremum_around_candidate_point or iterations > 10000:
            result = find_local_maximum(f, args_amount, points[len(points) - 1], h.copy(), eps, True)
            adjust_point_if_exceeds_search_scope(result, min_values, max_values)
            return result
        else:
            points.append(extremum_around_candidate_point)
