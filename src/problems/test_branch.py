# problems/test_branch.py

def test_branch_buggy(x: int) -> int:
    # Simple branch we can force to only go one way
    if x > 0:     # Branch A
        return 1
    else:         # Branch B
        return -1
