from datetime import datetime

from calculation.step_scan import step_scan
from dto.schemas import CoefficientSetup, CalculationResult


def calculate(cs: CoefficientSetup) -> CalculationResult:
    f = lambda t1, t2 : cs.a * (cs.g * cs.mu * ((t2 - t1) ** cs.n + (cs.beta * cs.a - t1) ** cs.n))

    limits = [
        lambda t1, t2: -3 <= t1 <= 3,
        lambda t1, t2: -2 <= t2 <= 6,
        lambda t1, t2: t1 - t2 >= -3
    ]

    max_t1, max_t2 = step_scan(f, limits, [0, 0], [-0.5, 0.5], 0.00001)
    max_value = f(max_t1, max_t2)

    calculation_result = CalculationResult(**(cs.__dict__ | {"t1": max_t1, "t2": max_t2, "s": max_value, "calculated_at": datetime.now()}))
    calculation_result.id = None

    return calculation_result
