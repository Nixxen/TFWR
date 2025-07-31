import position
import static
import field
import poison_pill
import log
import timer

def plant_carrot(target_items, poison_pills):
	log.info(["Planting carrot until", target_items])

	# Reaches ~7850 items per min at a ~1:1 harvest:cost convergence
	# Uses field actions, but we do not need it for this algo.
	# Sub-optimal to built_ins
	def field_usage():
		field.plant_field(Entities.Carrot, Grounds.Soil, False, True)
	
	# Reaches ~18700 items per min at a ~1:1 harvest:cost convergence
	def built_ins_main_loop(do_water = False):
		field.plant_harvest_quick(Entities.Carrot, do_water)

	gain_and_cost_items = [Items.Carrot, Items.Wood, Items.Hay]
	for item in gain_and_cost_items:
		timer.start(item)
	field.pre_plant_built_ins(Entities.Carrot)
	while num_items(Items.Carrot) < target_items:
		if poison_pill.triggered(poison_pills):
			break
		#field_usage()
		for _ in range(34): # Water < 0.35
			built_ins_main_loop()
		built_ins_main_loop(True)
		for item in gain_and_cost_items:
			timer.checkpoint(item)
		

def main():
	change_hat(Hats.Straw_Hat)
	poison_pill = get_cost(Entities.Carrot)
	target_amount = num_items(Items.Carrot) * 1.25
	plant_carrot(target_amount, poison_pill)

if __name__ == "__main__":
	main()
