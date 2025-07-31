import position
import static
import field
import algorithms
import poison_pill
import log
import timer

# Old algo reaches ~73000 items per min
# Trimmed algo reaches ~111000 items per min
def plant_tree(target_items, poison_pills):
	log.info(["Planting tree until", target_items])

	def is_tree_plot(pos):
		return (pos[0] + pos[1]) % 2 == 0
		
	def pre_plant_trees():
		plant_entity = Entities.Tree
		auxillary_entity = Entities.Bush
		position.go_to(0, 0)
		for x in range(static.world_size):
			for y in range(static.world_size):
				pos = (x, y)
				if not field.tilled[pos]:
					if get_ground_type() != Grounds.Soil:
						field.till()
					field.tilled[pos] = True
				harvested = False
				field.water(pos)
				current_entity = get_entity_type()
				if current_entity and (
						(is_tree_plot(pos) and current_entity != plant_entity)
						or (not is_tree_plot(pos) and current_entity != auxillary_entity)
					):
					harvested = harvest() # Remove invalid entity without waiting for growth
				if harvested or not current_entity:
					if is_tree_plot(pos):
						plant(plant_entity)
					else:
						plant(auxillary_entity)
				move(North)
			move(East)
		
	def plant_harvest_quick_trees(do_water = False):
		plant_entity = Entities.Tree
		auxillary_entity = Entities.Bush
		position.go_to(0, 0)
		for x in range(static.world_size):
			for y in range(static.world_size):
				pos = (x, y)
				harvested = False
				if do_water:
					field.water(pos)
				if can_harvest():
					harvested = harvest()
				if harvested:
					if is_tree_plot(pos):
						plant(plant_entity)
					else:
						plant(auxillary_entity)
				move(North)
			move(East)
	
	item = Items.Wood
	timer.start(item)
	pre_plant_trees()
	counter = 0
	while num_items(Items.Wood) < target_items:
		if poison_pill.triggered(poison_pills):
			break
		counter += 1
		for _ in range(19): # Water < 0.55
			plant_harvest_quick_trees()
		plant_harvest_quick_trees(True)
		timer.checkpoint(item)

def main():
	change_hat(Hats.Straw_Hat)
	poison_pill = get_cost(Entities.Tree)
	target_amount = num_items(Items.Wood) * 1.25
	plant_tree(target_amount, poison_pill)

if __name__ == "__main__":
	main()
