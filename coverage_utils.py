# coverage_utils.py

import importlib.util
import sys
import os
from coverage import Coverage
import traceback
import time

from individual import Individual
from population import Population

# Evaluate function, this is key to getting our results 
def evaluate_individual(ind: Individual, problem_id: str, problem_map: dict, archive=None) -> dict:
    args = ind.as_kwargs().values()
    # print(f"[DEBUG] Running individual with args: {args}")

    try:
        # Get oracle for this problem
        oracle = problem_map[problem_id]["oracle"]
        try:
            expected = oracle(*args)
            oracle_success = True
        except Exception:
            oracle_success = False

        # Run the buggy function with coverage
        result = run_with_coverage(
            problem_map[problem_id]["module"],
            problem_map[problem_id]["func"],
            args=args
        )

        coverage = result.get("coverage", {}).get("percent", 0)

        # Determine failures using oracle comparison
        if not result["exec_success"]:
            failures = 1
        elif oracle_success and result["exec_success"] and result["output"] != expected:
            failures = 1
        else:
            failures = 0

        # print(f"[DEBUG] run_with_coverage result: coverage={coverage}, failures={failures}, exec_success={result.get('exec_success')}")

    except Exception as e:
        print(f"[EVAL-EXCEPTION] {e}")
        coverage = 0
        failures = 1

    # Fitness = coverage + 5 * failures (you can adjust weighting)
    failure_weight = 50
    fitness = coverage + (failure_weight * failures)
    ind.fitness = fitness
    ind.coverage = coverage
    ind.detected_bug = failures > 0

    # print(f"[DEBUG] Individual evaluated: fitness={fitness}, coverage={coverage}, detected_bug={ind.detected_bug}")

    return {
        "coverage": coverage,
        "failures": failures,
        "detected_bug": failures > 0,
        "fitness": fitness
    }


# Function to help us compute code coverage
def run_with_coverage(
        file_path: str,
        func_name: str,
        args=(),
        kwargs=None,
        branch=True,
):
    if kwargs is None:
        kwargs = {}
    file_path = os.path.abspath(file_path)
    module_name = f"cov_target_{os.path.basename(file_path).replace('.py','')}"
    if module_name in sys.modules:
        del sys.modules[module_name]

    cov = Coverage(branch=branch, include=[file_path])
    cov.start()
    exec_success = True
    output = None
    t0 = time.time()
    
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        func = getattr(module, func_name)
        output = func(*args, **kwargs)
    except Exception:
        exec_success = False
        output = traceback.format_exc()
    finally:
        cov.stop()
        cov.save()

    # Coverage analysis
    try:
        _, statements, missing, _ = cov.analysis(file_path)
        executed = sorted(set(statements) - set(missing))
        percent = 100.0 * len(executed) / len(statements) if statements else 0.0
    except Exception:
        statements, missing, executed, percent = [], [], [], 0.0

    return {
        "output": output,
        "exec_success": exec_success,
        "coverage": {
            "lines_total": len(statements),
            "executed": executed,
            "missing": missing,
            "percent": percent,
        },
        "timing_ms": (time.time() - t0) * 1000,
    }
