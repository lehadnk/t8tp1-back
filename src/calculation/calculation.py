from datetime import datetime

from calculation.pattern_search import find_maximum_md
from dto.schemas import CoefficientSetup, CalculationResult


def calculate(cs: CoefficientSetup) -> CalculationResult:
    func = lambda t1, t2 : cs.a * (cs.g * cs.mu * ((t2 - t1) ** cs.n + (cs.beta * cs.a - t1) ** cs.n))
    max_t1, max_t2 = find_maximum_md(func, 2, [0, 0], [-3, -2], [3, 6], [0.1, 0.1], 0.001)
    max_value = func(max_t1, max_t2)

    calculation_result = CalculationResult(**(cs.__dict__ | {"t1": max_t1, "t2": max_t2, "s": max_value, "calculated_at": datetime.now()}))
    calculation_result.id = None

    return calculation_result
