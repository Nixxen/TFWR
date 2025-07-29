# Sort based on first value in the entity tuple, ascending
def selection_sort(entities):
	for i in range(len(entities)):
		min_index = i
		for j in range(i+1, len(entities)): 
			if entities[j][0] < entities[min_index][0]:
				min_index = j
		if min_index != i:
			temp = entities[i]
			entities[i] = entities[min_index]
			entities[min_index] = temp
	return entities

# Sort based on first value in the entity tuple, descending
def selection_sort_desc(entities):
	for i in range(len(entities)):
		max_index = i
		for j in range(i+1, len(entities)):
			if entities[j][0] > entities[max_index][0]:
				max_index = j
		if max_index != i:
			temp = entities[i]
			entities[i] = entities[max_index]
			entities[max_index] = temp
	return entities
	
# Returns the flattened field
# Optionally feed a ignore set of coordinates to skip
def get_flattened_values(grid, ignore = None):
	entities = []
	for pos in grid:
		if ignore and pos in ignore:
			continue
		entities.append((grid[pos], pos))
	return entities

# Returns a list of entities (val, pos) where val is the 
# highest value in the provided entities list
def get_highest_values(unsorted_entities):
	if not unsorted_entities:
		return []
	value = unsorted_entities[0][0]
	highest_value_entities = [unsorted_entities[0]]
	index = 1
	while index < len(unsorted_entities):
		if unsorted_entities[index][0] > value:
			highest_value_entities = [unsorted_entities[index]] # Reset list
			value = unsorted_entities[index][0]
		elif unsorted_entities[index][0] == value:
			highest_value_entities.append(unsorted_entities[index])
		index += 1
	return highest_value_entities

def copy_dict(original):
	new_dict = {}
	for key in original:
		new_dict[key] = original[key]
	return new_dict
	
# Returns the lowest of two items, or the first if the items are equal
# If neither item exist in Items, retusns None
def lowest_item(item_a, item_b):
	if item_a == item_b:
		return item_a # They are equal, assume order does not matter
	for item in Items:
		if item_a == item:
			return item_a
		if item_b == item:
			return item_b
	return None

# Returns true if item a is less than or equal to item b
def item_leq(item_a, item_b):
	return item_a == lowest_item(item_a, item_b)
	
# Reverses the input list in place
def reverse_list_in_place(list):
	start = 0
	end = len(list) - 1
	while start < end:
		temp = list[start]
		list[start] = list[end]
		list[end] = temp
		start += 1
		end -= 1

# Returns the key with the highest value in the dict
# Assumes the dict values are integers
def get_key_with_highest_value(dict):
	max_key = None
	max_value = -9999
	for key in dict:
		if dict[key] < max_value:
			continue
		max_value = dict[key]
		max_key = key
	return max_key
			

def main_highest_value():
	import log
	any_pos = (0,0)
	unsorted = [
		(1, any_pos),
		(1, any_pos),
		(2, any_pos),
		(2, any_pos),
		(3, any_pos),
		(3, any_pos),
		(9, any_pos),
		(9, any_pos),
		(9, any_pos),
		(8, any_pos),
		(8, any_pos),
		(7, any_pos)
	]
	log.info(["Unsorted: ", unsorted])
	
	highest = get_highest_values(unsorted)
	log.info(["Highest:", highest])

def main_reverse():
	import log
	
	list = [1, 2, 3, 1, 2, 3, 4]
	log.info(["Before reverse:", list])
	
	reverse_list_in_place(list)
	log.info(["After reverse:", list])

if __name__ == '__main__':
	#main_highest_value()
	main_reverse()
