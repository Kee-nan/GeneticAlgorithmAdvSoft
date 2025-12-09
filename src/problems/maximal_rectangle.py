# src/problems/maximal_rectangle.py

# Find the area of the largest rectangle of 1's in a binary matrix.
def maximal_rectangle_correct(matrix):
    if not matrix:
        return 0

    n_cols = len(matrix[0])
    heights = [0] * (n_cols + 1)
    max_area = 0

    for row in matrix:
        for i in range(n_cols):
            heights[i] = heights[i] + 1 if row[i] == "1" else 0

        stack = [-1]
        for i in range(n_cols + 1):
            while heights[i] < heights[stack[-1]]:
                h = heights[stack.pop()]
                w = i - stack[-1] - 1
                max_area = max(max_area, h * w)
            stack.append(i)

    return max_area

#######################################################################

# Buggy version — fails to handle empty rows and last element.
def maximal_rectangle_buggy(matrix):
    if not matrix:
        return 0

    n_cols = len(matrix[0])
    heights = [0] * n_cols
    max_area = 0

    for row in matrix:
        for i in range(n_cols):
            heights[i] = heights[i] + 1 if row[i] == "1" else 0

        stack = []
        for i in range(n_cols):
            # Bug: misses computation when stack not empty at end
            while stack and heights[i] < heights[stack[-1]]:
                h = heights[stack.pop()]
                w = i if not stack else i - stack[-1] - 1
                max_area = max(max_area, h * w)
            stack.append(i)

    return max_area
