# ga_engine.py

import random
from typing import Callable, Dict
from population import Population
from individual import Individual
from operators import init_random_individual, crossover_structured, mutate
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from coverage_utils import evaluate_individual


class GAEngine:
    def __init__(
        self,
        problem_id: str,
        population_size: int,
        generations: int,
        crossover_prob: float,
        mutation_prob: float,
        evaluator: Callable[[Individual], Dict],
        config: dict,
    ):
        self.problem_id = problem_id
        self.population_size = population_size
        self.generations = generations
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.evaluator = evaluator
        self.config = config
        self.archive = set()  # global archive for novelty

    def run(self) -> Dict:
        # Initialize population
        initial_individuals = [init_random_individual(self.problem_id, self.config) for _ in range(self.population_size)]
        population = Population(initial_individuals)
        history = []

        for gen in range(self.generations):
            population.evaluate(lambda ind: evaluate_individual(ind, self.problem_id, self.config.get("problem_map"), archive=self.archive)) ####

            # Elitism
            elite_count = self.config.get("elitism", 2)
            elites = population.get_elite(elite_count)
            print(f"\n--- Generation {gen} ---")
            print(f"Elites (top {elite_count}): {[e.fitness for e in elites]}")

            # Selection
            tournament_size = self.config.get("tournament_size", 5)
            num_to_select = self.population_size - len(elites)
            parents = population.select_tournament(k=num_to_select, tournament_size=tournament_size)
            print(f"Selected {len(parents)} parents for mating")

            # DEBUG: show first few parent args
            print("[DEBUG] Sample parents args (first 3):")
            for i, p in enumerate(parents[:3]):
                print(f"Parent {i}: args={p.as_kwargs()}")

            # Crossover & mutation
            children = []
            for i in range(0, len(parents), 2):
                parent_a = parents[i]
                parent_b = parents[i+1] if i+1 < len(parents) else parents[0]

                if random.random() < self.crossover_prob:
                    child_a, child_b = crossover_structured(parent_a, parent_b)
                else:
                    child_a, child_b = parent_a.copy(), parent_b.copy()

                child_a = mutate(child_a, self.problem_id, self.mutation_prob, self.config)
                child_b = mutate(child_b, self.problem_id, self.mutation_prob, self.config)


                children.extend([child_a, child_b])

            print(f"Generated {len(children)} children")
            # DEBUG: show first few children args
            print("[DEBUG] Sample children args (first 3):")
            for i, child in enumerate(children[:3]):
                print(f"Child {i}: args={child.as_kwargs()}")

            print("[DEBUG] Child types after crossover/mutation:")
            for i, child in enumerate(children[:5]):
                print(f"Child {i} type: {type(child)}, fitness: {child.fitness}, coverage: {child.coverage}")


            # New population
            new_individuals = elites + children[:self.population_size - len(elites)]
            population = Population(new_individuals)

            # Evaluate new population
            population.evaluate(lambda ind: self.evaluator(
                ind,
                self.problem_id,
                self.config.get("problem_map"),
                archive=self.archive
            ))

            # DEBUG: first few individuals after evaluation
            print(f"[DEBUG] After GA evaluation, Gen {gen} sample:")
            for i, ind in enumerate(population.individuals[:3]):
                print(f"Ind {i}: fitness={ind.fitness}, coverage={ind.coverage}, detected_bug={ind.detected_bug}")

            best_ind = max(population.individuals, key=lambda ind: ind.fitness or 0)
            avg_fitness = sum(ind.fitness or 0 for ind in population.individuals) / len(population.individuals)
            avg_coverage = sum(ind.coverage or 0 for ind in population.individuals) / len(population.individuals)
            bug_detections = sum(1 for ind in population.individuals if ind.detected_bug)

            history.append({
                "generation": gen,
                "best_fitness": best_ind.fitness,
                "best_coverage": best_ind.coverage,
                "avg_fitness": avg_fitness,
                "avg_coverage": avg_coverage,
                "bug_detections": bug_detections,
                "population": population.individuals.copy()
            })

            print(f"[GA] Gen {gen}: Best fitness={best_ind.fitness:.2f}, "
                  f"Best coverage={best_ind.coverage:.2f}, "
                  f"Bug detections={bug_detections}")

        best_overall = max(population.individuals, key=lambda ind: ind.fitness or 0)
        return {"best_individual": best_overall, "history": history}