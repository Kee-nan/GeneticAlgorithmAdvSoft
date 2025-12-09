# population.py
import random
from typing import List, Callable
from individual import Individual

class Population:
    def __init__(self, individuals: List[Individual]):
        self.individuals = individuals

# Evaluation
# Runs evaluate_individual for each, well, indicidual 
    def evaluate(self, evaluator: Callable[[Individual], dict], verbose=True) -> None:

        for i, ind in enumerate(self.individuals):
            if not isinstance(ind, Individual):
                print(f"[EVAL-ERROR] Non-Individual in population: {type(ind)}")
                continue

            try:
                result = evaluator(ind)

                # REQUIRED FIELDS
                ind.fitness = float(result.get("fitness", 0))
                ind.coverage = float(result.get("coverage", 0))
                ind.failures = int(result.get("failures", 0))
                ind.detected_bug = bool(result.get("detected_bug", ind.failures > 0))

                # DEBUG: print first 3 individuals per generation
                if i < 3:
                    print(f"[POP-EVAL DEBUG] Ind {i}: fitness={ind.fitness}, coverage={ind.coverage}, "
                        f"failures={ind.failures}, detected_bug={ind.detected_bug}")

            except Exception as e:
                # Catastrophic evaluator failure → treat as bad individual
                ind.fitness = 0
                ind.coverage = 0
                ind.failures = 0
                ind.detected_bug = True
                if verbose:
                    print(f"[EVAL-ERROR] {e}")

    # Selection Methods - Tournament selection (higher fitness wins).
    def select_tournament(self, k: int, tournament_size: int) -> List[Individual]:
        selected = []
        for _ in range(k):
            tournament = random.sample(self.individuals, tournament_size)
            winner = max(tournament, key=lambda ind: ind.fitness or 0)
            selected.append(winner.copy())
        return selected

    # Roulette-wheel / fitness-proportionate selection.
    def select_roulette(self, k: int) -> List[Individual]:
        fitnesses = [(ind.fitness or 0) for ind in self.individuals]
        total = sum(fitnesses)

        # fallback if all fitness = 0
        if total == 0:
            return [random.choice(self.individuals).copy() for _ in range(k)]

        selected = []
        for _ in range(k):
            pick = random.uniform(0, total)
            current = 0
            for ind, fit in zip(self.individuals, fitnesses):
                current += fit
                if current >= pick:
                    selected.append(ind.copy())
                    break
        return selected

    # Elitism - Return top-n individuals by fitness.
    def get_elite(self, n: int) -> List[Individual]:
        sorted_inds = sorted(
            self.individuals,
            key=lambda ind: ind.fitness or 0,
            reverse=True,
        )
        return [ind.copy() for ind in sorted_inds[:n]]
