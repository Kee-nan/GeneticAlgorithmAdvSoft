# operators.py
import random
from typing import Tuple
from individual import Individual

# Import ALL random input generators
from random_generator import (
    random_input_edit_distance,
    random_input_maximal_rectangle,
    random_input_reverse_pairs,
    random_input_median_two_arrays,
    random_input_search_rotated,
    random_input_decode_ways,
)


# Initilization (this is where we integrate all the problems )
def init_random_individual(problem_id: str, config: dict) -> Individual:
    """Create a random individual mapped to the required function arguments."""

    
    # Edit Distance
    # signature: minDistance(word1, word2)
    if problem_id == "edit_distance":
        s1, s2 = random_input_edit_distance()
        return Individual({"word1": s1, "word2": s2})

    
    # Maximal Rectangle
    # signature: maximalRectangle(matrix)
    elif problem_id == "maximal_rectangle":
        (matrix,) = random_input_maximal_rectangle()
        return Individual({"matrix": matrix})

    
    # Reverse Pairs
    # signature: reversePairs(nums)
    elif problem_id == "reverse_pairs":
        (nums,) = random_input_reverse_pairs()
        return Individual({"nums": nums})

    
    # Median of Two Sorted Arrays
    # signature: findMedianSortedArrays(nums1, nums2)
    elif problem_id == "median_two_arrays":
        nums1, nums2 = random_input_median_two_arrays()
        return Individual({"nums1": nums1, "nums2": nums2})

    
    # Search in Rotated Sorted Array
    # signature: search(nums, target)
    elif problem_id == "search_rotated":
        nums, target = random_input_search_rotated()
        return Individual({"nums": nums, "target": target})

    # Decode Ways
    # signature: numDecodings(s)
    elif problem_id == "decode_ways":
        (s,) = random_input_decode_ways()
        return Individual({"s": s})

    # FALLBACK (Safe default)
    else:
        return Individual({"value": random.randint(0, 100)})


# CROSSOVER
# Structured 2-point crossover with optional uniform crossover.
# uniform_prob: probability of doing uniform crossover instead of 2-point.
def crossover_structured(ind_a, ind_b, uniform_prob=0.5):
    A = ind_a.genes
    B = ind_b.genes
    new_ind1, new_ind2 = ind_a.copy(), ind_b.copy()

    # Uniform crossover occasionally
    if random.random() < uniform_prob:
        child1, child2 = {}, {}
        for key in A:
            if random.random() < 0.5:
                child1[key] = A[key]
                child2[key] = B[key]
            else:
                child1[key] = B[key]
                child2[key] = A[key]
        new_ind1.genes, new_ind2.genes = child1, child2
        return new_ind1, new_ind2

    # Structured 2-point crossover
    min_len = min(len(A), len(B))
    if min_len < 3:
        return new_ind1, new_ind2

    cut_points = sorted(random.sample(range(1, min_len), k=2))
    c1, c2 = cut_points
    child1 = A[:c1] + B[c1:c2] + A[c2:]
    child2 = B[:c1] + A[c1:c2] + B[c2:]

    new_ind1.genes, new_ind2.genes = child1, child2
    return new_ind1, new_ind2


# MUTATION
# Mutate genes with higher intensity and occasional radical mutations.
def mutate(ind: Individual, problem_id, mutation_prob, config, radical_prob=0.15):
    new = ind.copy()

    for key, val in new.genes.items():
        if random.random() > mutation_prob:
            continue

        # integer
        if isinstance(val, int):
            if random.random() < radical_prob:
                # completely random new int
                new.genes[key] = random.randint(-100, 100)
            else:
                new.genes[key] = val + random.randint(-20, 20)

        # float
        elif isinstance(val, float):
            if random.random() < radical_prob:
                new.genes[key] = random.uniform(-50.0, 50.0)
            else:
                new.genes[key] = val + random.uniform(-5.0, 5.0)

        # string
        elif isinstance(val, str):
            s = list(val)
            if random.random() < 0.3:
                s.insert(random.randint(0, len(s)), random.choice("abcdefghijklmnopqrstuvwxyz0123456789"))
            if len(s) > 1 and random.random() < 0.3:
                s.pop(random.randint(0, len(s)-1))
            for i in range(len(s)):
                if random.random() < 0.4:
                    s[i] = random.choice("abcdefghijklmnopqrstuvwxyz0123456789")
            new.genes[key] = ''.join(s)

        # list
        elif isinstance(val, list):
            L = val.copy()
            if random.random() < 0.4:
                L.append(random.randint(-50, 50))
            if len(L) > 1 and random.random() < 0.3:
                L.pop(random.randint(0, len(L)-1))
            for i in range(len(L)):
                if isinstance(L[i], int) and random.random() < 0.7:
                    if random.random() < radical_prob:
                        L[i] = random.randint(-100, 100)
                    else:
                        L[i] += random.randint(-20, 20)
                elif isinstance(L[i], list) and len(L[i]) > 0 and random.random() < 0.5:
                    j = random.randint(0, len(L[i])-1)
                    if isinstance(L[i][j], int):
                        L[i][j] += random.randint(-10, 10)
            new.genes[key] = L

        # tuple
        elif isinstance(val, tuple):
            T = list(val)
            for i in range(len(T)):
                if isinstance(T[i], int) and random.random() < 0.7:
                    if random.random() < radical_prob:
                        T[i] = random.randint(-100, 100)
                    else:
                        T[i] += random.randint(-20, 20)
            new.genes[key] = tuple(T)

    return new
