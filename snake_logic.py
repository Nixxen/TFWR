import static
import poison_pill
import field
import position
import pathfinding
import algorithms
import log

def be_dinosaur(target_items, poison_pills):
	log.info(["Gathering dinosaur bones until", target_items])
	
	def get_next_apple_pos():
		next = None
		if get_entity_type() == Entities.Apple:
			next = measure()
		return next
	
	def can_move(pos, blocked):
		north = position.update(pos, North, False)
		south = position.update(pos, South, False)
		west = position.update(pos, West, False)
		east = position.update(pos, East, False)
		moves = []
		for move in [north, east, south, west]:
			if not move or move in blocked:
				continue
			moves.append(move)
		return moves != []
	
	def build_tail_grid(tail):
		grid = algorithms.copy_dict(field.empty)
		for index in range(len(tail)):
			grid[tail[index]] = index + 1
		return grid
		
	def update_tail():
		tail.append(pos)
		if len(tail) != tail_length:
			tail.pop(0)
	
	while num_items(Items.Bone) < target_items:
		if poison_pill.triggered(poison_pills):
			break
		current_entity = get_entity_type()
		if current_entity != Entities.Grass and current_entity != None:
			field.clear_field()
		next_apple_pos = get_next_apple_pos()
		while not next_apple_pos: # Fix bad start location
			field.action(change_hat, Hats.Straw_Hat)
			field.action(change_hat, Hats.Dinosaur_Hat)
			next_apple_pos = get_next_apple_pos()
		pos = position.get_xy()
		tail_length = 1 # Including head
		tail = [pos]
		move_cost_reduction = 0.03 * tail_length
		tail_grid = build_tail_grid(tail)
		moves = pathfinding.astar_snake(pos, next_apple_pos, position.distance, tail_grid)
		while can_move(pos, tail):
			next_move = moves.pop()
			moved = position.go_to_limited(next_move[0], next_move[1])
			if not moved:
				pathfinding.debug_moves(build_tail_grid(tail), moves, True)
				log.warn(["Failed to move. Aborting"])
				break
			pos = next_move
			if pos == next_apple_pos:
				next_apple_pos = get_next_apple_pos()
				if not next_apple_pos:
					log.warn(["Unexpected lack of apples. Aborting"])
					break
				tail_length += 1
				tail_grid = build_tail_grid(tail)
				moves = pathfinding.astar_snake(pos, next_apple_pos, position.distance, tail_grid)
				if not moves:
					log.debug(["Pathfinding failed. Aborting"])
					break
				# TODO: implement flood fill avoidance and recovery path
				# simulate moves, updating blocked
				# if no space to move + 1 tail piece, do not path that way
				# select a "holding pattern fallback", and repeat until safe
				# If no holding pattern available, break
			else:
				update_tail()
		before = num_items(Items.Bone)
		field.action(change_hat, Hats.Straw_Hat)
		after = num_items(Items.Bone)
		log.info(["Dinosaured for a while. Gained", after-before])
	# Reset to straw hat if somehow we are still wearing a dinosaur hat
	field.action(change_hat, Hats.Straw_Hat)
		
		
def main():
	current_entity = get_entity_type()
	if current_entity != None:
		harvest()
	poison_pill = {}
	target_amount = 123123123
	be_dinosaur(target_amount, poison_pill)

if __name__ == "__main__":
	main()	
		