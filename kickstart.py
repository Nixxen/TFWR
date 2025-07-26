import grass_logic
import tree_logic
import carrot_logic
import sunflower_logic
import log

def execute_kickstart(target_amount, kill_switch):
	log.info(["Kickstarting the farm to get enough power to not death spiral"])
	required_power = target_amount
	required_carrots = get_cost(Entities.Sunflower)[Items.Carrot] * required_power
	carrot_costs = get_cost(Entities.Carrot)
	required_wood = carrot_costs[Items.Wood] * required_carrots
	required_hay = carrot_costs[Items.Hay] * required_carrots
	empty_poison_pill = {}
	if required_hay > num_items(Items.Hay):
		log.info(["Producing hay"])
		grass_logic.plant_grass(required_hay, empty_poison_pill)
	if required_wood > num_items(Items.Wood):
		log.info(["Producing wood"])
		tree_logic.plant_tree(required_wood, empty_poison_pill)
	if required_carrots > num_items(Items.Carrot):
		log.info(["Producing carrot"])
		carrot_logic.plant_carrot(required_carrots, empty_poison_pill)
	if required_power > num_items(Items.Power):
		log.info(["Producing power"])
		sunflower_logic.plant_sunflower(required_power, empty_poison_pill)
		
def main():
	change_hat(Hats.Straw_Hat)
	target_amount = 3000
	execute_kickstart(target_amount, {})

if __name__ == "__main__":
	main()	
	
	
