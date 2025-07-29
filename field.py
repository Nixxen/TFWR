import static
import position
import algorithms
import log
import debug

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

# Similar to get_highest_value_pos, but returns a list of highest values
# with the lowest grow time (consider 0 growtime only)
def get_highest_value_pos_list():
	highest_list_potential = []
	highest_value = 0
	for pos in value:
		if value[pos] and not growing[pos] and value[pos] >= highest_value:
			highest_value = value[pos]
			entity = (value[pos], pos)
			if not highest_list_potential:
				highest_list_potential.append(entity)
				continue
			if highest_list_potential[-1][0] < highest_value:
				highest_list_potential = [] # Lower value list, reset it
			highest_list_potential.append(entity)
	# All entities in the list should have equal value
	return highest_list_potential

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

def action(task, arg1 = None, arg2 = None):
	result = False
	if arg2:
		result = task(arg1, arg2)
	elif arg1:
		result = task(arg1)
	else:
		result = task()
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
	
def plant_field(plant_entity, ground_type, do_measurement = False, do_harvest = False, do_water = True):
	position.go_to(0, 0)
	for x in range(static.world_size):
		for y in range(static.world_size):
			pos = (x, y)
			if not tilled[pos]:
				if get_ground_type() != ground_type:
					action(till)
				tilled[pos] = True
			harvested = False
			if do_water:
				water(pos)
			current_entity = get_entity_type()
			if current_entity and (current_entity != plant_entity):
				harvested = action(harvest) # Remove invalid entity without waiting for growth
			if do_harvest and not harvested and can_harvest():
				harvested = action(harvest)
			if harvested or not current_entity:
				action(plant, plant_entity)
			if do_measurement:
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
		