import position
import static
import field
import poison_pill
import log

def plant_grass(target_items, poison_pills):
	log.info(["Planting grass until", target_items])
	while num_items(Items.Hay) < target_items:
		if poison_pill.triggered(poison_pills):
			break
		field.plant_field(Entities.Grass, Grounds.Soil, False, True)
		
		
def main():
	change_hat(Hats.Straw_Hat)
	poison_pill = get_cost(Entities.Grass)
	target_amount = 100000
	plant_grass(target_amount, poison_pill)

if __name__ == "__main__":
	main()	