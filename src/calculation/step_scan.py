from typing import Callable, List


def step_scan(f: Callable, limits: List[Callable], starting_point: list, delta: list, min_delta: float) -> list:
    point = starting_point
    for k, limit in enumerate(limits):
        if not limit(*point):
            raise Exception("Starting point {} is out of bounds for limit {}".format(point, k))

    point_value = f(*point)

    while True:
        for dimension_index in range(len(starting_point)):
            varying_point = point.copy()
            varying_point[dimension_index] += delta[dimension_index]
            varying_point_value = f(*varying_point)
            print("Point value is {} and varying point value is {}".format(point_value, varying_point_value))

            varying_point_exceeds_limit = False
            for k, limit in enumerate(limits):
                if not limit(*varying_point):
                    varying_point_exceeds_limit = True
                    print("Varying point {} is out of bounds for limit {}".format(varying_point, k))

            if varying_point_exceeds_limit or varying_point_value < point_value:
                # decrease step or whatever
                delta[dimension_index] = delta[dimension_index] * 0.5
                continue

            point = varying_point

        if sum([1 for d in delta if abs(d) < min_delta]) == len(delta):
            return point