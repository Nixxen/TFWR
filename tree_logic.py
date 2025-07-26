import position
import static
import field
import algorithms
import poison_pill
import log

def plant_tree(target_items, poison_pills):
	log.info(["Planting tree until", target_items])
	def is_tree_plot(pos):
		return (pos[0]+pos[1])%2 == 0

	def get_auxillary_entity():
		return Entities.Bush 
		# Override cozy auxillary function in an attempt to maximize wood and force other planters to run more often
		# TODO: Remove override or integrate it into the system in a better way
		if num_items(Items.hay)<num_items(Items.Carrot):
			return Entities.Grass
		return Entities.Carrot
	
	position.go_to(0, 0)
	while num_items(Items.Wood) < target_items:
		if poison_pill.triggered(poison_pills):
			break
		auxillary_entity = get_auxillary_entity()
		for column in range(static.world_size):
			for row in range(static.world_size):
				pos = (row, column)
				if not field.tilled[pos]:
					if get_ground_type() == Grounds.Grassland:
						till()
					field.tilled[pos] = True
				harvested = False
				growth_multiplier = field.water(pos)
				current_entity=get_entity_type()
				if current_entity and (
						(is_tree_plot(pos) and current_entity != Entities.Tree)
						or (not is_tree_plot(pos) and current_entity != auxillary_entity)
					):
					harvested = harvest() # Remove invalid entity without waiting for growth
				if not harvested and can_harvest():
					harvested = harvest()
				if harvested or not current_entity:
					if is_tree_plot(pos):
						plant(Entities.Tree)
					else:
						plant(auxillary_entity)
				field.action(move, North)
			field.action(move, East)


def main():
	change_hat(Hats.Straw_Hat)
	poison_pill = get_cost(Entities.Tree)
	target_amount = 100000
	plant_tree(target_amount, poison_pill)

if __name__ == "__main__":
	main()
