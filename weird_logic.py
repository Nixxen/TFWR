import position
import static
import field
import poison_pill
import log
import debug
import timer

def plant_grass_fertilize(target_items, poison_pills):
	log.info(["Fertilizing hay until", target_items])
	
	# Plants a cross pattern of grass, repeatedly iterating through the 5 positions
	# attempting to optimize the gain of weird substance.
	# Reaches ~6700 items per min at a ~11:1 harvest:cost convergence
	def plant_cross_pattern():
		def pre_plant_cross(start_pos):
			pos = start_pos
			for index in range(len(moves)):
				pos = position.update(pos, moves[index])
				field.action(move, moves[index])
				if index % 2 == 0 and index != 0:
					continue
				field.water(pos)
				harvested = False
				current_entity = get_entity_type()
				if current_entity and (current_entity != plant_entity):
					harvested = field.action(harvest) # Remove invalid entity without waiting for growth
				if harvested or not current_entity:
					field.action(plant, plant_entity)
					field.action(use_item, Items.Fertilizer)
			return pos
		
		def harvest_cross():
			for dir in moves:
				field.action(move, dir)
				harvest()
				if get_ground_type() == Grounds.Grassland:
					till()
		
		clear()
		plant_entity = Entities.Bush # Hay is too fast
		planting_center = (2, 2)
		start_pos = position.update(planting_center, South)
		position.go_to(start_pos[0], start_pos[1])
		moves = [North, East, West, North, South, West, East, South]
		harvest_cross()
		pos = pre_plant_cross(planting_center)
		
		while num_items(Items.Weird_Substance) < target_items:
			if poison_pill.triggered(poison_pills):
				break
			field.water(pos) # Water only center
			for index in range(len(moves)):
				field.action(move, moves[index])
				field.action(harvest)
				field.plant(plant_entity)
				field.action(use_item, Items.Fertilizer)
			for item in gain_and_cost_items:
				if not timer.checkpoint(item, 10):
					break # Skip checking the rest as we are under the threshold

	gain_and_cost_items = [Items.Weird_Substance, Items.Wood, Items.Fertilizer]
	for item in gain_and_cost_items:
		timer.start(item)
	plant_cross_pattern()
		
def main():
	change_hat(Hats.Straw_Hat)
	poison_pill = {}
	target_amount = 100000
	plant_grass_fertilize(target_amount, poison_pill)

if __name__ == "__main__":
	main()
	