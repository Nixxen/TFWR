import position
import static
import field
import poison_pill
import log
import algorithms

def amaze(target_items, poison_pills):
	log.info(["Hunting for gold until", target_items])
	
	def plant_maze():
		plant(Entities.Bush)
		n_substance = get_world_size() * num_unlocked(Unlocks.Mazes)
		use_item(Items.Weird_Substance, n_substance)
	
	# Blindly feel the walls, building a map of the maze
	def feel():
		pass

	plant_maze()
	next_treasure = None
	walls = algorithms.copy_dict(field.empty)
	while num_items(Items.Gold) < target_items:
		if poison_pill.triggered(poison_pills):
			break
		drone_pos = position.get_xy()
		entity_type = get_entity_type()
		while entity_type != Entities.Treasure:
			if not next_treasure:
				feel()
			else:
				next_move = moves.pop()
				moved = position.go_to_limited(next_move[0], next_move[1])
				if not moved:
					pathfinding.debug_moves(walls, moves, True)
					log.warn(["Failed to move. Aborting"])
					break
				pos = next_move
				if pos == next_treasure:
					next_treasure = get_next_treasure_pos()
				moves = pathfinding.pathfind(pos, next_treasure, position.distance, walls)
		# TODO: Rework snake logic to work for mazes
		
def main():
	change_hat(Hats.Straw_Hat)
	poison_pill = get_cost(Entities.Pumpkin)
	target_amount = 1000000
	plant_pumpkin(target_amount, poison_pill)

if __name__ == "__main__":
	main()
	