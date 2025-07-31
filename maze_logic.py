import position
import static
import field
import poison_pill
import log
import pathfinding
import debug
import algorithms

def amaze(target_items, poison_pills):
	log.info(["Hunting for gold until", target_items])
	
	def plant_maze(n_substance):
		current_entity = get_entity_type()
		if current_entity != None:
			harvest()
		plant(Entities.Bush)
		use_item(Items.Weird_Substance, n_substance)

	# Blindly feel the walls, building a partial map of the maze, using DFS-like method to avoid repeating paths
	def feel_for_first_treasure(pos):
		def is_treasure():
			return get_entity_type() == Entities.Treasure
		return pathfinding.dfs(pos, is_treasure)
		
	def get_walls(pos):
		pos_walls = []
		for direction in [North, East, South, West]:
			if (pos, direction) in walls:
				pos_walls.append(direction)
		return pos_walls
		
	def make_moves(pos):
		next_move = moves.pop()
		previous = pos
		if pos == next_move:
			log.error(["We are pathing into the same location. Debug this pos", pos])
		if not optimal_path_found: # Scan existing walls for removal
			next_move_walls = get_walls(pos)
			if next_move_walls:
				found_shortcut = False
				for probe_dir in next_move_walls:
					probe_move = position.update(pos, probe_dir, False)
					if probe_move == None:
						continue
					probe_moved = position.go_to_limited(probe_move[0], probe_move[1])
					if not probe_moved:
						continue
					algorithms.del_bidirection(walls, pos, probe_dir)
					if probe_move in moves:
						found_shortcut = True
						while moves.pop() != probe_move:
							continue
						moves.append(probe_move)
						break
				if found_shortcut:
					return True, pos # Skip intended move and apply shortcut
				probe_pos = position.get_xy()
				if probe_pos != pos:
					pos = probe_pos # Recalculate path from new position
					return False, pos
		moved = position.go_to_limited(next_move[0], next_move[1])
		if not moved:
			# Ran into a wall, update walls and start over
			direction = position.get_direction(pos, next_move)
			algorithms.set_bidirection(walls, pos, direction)
			neighbor_dirs = pathfinding.get_neighbors_directions_maze(pos, walls)
			for direction in neighbor_dirs:
				neighbor = position.update(pos, direction, False)
				if neighbor == previous:
					continue
				moved = position.go_to_limited(neighbor[0], neighbor[1])
				if moved:
					break # We are only probing for extra walls after hitting another wall, but actually moved. Restart pathfinding
				if not moved:
					algorithms.set_bidirection(walls, pos, direction)
			log.debug(["Failed to move from pos", pos, "to", next_move, ". Walls updated. Restarting pathfinding"])
			return False, pos
		pos = next_move
		return True, pos
	
	size = get_world_size()
	n_substance = size * num_unlocked(Unlocks.Mazes)
	gold_per_solve = (size**2) * num_unlocked(Unlocks.Mazes)
	solves_to_target = (target_items - num_items(Items.Gold))/gold_per_solve
	
	while num_items(Items.Gold) < target_items:
		if poison_pill.triggered(poison_pills):
			break
		plant_maze(n_substance)
		next_treasure = None
		walls = None
		solves = 0
		max_solves = min(299, solves_to_target)
		while solves <= max_solves:
			final_solve = solves + 1 > max_solves
			pos = position.get_xy()
			if not next_treasure:
				success, walls = feel_for_first_treasure(pos)
				pathfinding.debug_walls(walls, True)
				if success:# Found first treasure
					next_treasure = measure()
					if not final_solve:
						use_item(Items.Weird_Substance, n_substance)
					solves += 1 
				else:
					log.error(["DFS failed to find treasure, debug this"])
					continue
			else:
				# Pathfind towards next treasure.
				# Checking each step for possible moves through walls to update the blocking areas.
				# Skip checking walls if the previous update was within some threshold of the manhattan distance.
				# Repeat at max 500 times.
				if walls == None:
					log.warn(["Walls should be populated. Something has gone wrong. Debug this."])
					break
				moves = pathfinding.astar_maze(pos, next_treasure, position.distance, walls)
				optimal_path_found = False
				if moves:
					pos = moves.pop()
					optimal_path_found = position.distance(pos, moves[0]) == len(moves)
					#pathfinding.debug_walls(walls, (pos, moves[0]), True)
				while moves:
					success, pos = make_moves(pos)
					if not success:
						break # Abort and restart pathfinding
				if pos == next_treasure:
					next_treasure = measure()
					if not final_solve:
						use_item(Items.Weird_Substance, n_substance)
					solves += 1 
		before_harvest = num_items(Items.Gold)
		harvest()
		after_harvest = num_items(Items.Gold)
		log.info(["Harvested maze and gained", after_harvest - before_harvest, Items.Gold])
		solves_to_target = (target_items - num_items(Items.Gold))/gold_per_solve
		
def main():
	change_hat(Hats.Straw_Hat)
	poison_pill = {}
	target_amount = 10000
	amaze(target_amount, poison_pill)

if __name__ == "__main__":
	main()
	