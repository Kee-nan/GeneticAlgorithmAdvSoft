# individual.py
import json
from copy import deepcopy

# genes: dict mapping parameter names → test values.
# Example for two_sum: {'nums': [...], 'target': 9}
class Individual:
    def __init__(self, genes: dict):
        self.genes = genes
        self.fitness = None
        self.coverage = 0
        self.failures = 0
        self.detected_bug = False


    def __lt__(self, other):
        return self.fitness < other.fitness

    # Copy Helpers Return a deep clone of this entire individual.
    def copy(self) -> "Individual":
        return deepcopy(self)

    clone = copy  # alias (useful in GA engines)

    # Serialization / Logging - Serialize just the genes (no fitness metadata).
    def serialize(self) -> str:
        return json.dumps(self.genes)

    # Human readable, always safe.
    def pretty(self) -> str:
        return (
            f"Genes={self.genes}, "
            f"Fitness={self.fitness}, "
            f"Coverage={self.coverage}, "
            f"Bug={self.detected_bug}"
        )

    # Convenience for evaluator
    # Return genes in a form that can be passed directly as:
    # func(**individual.as_kwargs())
    def as_kwargs(self) -> dict:
        return self.genes

