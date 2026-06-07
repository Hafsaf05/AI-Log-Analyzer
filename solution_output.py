def bubble_sort(numbers: list[int]) -> list[int]:
    """
    Sorts a list of integers in ascending order using the bubble sort algorithm.

    Args:
        numbers (list[int]): A list of integers to be sorted.

    Returns:
        list[int]: A sorted list of integers.

    Raises:
        TypeError: If the input list is None or contains non-integer elements.
        ValueError: If the input list is empty.

    Notes:
        This function has a worst-case and average time complexity of O(n²), which is inefficient for large lists.
        It modifies the input list copy in-place.
    """
    # Check if the input list is None or empty, or contains non-integer elements
    if numbers is None or not numbers:
        raise ValueError("Input list cannot be empty") if not numbers else raise TypeError("Input list cannot be None")
    if not all(isinstance(x, (int,)) for x in numbers):
        raise TypeError("Input list must contain only integers")

    # Create a copy of the input list to avoid modifying it in-place
    numbers = numbers.copy()

    # Iterate over the list until no more swaps are needed
    for i in range(len(numbers)):
        # Create a flag to track if any swaps occurred in the current pass
        swapped = False

        # Reduce the range of the inner loop by i in each iteration
        for j in range(len(numbers) - 1 - i):
            # If the current element is greater than the next one, swap them
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]  # Swap elements
                swapped = True  # Set the flag to indicate a swap occurred

        # If no swaps occurred in the current pass, the list is sorted
        if not swapped:
            break

    return numbers


def main() -> None:
    try:
        # Example usage
        numbers = [64, 34, 25, 12, 22, 11, 90]
        print("Original list:", numbers)
        print("Sorted list:", bubble_sort(numbers))
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()