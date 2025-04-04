
def binary_search_iterative(arr, target):
    """Binary Search using Iteration"""
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2 # Find the middle index

        if arr[mid] == target:
            return mid # Target found
        elif arr[mid] < target:
            left = mid + 1 # search the right half
        else:
            right = mid - 1 # search the left half
    
    return -1 # Target not found

def binary_search_recursive(arr, target, left, right):
    """Binary Search using Recursion"""
    if left > right:
        return -1 # Target not found
    
    mid = (left + right) // 2 # Find the middle index

    if arr[mid] == target:
        return mid # Target found
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right) # search the right half
    else:
        return binary_search_recursive(arr, target, left, mid - 1) # search the left half
    

if __name__ == "__main__":
    numbers = sorted([12, 3, 8, 15, 29, 42, 23, 6, 18, 31]) # Ensure the list is sorted
    print("Sorted Array:", numbers)

    target = int(input("Enter a number to search: "))

    # Iterative Binary Search
    result_iterative = binary_search_iterative(numbers, target)
    print(f"Iterative Search: {'Found at index' + str(result_iterative) if result_iterative != -1 else 'Not Found'}")

    # Recursive Search
    result_iterative = binary_search_recursive(numbers, target, 0, len(numbers) - 1)
    print(f"Recursive Search: {'Found at index' + str(result_iterative) if result_iterative != -1 else 'Not Found'}")

