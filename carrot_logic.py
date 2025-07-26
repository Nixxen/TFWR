import position
import static
import field
import poison_pill
import log

def plant_carrot(target_items, poison_pills):
	log.info(["Planting carrot until", target_items])
	while num_items(Items.Carrot) < target_items:
		if poison_pill.triggered(poison_pills):
			break
		field.plant_field(Entities.Carrot, Grounds.Soil, False, True)
		

def main():
	change_hat(Hats.Straw_Hat)
	poison_pill = get_cost(Entities.Carrot)
	target_amount = 100000
	plant_carrot(target_amount, poison_pill)

if __name__ == "__main__":
	main()
