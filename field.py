import static
import position
import algorithms
import log

plants={}
infected={}
value={}
tilled={}
growing={}
multiplier={}
empty={}
locked = set()

for x in range(static.world_size):
	for y in range(static.world_size):
		pos = (x, y)
		plants[pos] = None
		infected[pos] = False
		value[pos] = None
		tilled[pos] = False
		growing[pos] = 0
		multiplier[pos] = 0
		empty[pos] = 0

		
def has_traversed_field():
	for pos in plants:
		if pos == None:
			return False
	return True

# Returns the highest value in field value
def get_highest_value():
	highest_value = 0
	for pos in value:
		if value[pos] and value[pos] > highest_value:
			highest_value = value[pos]
	return highest_value

# Returns the position with the highest value, along with the value.
# Or returns None if no positions have value
# Takes move cost into consideration
def get_highest_value_pos(drone_pos):
	highest_pos = None
	highest_value = 0
	for pos in value:
		move_cost = position.distance(drone_pos, pos)
		will_be_ready_to_harvest = (
			not growing[pos]
			or (growing[pos] - move_cost * static.action_time <= 0)
			)
		if value[pos] and will_be_ready_to_harvest and value[pos]>highest_value:
			highest_value = value[pos]
			highest_pos = pos
	return highest_pos, value[highest_pos]

# Similar to get_highest_value_pos, but returns the closest highest value
# with the lowest grow time (prioritize 0 growtime, then lowest)
def get_closest_highest_value_pos(drone_pos):
	highest_list_potential = []
	highest_value = 0
	for pos in value:
		if value[pos] and value[pos]>=highest_value:
			highest_value = value[pos]
			entity = (value[pos], pos)
			if not highest_list_potential:
				highest_list_potential.append(entity)
				continue
			while highest_list_potential[0][0] < highest_value:
				highest_list_potential.pop(0)
				if not highest_list_potential:
					break
			highest_list_potential.append(entity)
	# All entities in the list should have equal value
	closest_entity = None
	closest_distance = None
	grow_times = []
	for entity in highest_list_potential:
		grow_times.append((growing[entity[1]], entity))
	grow_times = algorithms.selection_sort(grow_times)
	for grow_time, entity in grow_times:
		distance = position.distance(drone_pos, entity[1], True)
		if not closest_entity:
			closest_entity = entity
			closest_distance = distance
			continue
		if distance < closest_distance:
			cosest_entity = entity
			closest_distance = distance
	return closest_entity

def update_growing():
	for pos in growing:
		if not growing[pos]:
			continue
		growing[pos] = max(0, growing[pos] - static.action_time)

def swap(source, target):
	swappable = [plants, infected, value, growing]
	log.debug(["Swapping positions: ", source, "->", target])
	for grid in swappable:
		if grid[source] == grid[target]:
			continue
		temp = grid[target]
		grid[target] = grid[source]
		grid[source] = temp
	
# Waters the ground and updates the growth multiplier of the position
def water(pos):
	water_items=num_items(Items.Water)
	water_level=get_water()
	multiplier[pos] = water_level*5
	if water_items<1:
		return
	
	expected_increase = 0.25
	water_target=1
	if water_level>(water_target-expected_increase):
		return
		
	water_to_use=max((water_target-water_level)/expected_increase, 1)
	success=action(use_item, Items.Water, min(water_to_use, water_items))
	if not success:
		return
	multiplier[pos] = get_water()*5

def action(task, arg1, arg2 = None):
	result = False
	if arg2:
		result = task(arg1, arg2)
	else:
		result = task(arg1)
	update_growing()
	return result

# Creates a distance map from source
def create_distance_map(source):
	distance_map = {}
	for x in range(static.world_size):
		for y in range(static.world_size):
			pos = (x, y)
			distance_map[pos] = position.distance(source, pos)
	return distance_map
	
def plant_field(plant_entity, ground_type, take_measurement = False, do_harvest = False):
	position.go_to(0, 0)
	for x in range(static.world_size):
		for y in range(static.world_size):
			pos = (x, y)
			if not tilled[pos]:
				if get_ground_type() != ground_type:
					till()
				tilled[pos] = True
			harvested = False
			growth_multiplier = water(pos)
			current_entity = get_entity_type()
			if current_entity and (current_entity != plant_entity):
				harvested = harvest() # Remove invalid entity without waiting for growth
			if do_harvest and not harvested and can_harvest():
				harvested = harvest()
			if harvested or not current_entity:
				action(plant, plant_entity)
			if take_measurement:
				value[pos] = measure()
			action(move, North)
		action(move, East)

def clear_field():
	position.go_to(0, 0)
	for x in range(static.world_size):
		for y in range(static.world_size):
			pos = (x, y)
			current_entity = get_entity_type()
			if current_entity:
				harvested = harvest() # Remove invalid entity without waiting for growth
			action(move, North)
		action(move, East)
		