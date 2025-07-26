def insert(heap, value):
	heap.append(value)
	index = len(heap) - 1
	while index > 0 and heap[(index - 1) // 2] > heap[index]:
		heap[index], heap[(index - 1) // 2] = heap[(index - 1) // 2], heap[index]
		index = (index - 1) // 2


def delete(heap, value):
	index = -1
	for i in range(len(heap)):
		if heap[i] == value:
			index = i
			break
	if index == -1:
		return
	heap[index] = heap[-1]
	heap.pop()
	while True:
		left_child = 2 * index + 1
		right_child = 2 * index + 2
		smallest = index
		if left_child < len(heap) and heap[left_child] < heap[smallest]:
			smallest = left_child
		if right_child < len(heap) and heap[right_child] < heap[smallest]:
			smallest = right_child
		if smallest != index:
			heap[index], heap[smallest] = heap[smallest], heap[index]
			index = smallest
		else:
			break

def main():
	import log
	
	heap = []
	values = [13, 16, 31, 41, 51, 100]
	for value in values:
		insert(heap, value)
	log.info(["Initial heap:", heap])
	
	delete(heap, 13)
	log.info(["Heap after deleting 13:", heap])
	
	delete(heap, 41)
	log.info(["Heap after deleting 41:", heap])
	
if __name__ == '__main__':
	main()
