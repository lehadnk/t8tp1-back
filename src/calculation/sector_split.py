from typing import Callable, List, Tuple


class SectorSplit: # NaBarabane
    def __init__(self) -> None:
        self.__f = None
        self.__limits = None
        self.__deltas = None

        self.__max_value_point = None
        self.__max_point_value = None

        self.__current_point = None

    def split_scan(self, f: Callable, limits: List[Callable], boundaries: List[Tuple[float]], deltas: list, min_delta: float) -> list:
        self.__f = f
        self.__limits = limits
        self.__deltas = deltas

        while True:
            self.__walk_through_array(boundaries)

            boundaries = [[self.__max_value_point[i] - self.__deltas[i], self.__max_value_point[i] + self.__deltas[i]] for i, v in enumerate(self.__deltas)]
            self.__deltas = [d * 0.5 for d in self.__deltas]

            if self.__deltas[0] <= min_delta:
                return self.__max_value_point


    def __walk_through_array(self, boundaries, index=[], dimension=0):
        if dimension == len(boundaries):
            if self.__is_point_exceeds_limits(index):
                return

            point_value = self.__f(*index)
            if self.__max_value_point is None or point_value > self.__max_point_value:
                self.__max_point_value = point_value
                self.__max_value_point = index.copy()
        else:
            i = boundaries[dimension][0]
            while i <= boundaries[dimension][1]:
                index.append(i)
                self.__walk_through_array(boundaries, index, dimension + 1)
                index.pop()
                i += self.__deltas[dimension]

    def __is_point_exceeds_limits(self, point: list) -> bool:
        for limit in self.__limits:
            if not limit(*point):
                return True

        return False
