import position
import static
import field
import poison_pill
import log

def plant_sunflower(target_items, poison_pills):
	log.info(["Planting sunflower until", target_items])

	average_sunflower_grow_time = ((8.4 - 5.6) / 2 + 5.6)
	field.plant_field(Entities.Sunflower, Grounds.Soil, True)
	
	while num_items(Items.Power) < target_items:
		if poison_pill.triggered(poison_pills):
			break
		drone_pos = position.get_xy()
		value, pos = field.get_closest_highest_value_pos(drone_pos)
		if not pos:
			log.warn("Value error, invalid position. Unable to get closest high position")
			break
		position.go_to(pos[0], pos[1])
		growth_multiplier = field.water(pos)
		harvested = False
		moved = False
		while(not can_harvest()):
			# Move somewhere else until we can harvest, not wasting time
			pos = position.get_xy()
			dice_x = (pos[0] + random() * static.world_size/2 // 1) % static.world_size
			dice_y = (pos[1] + random() * static.world_size/2 // 1) % static.world_size
			position.go_to(dice_x, dice_y)
			moved = True
		max_value = field.get_highest_value()
		pre_harvest = num_items(Items.Power)
		harvested = harvest()
		post_harvest = num_items(Items.Power)
		if not moved:
			log.debug(["Harvested most valuable sunflower with value", value, "/", max_value, ", gained", post_harvest-pre_harvest])
		else:
			log.debug(["Harvested random different sunflower with value", field.value[pos], "/", max_value, ", gained", post_harvest-pre_harvest])
		if harvested:
			pos = position.get_xy()
			plant(Entities.Sunflower)
			field.growing[pos] = average_sunflower_grow_time / field.multiplier[pos]
			field.value[pos] = measure()
		
def main():
	change_hat(Hats.Straw_Hat)
	poison_pill = get_cost(Entities.Sunflower)
	target_amount = 100000
	plant_sunflower(target_amount, poison_pill)

if __name__ == "__main__":
	main()
