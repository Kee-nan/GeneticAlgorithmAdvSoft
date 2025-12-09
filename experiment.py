# experiment.py

import os
import csv
from typing import Dict, Callable
import sys
sys.path.append(os.path.abspath("src/ga"))
from coverage_utils import run_with_coverage, evaluate_individual
from random_generator import generate_random_inputs
from ga_engine import GAEngine #Should work after setting python path


# Import the correct functions to act as oracle
from src.problems.edit_distance import edit_distance_correct
from src.problems.maximal_rectangle import maximal_rectangle_correct
from src.problems.reverse_pairs import reverse_pairs_correct
from src.problems.median_of_two_sorted_arrays import median_two_sorted_arrays_correct
from src.problems.search_rotated import search_rotated_correct
from src.problems.decode_ways import decode_ways_correct


# Problem Map
PROBLEMS_ROOT = "src/problems"

PROBLEM_MAP = {
    "edit_distance": {
        "module": f"{PROBLEMS_ROOT}/edit_distance.py",
        "func": "edit_distance_buggy",
        "oracle": edit_distance_correct,
    },
    "maximal_rectangle": {
        "module": f"{PROBLEMS_ROOT}/maximal_rectangle.py",
        "func": "maximal_rectangle_buggy",
        "oracle": maximal_rectangle_correct,
    },
    "reverse_pairs": {
        "module": f"{PROBLEMS_ROOT}/reverse_pairs.py",
        "func": "reverse_pairs_buggy",
        "oracle": reverse_pairs_correct,
    },
    "median_two_arrays": {
        "module": f"{PROBLEMS_ROOT}/median_of_two_sorted_arrays.py",
        "func": "median_two_sorted_arrays_buggy",
        "oracle": median_two_sorted_arrays_correct,
    },
    "search_rotated": {
        "module": f"{PROBLEMS_ROOT}/search_rotated.py",
        "func": "search_rotated_buggy",
        "oracle": search_rotated_correct,
    },
    "decode_ways": {
        "module": f"{PROBLEMS_ROOT}/decode_ways.py",
        "func": "decode_ways_buggy",
        "oracle": decode_ways_correct,
    },
}


# Random Test Runner
def run_random_trial(problem_id: str, n_inputs: int = 10):
    if problem_id not in PROBLEM_MAP:
        raise ValueError(f"Unknown problem: {problem_id}")

    entry = PROBLEM_MAP[problem_id]
    module_path = entry["module"]
    func_name = entry["func"]
    oracle = entry["oracle"]

    inputs = generate_random_inputs(problem_id, n=n_inputs)
    coverage_values = []
    failures = 0

    for args in inputs:
        # Compute oracle - correct version
        try:
            expected = oracle(*args)
            oracle_success = True
        except Exception:
            oracle_success = False

        # Run buggy version
        buggy = run_with_coverage(module_path, func_name, args=args)

        # Check failures
        if not buggy["exec_success"]:
            failures += 1
            continue

        coverage_values.append(buggy["coverage"]["percent"])

        # Logic bug detection
        if oracle_success and buggy["exec_success"]:
            if buggy["output"] != expected:
                failures += 1

    avg_cov = sum(coverage_values) / len(coverage_values) if coverage_values else 0.0

    return {
        "avg_coverage": avg_cov,
        "failures": failures,
        "n_tests": len(inputs),
    }


# GA Test Runner
def run_ga_trial(problem_id: str, ga_params: Dict, evaluator: Callable = None):
    
    if evaluator is None:
        evaluator = lambda ind, pid, pmap, archive=None: evaluate_individual(
            ind, pid, pmap, archive=archive
        )

    cfg = ga_params.get("config", {})
    cfg["problem_map"] = PROBLEM_MAP  

    ga = GAEngine(
        problem_id=problem_id,
        population_size=ga_params.get('population_size', 50),
        generations=ga_params.get('generations', 10),
        crossover_prob=ga_params.get('crossover_prob', 0.7),
        mutation_prob=ga_params.get('mutation_prob', 0.3),
        evaluator=evaluator,
        config=cfg
    )

    results = ga.run()
    last_gen = results['history'][-1]

    return {
    "avg_coverage": sum(gen["avg_coverage"] for gen in results["history"]) / len(results["history"]),
    "failures": results["total_failures"],  # cumulative across generations
    "n_tests": ga_params.get('population_size', 50) * ga_params.get('generations', 10)
    }

# Comparison Runner
def run_comparison(
    problem_id: str,
    trials: int = 3,
    ga_params: dict = None,
    random_params: dict = None,
    evaluator: Callable = None,
    output_dir: str = "results"
) -> Dict:

    # For fair comparison, generations * Popsize should always  = n_inputs in random
    if ga_params is None:
        ga_params = {"population_size": 50, "generations": 5} # Can change these variables

    if random_params is None:
        random_params = {"n_inputs": 250} #Can change this variable

    os.makedirs(output_dir, exist_ok=True)
    all_results = []

    for t in range(1, trials + 1):
        print(f"=== Trial {t} for problem {problem_id} ===")

        # Random Search
        random_result = run_random_trial(problem_id, random_params["n_inputs"])
        print("Random:", random_result)

        # GA Search
        ga_result = run_ga_trial(problem_id, ga_params, evaluator=evaluator)
        print("GA:", ga_result)

        trial_result = {
            "trial": t,
            "problem": problem_id,
            "random_avg_coverage": random_result["avg_coverage"],
            "random_failures": random_result["failures"],
            "random_n_tests": random_result["n_tests"],
            "ga_avg_coverage": ga_result['avg_coverage'],
            "ga_failures": ga_result['failures'],
            "ga_n_tests": ga_result['n_tests'],
        }

        all_results.append(trial_result)

    # Save to CSV ion results directory
    csv_path = os.path.join(output_dir, f"{problem_id}_comparison.csv")
    keys = list(all_results[0].keys()) if all_results else []
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in all_results:
            writer.writerow(row)
    print(f"Saved CSV to {csv_path}")

    return {"trials": trials, "results": all_results}


# Main
# This is where the code enters when we run
if __name__ == "__main__":
    # Add whatever problems you want to run here
    problem_ids = [
        "edit_distance", "decode_ways", "maximal_rectangle"
    ]
    for pid in problem_ids:
        print(f"\n=== Running comparison for: {pid} ===")
        run_comparison(pid, trials=5)

# "search_rotated", "median_two_arrays"