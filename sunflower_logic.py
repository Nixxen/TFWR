import position
import static
import field
import poison_pill
import log
import debug
import pathfinding
import algorithms
import timer
import math

def plant_sunflower(target_items, poison_pills):
	log.info(["Planting sunflower until", target_items])
	
	def wipe_row(start_pos):
		pos = start_pos
		for x in range(static.world_size):
			max_value = debug.execute(field.get_highest_value)
			pre_harvest = num_items(Items.Power)
			harvested = harvest()
			post_harvest = num_items(Items.Power)
			if harvested:
				log.debug(["ROW WIPE: Harvested sunflower with value", field.value[pos], "/", max_value, ", gained", post_harvest - pre_harvest, Items.Power], True)
				plant(Entities.Sunflower)
				field.growing[pos] = average_sunflower_grow_time / field.multiplier[pos]
				field.value[pos] = measure()
			field.action(move, East)
			pos = position.update(pos, East)
	
	# Plants a random field and uses pathfinding to determine the best flowers to pick	
	# Reaches ~330 items per min at a ~1:1 harvest:cost convergence
	def highest_values_pathfinding():
		average_sunflower_grow_time = 5.6
		field.plant_field(Entities.Sunflower, Grounds.Soil, True)
	
		while num_items(Items.Power) < target_items:
			if poison_pill.triggered(poison_pills):
				break
			drone_pos = position.get_xy()
			positions = field.get_highest_value_pos_list()
			if not positions:
				log.warn("Value error, invalid positions. Unable to get high position list")
				break
			
			moves = pathfinding.greedy_wrapped_traversal(drone_pos, positions)
			skipped_due_to_growing = False
			available_moves = len(moves)
			while moves:
				move = moves.pop()
				position.go_to(move[0], move[1])
				drone_pos = move
				growth_multiplier = field.water(move)
				harvested = False
				if not can_harvest():
					log.debug(["Encountered a growing sunflower at pos", move, "with registered grow time of", field.growing[move]], True)
					skipped_due_to_growing = True
					continue # Skip growing sunflowers, though this should not happen
				max_value = debug.execute(field.get_highest_value)
				pre_harvest = num_items(Items.Power)
				harvested = harvest()
				post_harvest = num_items(Items.Power)
				if harvested:
					log.debug(["Harvested most valuable ready-to-harvest sunflower with value",
						field.value[move], "/", max_value, ", gained", post_harvest - pre_harvest, Items.Power])
					plant(Entities.Sunflower)
					field.growing[move] = average_sunflower_grow_time / field.multiplier[move]
					field.value[move] = measure()
			if skipped_due_to_growing and available_moves < 3:
				log.debug(["Too few valid sunflowers. Cleaning up one row to make space for more"])
				wipe_row()
			timer.checkpoint(Items.Power)
			timer.checkpoint(Items.Carrot)

	# Plants low value 7th across the board, then harvest a random flower and replant it until it reaches 7 again
	# moving in one column repeating the pattern.
	# The idea is that if every flower is a 7, then any flower is the highest value, and any flower above 7 will
	# also be the highest value, allowing us to harvest it until we reach a new 7.
	# Best algo: Reaches ~2650 items per min at a ~4.8:1 harvest:cost convergence
	def plant_low_value():
		def pre_plant_7s(start_pos):
			farm_grids = static.world_size
			required_for_bonus = 10
			required_columns = math.ceil((required_for_bonus + farm_grids) / farm_grids)
			for x in range(required_columns):
				for y in range(static.world_size):
					wrap_x = (x + start_pos[0]) % static.world_size
					wrap_y = (y + start_pos[1]) % static.world_size
					pos = (wrap_x, wrap_y)
					if not field.tilled[pos]:
						if get_ground_type() != Grounds.Soil:
							field.action(till)
						field.tilled[pos] = True
					field.water(pos)
					harvested = False
					current_entity = get_entity_type()
					if current_entity and (current_entity != plant_entity):
						harvested = field.action(harvest) # Remove invalid entity without waiting for growth
					if harvested or not current_entity:
						field.action(plant, plant_entity)
					field.value[pos] = measure()
					while field.value[pos] != lowest_value:
						field.action(harvest) # Not thinking about growth yet, just want a quick field
						field.action(plant, plant_entity)
						field.value[pos] = measure()
					field.action(move, North)
				if x != required_columns - 1:
					field.action(move, East)
			return pos
		
		plant_entity = Entities.Sunflower
		lowest_value = 7
		pos = position.get_xy()
		pos = pre_plant_7s(pos) # Theoretically this could fail due to too poison_pill not checked
		
		while num_items(Items.Power) < target_items:
			if poison_pill.triggered(poison_pills):
				break
			
			# Reaches ~2650 items per min at a ~4.8:1 harvest:cost convergence
			# Uses field actions, but we do not need it for this algo.
			# Sub-optimal to built_ins
			def field_action():
				field.water(pos)
				field.action(harvest)
				field.action(plant, plant_entity)
				field.value[pos] = measure()
				while field.value[pos] != lowest_value: # Theoretically this could fail if we are EXTREMELY unlucky
					field.action(use_item, Items.Fertilizer)
					field.action(use_item, Items.Weird_Substance)
					field.action(harvest)
					field.action(plant, plant_entity)
					field.action(use_item, Items.Fertilizer) # Undo surrounding fertilizer
					field.action(use_item, Items.Weird_Substance)
					field.action(harvest)
					field.action(plant, plant_entity)
					field.value[pos] = measure()
				field.action(move, North)
			
			# Reaches ~6060 items per min at a ~4.8:1 harvest:cost convergence
			def built_ins():
				field.water(pos)
				harvest()
				plant(plant_entity)
				while measure() != lowest_value: # Theoretically this could fail if we are EXTREMELY unlucky
					use_item(Items.Fertilizer)
					use_item(Items.Weird_Substance)
					harvest()
					plant(plant_entity)
					use_item(Items.Fertilizer) # Undo surrounding fertilizer
					use_item(Items.Weird_Substance)
					harvest()
					plant(plant_entity)
				move(North)
				
			built_ins()
			for item in gain_and_cost_items:
				if not timer.checkpoint(item, 10):
					break # Skip checking the rest as we are under the threshold

	gain_and_cost_items = [Items.Power, Items.Carrot, Items.Fertilizer, Items.Weird_Substance]
	for item in gain_and_cost_items:
		timer.start(item)
	#highest_values_pathfinding()
	plant_low_value()
	
	
		
		
		
		
		
def main():
	change_hat(Hats.Straw_Hat)
	poison_pill = get_cost(Entities.Sunflower)
	target_amount = 123123123
	plant_sunflower(target_amount, poison_pill)

if __name__ == "__main__":
	main()
