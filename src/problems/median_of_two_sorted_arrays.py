# src/problems/median_of_two_sorted_arrays.py

# Correct version using binary search to find the median in O(log(min(n, m))) time.
def median_two_sorted_arrays_correct(nums1, nums2):
    A, B = nums1, nums2
    m, n = len(A), len(B)
    if m > n:
        A, B, m, n = B, A, n, m
    if n == 0:
        raise ValueError("Both arrays are empty")

    imin, imax, half_len = 0, m, (m + n + 1) // 2
    while imin <= imax:
        i = (imin + imax) // 2
        j = half_len - i
        if i < m and B[j-1] > A[i]:
            imin = i + 1
        elif i > 0 and A[i-1] > B[j]:
            imax = i - 1
        else:
            if i == 0: max_of_left = B[j-1]
            elif j == 0: max_of_left = A[i-1]
            else: max_of_left = max(A[i-1], B[j-1])

            if (m + n) % 2 == 1:
                return max_of_left

            if i == m: min_of_right = B[j]
            elif j == n: min_of_right = A[i]
            else: min_of_right = min(A[i], B[j])
            return (max_of_left + min_of_right) / 2.0

#######################################################################

# Buggy version — fails when arrays have different lengths or when one array is empty.
# Also may return wrong median when duplicates exist at boundaries.
def median_two_sorted_arrays_buggy(nums1, nums2):
    A, B = nums1, nums2
    m, n = len(A), len(B)
    if n == 0:
        return A[len(A)//2]  # Bug: wrong if len(A) is even

    # Bug: no swap to ensure A is smaller
    half_len = (m + n + 1) // 2
    for i in range(m + 1):
        j = half_len - i
        if i < m and j > 0 and B[j-1] > A[i]:
            continue
        elif i > 0 and j < n and A[i-1] > B[j]:
            continue
        else:
            if i == 0: max_of_left = B[j-1]
            elif j == 0: max_of_left = A[i-1]
            else: max_of_left = max(A[i-1], B[j-1])

            if (m + n) % 2 == 1:
                return max_of_left

            if i == m: min_of_right = B[j]
            elif j == n: min_of_right = A[i]
            else: min_of_right = min(A[i], B[j])
            return (max_of_left + min_of_right) / 2.0
