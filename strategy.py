import tree_logic
import snake
import cactus_logic
import pumpkin_logic
import sunflower_logic
import carrot_logic
import grass_logic
import kickstart
import log


low_limit = {
	Items.Power: 3000,
	Items.Cactus: 4000,
	Items.Pumpkin: 4000,
	Items.Carrot: 4000,
	Items.Hay: 4000,
	Items.Wood: 4000,
	Items.Bone: 4000,
	Hats.Straw_Hat: 0 # kickstart wildcard
}
entity_map = {
	Items.Power: Entities.Sunflower,
	Items.Cactus: Entities.Cactus,
	Items.Pumpkin: Entities.Pumpkin,
	Items.Carrot: Entities.Carrot,
	Items.Hay: Entities.Grass,
	Items.Wood: Entities.Tree,
	Items.Bone: Entities.Apple
}
function = {
	Items.Power: sunflower_logic.plant_sunflower,
	Items.Cactus: cactus_logic.plant_cactus,
	Items.Pumpkin: pumpkin_logic.plant_pumpkin,
	Items.Carrot: carrot_logic.plant_carrot,
	Items.Hay: grass_logic.plant_grass,
	Items.Wood: tree_logic.plant_tree,
	Items.Bone: snake.be_dinosaur,
	Hats.Straw_Hat: kickstart.execute_kickstart
}
poison_pills = {}
hysteresis = 3 # multiplier
item_target = {}
for item in low_limit:
	item_target[item] = low_limit[item] * hysteresis
	# For simplicity we assume a static yield per item instead of algorithmic bonuses
	# We are considering the worst case
	if item != Items.Power and item != Hats.Straw_Hat:
		poison_pills[item] = {}
		poison_pills[item][Items.Power] = low_limit[Items.Power] #base_poison_pill
	else:
		poison_pills[item] = {}
	if not item in entity_map:
		continue # Wildcard item
	entity_cost = get_cost(entity_map[item])
	for cost_item in entity_cost:
		poison_pills[item][cost_item] = low_limit[cost_item]
	

# Returns a plant order stack allowing the target (front) to be reached by growing the items after it first
def determine():
	def stack_item_order(item, amount):
		item_order = (item, amount) # NB! Target amount is the end target, including existing num_items
		plant_stack.append(item_order)
		if not item in entity_map:
			# Dealing with wildcard item, additional costs will be manually
			# dealt with in the wildcard items functions
			return
		cost_items = get_cost(entity_map[item])
		for cost_item in cost_items:
			prerequisite_amount = cost_items[cost_item] * (amount - num_items(cost_item) + low_limit[cost_item])
			poison_pill_cost = poison_pills[item][cost_item]
			if num_items(cost_item) < prerequisite_amount:
				stack_item_order(cost_item, prerequisite_amount)
			elif num_items(cost_item) < poison_pill_cost:
				stack_item_order(cost_item, poison_pill_cost)
				# TODO: Need to account for used items as well as poison pill limit
	
	# Avoid death spiral due to too few power and lacking carrots
	def require_kickstart(kickstart_amount):
		if num_items(Items.Power) < kickstart_amount:
			required_carrots = get_cost(Entities.Sunflower)[Items.Carrot] * kickstart_amount
			if num_items(Items.Carrot) < required_carrots:
				return True
		return False
	
	
	plant_stack = [] # Item orders (Item, quantity)
	for item in low_limit:
		if not low_limit[item] or num_items(item) > low_limit[item]:
			continue
		kickstart_amount = low_limit[Items.Power] * 2
		if require_kickstart(kickstart_amount):
			stack_item_order(Hats.Straw_Hat, kickstart_amount)
			break
		stack_item_order(item, item_target[item])
		break # Stack one item at a time to not cause infinite loops
	if not plant_stack:
		log.info(["We won the game I quess. Make some cacti for now"])
		stack_item_order(Items.Cactus, num_items(Items.Cactus) * hysteresis)
	return plant_stack
	

def main():
	pass

if __name__ == "__main__":
	main()	
