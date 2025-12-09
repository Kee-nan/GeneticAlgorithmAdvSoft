# search_rotated.py

def search_rotated_correct(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if nums[mid] == target:
            return mid
        
        # Left half sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        
        # Right half sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
                
    return -1

#######################################################################


def search_rotated_buggy(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if nums[mid] == target:
            return mid
        
        # Bug: uses < instead of <= which breaks equal-bound cases
        if nums[left] < nums[mid]:
            if nums[left] <= target <= nums[mid]:  # bug: should be < mid
                right = mid - 1
            else:
                left = mid + 1
        
        else:
            # Bug: incorrect comparison flips search direction
            if nums[mid] <= target < nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1
