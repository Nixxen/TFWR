import static
import position
import min_heap
import algorithms
import field
import log
import debug

# Pathfind from pos to target avoiding any blocking_position using A*
# Returns the full path of moves required to reach target without
# hitting any blocking areas.
# heur is the cost function. E.g., position.distance.
# blocking_position is a dictionary of positions with blocking values.
#  any truthy value will be blocking.
# If `moving_block` is true, each move will make the block
# follow the drone (e.g., for Snake)
# If `moving_block` is false, the blocks are considered static (e.g., for mazes)
def astar(start, target, heur, blocked_positions, moving_block = False):
	# Returns a stack for the path
	def reconstruct_path(moves, current):
		path = [current]
		while current in moves:
			current = moves[current]
			path.append(current)
		return path
	
	def update_moving_block(new_position, old_block):
		new_block = {}
		highest_block = 0
		for pos in old_block:
			if not old_block[pos]:
				new_block[pos] = old_block[pos]
				continue
			if not highest_block or highest_block < old_block[pos]:
				highest_block = old_block[pos]
			new_block[pos] = old_block[pos] - 1
		new_block[new_position] = highest_block
		return new_block
	
	# Returns a grid dict initialized with arbitrarily high values
	def cost_dict():
		cost = {}
		for x in range(static.world_size):
			for y in range(static.world_size):
				pos = (x, y)
				cost[pos] = 99999 # Essentially "infinite"
		return cost
				
	def get_neighbors(pos, blocked):
		x, y = pos
		max_size = static.world_size - 1
		north = None
		east = None
		south = None
		west = None
		north = position.update(pos, North, False)
		south = position.update(pos, South, False)
		west = position.update(pos, West, False)
		east = position.update(pos, East, False)
		neighbors = []
		for neighbor in [north, east, south, west]:
			if not neighbor or blocked[neighbor]:
				continue
			neighbors.append(neighbor)
		return neighbors
	
	open_heap = [(0, start)] 
	moves = {}
	known_cost = cost_dict()
	known_cost[start] = 0
	estimated_cost = cost_dict()
	estimated_cost[start] = heur(start, target)
	if moving_block:
		block_map = {}
		block_map[start] = blocked_positions
	
	while open_heap:
		closest = open_heap[0]
		current = closest[1]
		if current == target:
			return reconstruct_path(moves, current)
		
		min_heap.delete(open_heap, closest)
		if moving_block:
			neighbors = get_neighbors(current, block_map[current])
		else:
			neighbors = get_neighbors(current, blocked_positions)
		for neighbor in neighbors:
			tentative_cost = known_cost[current] + 1
			if neighbor not in known_cost or tentative_cost < known_cost[neighbor]:
				moves[neighbor] = current
				known_cost[neighbor] = tentative_cost
				estimated_cost[neighbor] = tentative_cost + heur(neighbor, target)
				if moving_block:
					block_map[neighbor] = update_moving_block(neighbor, block_map[current])
				if neighbor not in open_heap:
					min_heap.insert(open_heap, (estimated_cost[neighbor], neighbor))
	return []

# Pathfind from pos through all targets assuming no blocks
# Returns the full path-stack of moves required to traverse all targets
# in a greedy-effort shortet path. A radius is used to further
# "greed up" the search. If no points are detected within the radius,
# the full grid is searched.
# Targets are a list of entities following the (value, (x, y)) format.
# Uses position.distance with wrapping as a cost function.
# max_radius is the initial search radius limiting factor.
def greedy_wrapped_traversal(start, targets, max_radius = 5):
	visited = set()
	path = []
	current = start
	size = static.world_size - 1
	
	def is_within_radius(pos_a, pos_b):
		dx = abs(pos_a[0] - pos_b[0])
		if dx > max_radius and (size - dx) > max_radius:
			return False
		dy = abs(pos_a[1] - pos_b[1])
		if dy > max_radius and (size - dy) > max_radius:
			return False
		return True
		
	def find_best_target(current, targets, visited, use_radius_filter):
		best_pos = None
		best_distance = 9999999 # Arbitrarily high number
		for i in range(len(targets)):
			pos = targets[i][1]
			if pos in visited:
				continue
			if use_radius_filter and not is_within_radius(current, pos):
				continue
			distance = position.distance(current, pos, True)
			if distance < best_distance:
				best_pos = pos
				best_distance = distance
		return best_pos
				
	for _ in targets:
		# First pass: radius-filtered scan
		best_pos = find_best_target(current, targets, visited, True)
		# Fallback: full scan if no close point found
		if best_pos == None:
			best_pos = find_best_target(current, targets, visited, False)
		visited.add(best_pos)
		path.append(best_pos)
		current = best_pos
	
	# Reverse to stack
	algorithms.reverse_list_in_place(path)
	return path

def debug_moves(grid, moves, override = False):
	log.debug(["Moves debug:", override])
	y = static.world_size - 1
	while y >= 0:
		line = ""
		for x in range(static.world_size):
			pos = (x, y)
			if pos in moves:
				if pos == moves[0]:
					line += " E"
				elif pos == moves[len(moves)-1]:
					line += " S"
				else:
					line += " X"
			else:
				val = grid[pos]
				if not val:
					line += " ."
				else:
					if len(str(val)) == 2:
						line += str(val)
					else:
						line += " " + str(val)
		log.debug([line], override)
		y -= 1

def main_astar():
	def heur_test(start, end):
		x1, y1 = start
		x2, y2 = end
		return abs(x1 - x2) + abs(y1 - y2)
	
	start = (0,0)
	target = (0,3)
	blocking = algorithms.copy_dict(field.empty)
	blocking[(0,1)] = 3
	blocking[(0,2)] = 2
	blocking[(1,2)] = 1
	
	moves = astar(start, target, position.distance, blocking, False)
	log.info(["Path:", moves])
	debug_moves(blocking, moves, True)
	
def main_greedy():
	start = (0,0)
	targets = [
		(1, (0,3)),
		(1, (0,5)),
		(1, (1,3)),
		(1, (4,4)),
		(1, (1,1)),
		(1, (8,8))
	]
	
	moves = greedy_wrapped_traversal(start, targets)
	log.info(["Path:", moves])
	order = algorithms.copy_dict(field.empty)
	visit_number = 1
	for index in range(len(targets) -1, -1, -1):
		pos = moves[index]
		order[pos] = visit_number
		visit_number += 1
	debug.dict(order, "Greedy path debug:", True)
	
if __name__ == '__main__':
	#main_astar()
	main_greedy()
