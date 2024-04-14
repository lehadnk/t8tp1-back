from datetime import datetime

from calculation.sector_split import SectorSplit
from dto.schemas import CoefficientSetup, CalculationResult


def calculate(cs: CoefficientSetup) -> CalculationResult:
    def f(t1, t2):
        return cs.a * (cs.g * cs.mu * ((t2 - t1) ** cs.n + (cs.beta * cs.a - t1) ** cs.n))

    limits = [
        lambda t1, t2: -3 <= t1 <= 3,
        lambda t1, t2: -2 <= t2 <= 6,
        lambda t1, t2: t1 - t2 >= -3
    ]

    print("Starting calculation task: alpha: {} beta: {} mu: {} G: {} A: {} N: {}".format(cs.alpha, cs.beta, cs.mu, cs.g, cs.a, cs.n))
    ss = SectorSplit()
    max_t1, max_t2 = ss.split_scan(f, limits, [[-3, 3], [-2, 6]], [1, 1], 0.001)
    max_value = f(max_t1, max_t2)

    calculation_result = CalculationResult(**(cs.__dict__ | {"t1": max_t1, "t2": max_t2, "s": max_value, "calculated_at": datetime.now()}))
    calculation_result.id = None

    return calculation_result
