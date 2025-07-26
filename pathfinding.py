import static
import position
import min_heap
import algorithms
import field
import log

# Pathfind from pos to target avoiding any blocking_position using A*
# Returns the full path of moves required to reach target without
# hitting any blocking areas.
# heur is the cost function. E.g., position.distance.
# blocking_position is a dictionary of positions with blocking values.
#  any truthy value will be blocking.
# If `moving_block` is true, each move will make the block
# follow the drone (e.g., for Snake)
# If `moving_block` is false, the blocks are considered
# static (e.g., for mazes)
def pathfind(start, target, heur, blocked_positions, moving_block = False):
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

def main():
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
	
	moves = pathfind(start, target, position.distance, blocking, False)
	log.info(["Path:", moves])
	debug_moves(blocking, moves, True)
	
if __name__ == '__main__':
	main()
