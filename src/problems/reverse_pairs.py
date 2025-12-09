# src/problems/reverse_pairs.py

# Correct version using modified merge sort. Counts the number of pairs (i, j) such that i < j and nums[i] > 2*nums[j].
def reverse_pairs_correct(nums):
    
    def merge_sort(arr):
        if len(arr) <= 1:
            return arr, 0
        mid = len(arr) // 2
        left, count_left = merge_sort(arr[:mid])
        right, count_right = merge_sort(arr[mid:])
        count = count_left + count_right

        # Count reverse pairs
        j = 0
        for i in range(len(left)):
            while j < len(right) and left[i] > 2 * right[j]:
                j += 1
            count += j

        # Merge step
        sorted_arr = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                sorted_arr.append(left[i])
                i += 1
            else:
                sorted_arr.append(right[j])
                j += 1
        sorted_arr.extend(left[i:])
        sorted_arr.extend(right[j:])
        return sorted_arr, count

    _, total_count = merge_sort(nums)
    return total_count

#######################################################################

# Buggy version — fails to count pairs when elements are equal or duplicates exist, and may undercount reverse pairs at the boundaries.
def reverse_pairs_buggy(nums):

    def merge_sort(arr):
        if len(arr) <= 1:
            return arr, 0
        mid = len(arr) // 2
        left, count_left = merge_sort(arr[:mid])
        right, count_right = merge_sort(arr[mid:])
        count = count_left + count_right

        # Bug: using >= instead of > 2*nums[j], misses some pairs
        j = 0
        for i in range(len(left)):
            while j < len(right) and left[i] >= 2 * right[j]:
                j += 1
            count += j

        # Merge step (correct)
        sorted_arr = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                sorted_arr.append(left[i])
                i += 1
            else:
                sorted_arr.append(right[j])
                j += 1
        sorted_arr.extend(left[i:])
        sorted_arr.extend(right[j:])
        return sorted_arr, count

    _, total_count = merge_sort(nums)
    return total_count
