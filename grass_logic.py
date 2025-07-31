import position
import static
import field
import poison_pill
import log
import timer

def plant_grass(target_items, poison_pills):
	log.info(["Planting grass until", target_items])
	
	# Reaches ~9200 items per min
	# Uses field actions, but we do not need it for this algo.
	# Sub-optimal to built_ins
	def field_usage():
		field.plant_field(Entities.Grass, Grounds.Soil, False, True)
	
	# Reaches ~22000 items per min
	def built_ins_main_loop():
		field.plant_harvest_quick(Entities.Grass)
	
	item = Items.Hay
	timer.start(item)
	field.pre_plant_built_ins(Entities.Grass)
	while num_items(Items.Hay) < target_items:
		if poison_pill.triggered(poison_pills):
			break
		#field_usage()
		built_ins_main_loop() # No need to water
		timer.checkpoint(item)
		
def main():
	change_hat(Hats.Straw_Hat)
	poison_pill = get_cost(Entities.Grass)
	target_amount = num_items(Items.Hay) * 1.25
	plant_grass(target_amount, poison_pill)

if __name__ == "__main__":
	main()	