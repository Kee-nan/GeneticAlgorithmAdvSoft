#random_generator.py

import random
from typing import List, Tuple, Any

# ----------------------------
# Random input generators
# ----------------------------

# Test Branch Problem
def random_input_test_branch():
    """Always take the true branch."""
    return (random.randint(1, 100),)


def random_input_edit_distance() -> Tuple[str, str]:
    letters = 'abcdefghijklmnopqrstuvwxyz'
    s1 = ''.join(random.choices(letters, k=random.randint(0, 5)))
    s2 = ''.join(random.choices(letters, k=random.randint(0, 5)))

    # occasional substitution linking
    if random.random() < 0.2 and s1 and s2:
        idx1 = random.randint(0, len(s1)-1)
        idx2 = random.randint(0, len(s2)-1)
        s2 = s2[:idx2] + s1[idx1] + s2[idx2+1:]

    return (s1, s2)


def random_input_maximal_rectangle() -> Tuple[List[List[str]]]:
    rows = random.randint(0, 5)
    cols = random.randint(0, 5)
    matrix = []

    for _ in range(rows):
        if random.random() < 0.3:
            matrix.append([])
        else:
            matrix.append([random.choice(['0', '1']) for _ in range(cols)])

    return (matrix,)


def random_input_reverse_pairs() -> Tuple[List[int]]:
    n = random.randint(0, 12)
    nums = [random.randint(-20, 20) for _ in range(n)]

    if nums and random.random() < 0.3:
        nums.append(random.choice(nums))

    if random.random() < 0.2:
        nums.sort(reverse=True)

    if random.random() < 0.1:
        nums.sort()

    if random.random() < 0.1:
        nums = [0] * n

    return (nums,)


def random_input_median_two_arrays() -> Tuple[List[int], List[int]]:
    len1, len2 = random.randint(0, 6), random.randint(0, 6)
    arr1 = sorted(random.choices(range(-25, 25), k=len1))
    arr2 = sorted(random.choices(range(-25, 25), k=len2))

    if random.random() < 0.2:
        if random.random() < 0.5:
            arr1 = []
        else:
            arr2 = []

    if random.random() < 0.2:
        if arr1:
            arr1.append(random.choice(arr1))
        if arr2:
            arr2.append(random.choice(arr2))

    if random.random() < 0.1:
        max_len = max(len1, len2)
        arr1 = sorted(random.choices(range(-25, 25), k=max_len))
        arr2 = sorted(random.choices(range(-25, 25), k=max_len))

    return (arr1, arr2)


def random_input_search_rotated():
    # 10%: Empty array
    if random.random() < 0.1:
        return ([], random.randint(-50, 50))

    # Choose length
    n = random.randint(1, 20)

    # Create sorted base array
    arr = sorted(random.randint(-50, 50) for _ in range(n))

    # 30% chance: inject duplicates
    if random.random() < 0.3:
        for _ in range(random.randint(1, 3)):
            pos = random.randint(0, len(arr)-1)
            arr.insert(pos, arr[pos])

    # Force fully duplicated array (rare but important edge-case)
    if random.random() < 0.05:
        v = random.randint(-10, 10)
        arr = [v] * n

    # Choose pivot with bias toward special values
    if len(arr) > 1:
        if random.random() < 0.3:
            # strategic pivots for edge-case branches
            pivot = random.choice([0, 1, len(arr)//2, len(arr)-1])
        else:
            pivot = random.randint(0, len(arr)-1)
        arr = arr[pivot:] + arr[:pivot]

    # Decide target
    if random.random() < 0.6 and arr:
        # 60%: choose an element from array (guaranteed hit)
        target = random.choice(arr)

        # 20% of these: choose near-pivot element to hit boundary logic
        if random.random() < 0.2 and len(arr) > 1:
            pivot_neighbor = (pivot + random.choice([-1, 1])) % len(arr)
            target = arr[pivot_neighbor]
    else:
        # 40%: choose element NOT in array (miss case)
        target = random.randint(-100, 100)
        while target in arr:
            target = random.randint(-100, 100)

    return (arr, target)


def random_input_decode_ways():
    length = random.randint(0, 12)
    s = ''.join(str(random.randint(0, 9)) for _ in range(length))

    if random.random() < 0.2 and length > 0:
        s = '0' + s[1:]

    if random.random() < 0.2 and length > 0:
        pos = random.randint(0, length - 1)
        s = s[:pos] + "0" + s[pos+1:]

    if random.random() < 0.1 and length >= 2:
        s = "1" + s

    return (s,)


# ----------------------------
# Generic dispatcher
# ----------------------------
def generate_random_inputs(problem_name: str, n: int = 50) -> List[Tuple[Any]]:
    inputs = []
    for _ in range(n):
        if problem_name == 'test_branch':
            inputs.append(random_input_test_branch())
        elif problem_name == 'edit_distance':
            inputs.append(random_input_edit_distance())
        elif problem_name == 'maximal_rectangle':
            inputs.append(random_input_maximal_rectangle())
        elif problem_name == 'reverse_pairs':
            inputs.append(random_input_reverse_pairs())
        elif problem_name == 'median_two_arrays':
            inputs.append(random_input_median_two_arrays())
        elif problem_name == 'search_rotated':
            inputs.append(random_input_search_rotated())
        elif problem_name == 'decode_ways':
            inputs.append(random_input_decode_ways())
        
        else:
            raise ValueError(f"Unknown problem: {problem_name}")
    return inputs