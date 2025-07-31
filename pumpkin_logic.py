import position
import static
import field
import poison_pill
import log
import timer

# Reaches ~25800 items per min at a ~4:1 harvest:cost convergence
def plant_pumpkin(target_items, poison_pills):
	log.info(["Planting pumpkin until", target_items])

	def replant_field():
		failed_locations = set()
		start_pos = position.get_xy()
		for x in range(static.world_size):
			for y in range(static.world_size):
				wrap_x = (x + start_pos[0]) % static.world_size
				wrap_y = (y + start_pos[1]) % static.world_size
				pos = (wrap_x, wrap_y)
				field.water(pos)
				current_entity=get_entity_type()
				if not current_entity:
					plant(Entities.Pumpkin)
					failed_locations.add(pos)
				field.action(move,North)
			field.action(move,East)
		return failed_locations
			
	def set_full_failed():
		failed_locations = set()
		for x in range(static.world_size):
			for y in range(static.world_size):
				failed_locations.add((x, y))
		return failed_locations
			
	def revisit_failed_crop_locations(drone_pos, locations):
		revisited = set() # TODO: Traverse based on shortest path
		for pos in locations:
			position.go_to(pos[0], pos[1])
			current_entity=get_entity_type()
			if not current_entity:
				plant(Entities.Pumpkin)
				revisited.add(pos) # TODO: Force grow using fertilizer
			elif not can_harvest():
				revisited.add(pos)
		return revisited	
	
	gain_and_cost_items = [Items.Pumpkin, Items.Carrot]
	for item in gain_and_cost_items:
		timer.start(item)
	field.plant_field(Entities.Pumpkin, Grounds.Soil)
	# TODO: Figure Out what the measure does for pumpkins
	# Assume all planting failed on first run
	failed = set_full_failed() 
	while num_items(Items.Pumpkin) < target_items:
		if poison_pill.triggered(poison_pills):
			break
		drone_pos = position.get_xy()
		while failed:
			failed = revisit_failed_crop_locations(drone_pos, failed)
			# TODO: Fix weird revisit pattern
		harvest()
		failed = replant_field()
		for item in gain_and_cost_items:
			timer.checkpoint(item)
		
def main():
	change_hat(Hats.Straw_Hat)
	poison_pill = get_cost(Entities.Pumpkin)
	target_amount = num_items(Items.Pumpkin) * 2
	plant_pumpkin(target_amount, poison_pill)

if __name__ == "__main__":
	main()
	