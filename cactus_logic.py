import position
import static
import field
import algorithms
import poison_pill
import log
import debug

def plant_cactus(target_items, poison_pills):
	log.info(["Planting cactus until", target_items])
	
	def sort_cacti():
		def set_unlocked_values():
			for pos in field.value:
				if pos in field.locked:
					continue
				val = field.value[pos]
				if val not in unlocked_values:
					unlocked_values[val] = 1
					continue 
				unlocked_values[val] += 1
			
		def lock_valid_positions():
			def lock(pos):
				field.locked.add(pos)
				south = position.update(pos, South, False)
				west = position.update(pos, West, False)
				for dir in [south, west]:
					if dir != None and field.value[dir] > field.value[pos]:
						debug.dict(field.value, "Debug current value:", True)
						debug.set(field.locked, "Debug locked:", True)
						log.error(["Unexpected logic. Debug this"])
				val = field.value[pos]
				if not val in unlocked_values:
					debug.dict(field.value, "Unlocked error values:", True)
					debug.set(field.locked, "Unlocked error locked:", True)
					log.error(["Missing value", val, "in unlocked values:", unlocked_values])
				unlocked_values[val] -= 1
				if unlocked_values[val] <= 0:
					unlocked_values.pop(val)
			
			def higher_unlock_exist(_current):
				for _val in unlocked_values:
					if _val > _current:
						return True
				return False
			
			highest_value = field.get_highest_value()
			top_right = (static.world_size - 1, static.world_size - 1)
			if field.value[top_right] != highest_value:
				return # top right is not highest value. Skip checking the rest
			if top_right not in field.locked:
				lock(top_right)
			locked_last_pass = -1
			while len(field.locked) > locked_last_pass:
				locked_last_pass = len(field.locked)
				for pos in field.value:
					if pos in field.locked:
						continue
					current = field.value[pos]
					if higher_unlock_exist(current):
						continue # Higher unlocked value exist, skip lock
					# Check that north and east are higher or equal before locking
					east = position.update(pos, East, False)
					north = position.update(pos, North, False)
					northernmost_row = north == None
					easternmost_row = east == None
					north_locked = northernmost_row or (north in field.locked and field.value[north] >= current)
					east_locked = easternmost_row or (east in field.locked and field.value[east] >= current)
					if north_locked and east_locked:
						lock(pos)
						
		# Get moves greedily, starting at the top right, with the highest value. Working outwards based on distance
		def get_max_value_moves(unsorted_entities):
			def sort_by_distance_desc(target, entities):
				sorted = []
				distance_entities = []
				for entity in entities:
					distance = position.distance(target, entity[1])
					distance_entities.append((distance, entity[1]))
				sorted = algorithms.selection_sort_desc(distance_entities)
				restored_values = []
				for entity in sorted:
					corrected = (field.value[entity[1]], entity[1])
					restored_values.append(corrected)
				return restored_values
				
			def get_unlocked_positions():
				unlocked = []
				for pos in field.value:
					if pos in field.locked:
						continue
					unlocked.append((field.value[pos], pos))
				return unlocked

			fill_positions = get_unlocked_positions()
			if not fill_positions:
				log.warn("Unexpectedly few positions left")
				return []
			start_position = (static.world_size - 1, static.world_size - 1)
			fill_positions = sort_by_distance_desc(start_position, fill_positions)
			needed_moves = []  # List of (value, from_pos, to_pos)
			highest_entities = algorithms.get_highest_values(unsorted_entities)
			while highest_entities:
				next_fill_pos = fill_positions.pop()[1]
				highest_entities = sort_by_distance_desc(next_fill_pos, highest_entities)
				source_value, source_pos = highest_entities.pop()
				move = (source_value, source_pos, next_fill_pos)
				needed_moves.append(move)
			return needed_moves
		
		def move_cacti(needed_moves):
			def bubble(source, target):
				def get_direction(source, target):
					# Very intentional order. Move in directions without locks first
					if source[0] > target[0]:
						return West
					elif source[1] > target[1]:
						return South
					elif source[1] < target[1]:
						return North
					elif source[0] < target[0]:
						return East
					else:
						return None  # Already at destination
			            
				pos = source
				while pos != target:
					direction = get_direction(pos, target) # not using position.get_direction to allow for longer paths
					next_pos = position.update(pos, direction)
					if not next_pos:
						log.warn(["Invalid bubble direction from", pos, "to", target])
						return
					if next_pos in field.locked:
						log.warn(["Blocked by locked tile at", next_pos, field.value[next_pos], " when moving ", direction])
						debug.dict(field.value, "Debug current value:", True)
						debug.set(field.locked, "Debug locked:", True)
						return
									
					field.action(swap, direction)
					field.action(move, direction)
					field.swap(pos, next_pos)
					pos = position.update(pos, direction)
					
			sorted_moves_desc = algorithms.selection_sort_desc(needed_moves)
			for _, best_source, target_pos in sorted_moves_desc:
				position.go_to(best_source[0], best_source[1])
				bubble(best_source, target_pos)
				lock_valid_positions()
				
		def validate():
			for x in range(static.world_size):
				for y in range(static.world_size):
					val = field.value[(x, y)]
					east = position.update((x, y), East)
					north = position.update((x, y), North)
					if x > east[0]:
						east = (x, y)
					if y > north[1]:
						north = (x, y)
					east_val = field.value[east]
					north_val = field.value[north]
					if east_val and val > east_val:
						log.debug(["Validation failed at", (x, y), "-> east"])
						return False
					if north_val and val > north_val:
						log.debug(["Validation failed at", (x, y), "-> north"])
						return False
			return True
		
		
	
		while not validate():
			unlocked_values = {}
			field.locked = set() # TODO: Rework this to not reset locked on every pass
			set_unlocked_values()
			lock_valid_positions()
			while unlocked_values: # Clear one value of cacti at a time
				flattened_movable_entities = algorithms.get_flattened_values(field.value, field.locked)
				highest_values = algorithms.get_highest_values(flattened_movable_entities)
				debug.dict(field.value, "Debug current value:")
				lock_valid_positions() # Unlocked values are reduced here
				moves = get_max_value_moves(highest_values)
				debug.set(field.locked, "Debug locked:")
				debug.list(moves, "Moves debug:")
				move_cacti(moves)

	while num_items(Items.Cactus) < target_items:
		if poison_pill.triggered(poison_pills):
			break
		field.plant_field(Entities.Cactus, Grounds.Soil, True, False, False)
		sort_cacti()
		while not can_harvest():
			pass # In the unlikely event the cacti are not yet grown, burn some ticks
		pre_harvest = num_items(Items.Cactus)
		success = harvest()
		if not success:
			log.warn("Failed to harves cactus. Aborting")
			break
		log.info(["Successfully harvested Cactus for a gain of", num_items(Items.Cactus) - pre_harvest])
		
def main():
	change_hat(Hats.Straw_Hat)
	poison_pill = get_cost(Entities.Cactus)
	target_amount = 1000000
	plant_cactus(target_amount, poison_pill)

if __name__ == "__main__":
	main()	