def heapify(arr, n, i):
	largest = i
	left  = 2 * i + 1
	right = 2 * i + 2
	
	if left < n and arr[left] > arr[largest]:
		largest = left
	
	if right < n and arr[right] > arr[largest]:
		largest = right
	
	if largest != i:
		arr[i], arr[largest] = arr[largest], arr[i]
		heapify(arr, n, largest)

# Heap Sort
def heap_sort(arr):
	n = len(arr)
	
	# Build max heap
	for i in range(n // 2 - 1, -1, -1):
		heapify(arr, n, i)
	
	# Extract elements one by one
	for i in range(n - 1, 0, -1):
		arr[0], arr[i] = arr[i], arr[0]  # Swap
		heapify(arr, i, 0)


# Example Usage
arr = [2, 8, 5, 3, 9, 1]
heap_sort(arr)
print("Sorted array is:", arr)
