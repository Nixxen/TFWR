import field
import static

def get_xy():
	return (get_pos_x(),get_pos_y())

# Returns the action cost of getting from A to B
def distance(pos_a, pos_b, allow_wrap = False):
	x1, y1 = pos_a
	x2, y2 = pos_b
	size = static.world_size
	if not allow_wrap:
		return abs(x1 - x2) + abs(y1 - y2)
	# Wrap-aware Manhattan distance
	delta_x = min(abs(x1 - x2), size - abs(x1 - x2))
	delta_y = min(abs(y1 - y2), size - abs(y1 - y2))
	return delta_x + delta_y

# Returns a pos coordinate incremented in the cardinal direction
# If the direction is invalid, return None
# If wrap_around is false and the move exits the grid, return None 
def update(pos, direction, wrap_around = True):
	if direction not in [North, East, South, West]:
		return None # Invalid direction
	if wrap_around:
		if direction == North:
			return (pos[0], (pos[1] + 1) % static.world_size)
		elif direction == South:
			return (pos[0], (pos[1] - 1 + static.world_size) % static.world_size)
		elif direction == East:
			return ((pos[0] + 1) % static.world_size, pos[1])
		elif direction == West:
			return ((pos[0] - 1 + static.world_size) % static.world_size, pos[1])
	else:
		if direction == North:
			if pos[1] == static.world_size - 1:
				return None
			return (pos[0], pos[1] + 1)
		elif direction == South:
			if pos[1] == 0:
				return None
			return (pos[0], pos[1] - 1)
		elif direction == East:
			if pos[0] == static.world_size - 1:
				return None
			return (pos[0] + 1, pos[1])
		elif direction == West:
			if pos[0] == 0:
				return None
			return (pos[0] - 1, pos[1])

# Returns the cardinal direction from source to target
# If the coordinates are not adjacent, return None
def get_direction(source, target):
	if distance(source, target) > 1:
		return None
	if source[0] != target[0]:
		if source[0] < target[0]:
			return East
		else:
			return West
	if source[1] < target[0]:
		return North
	return South

# Go to target coordinates using world wrap
# Assumes a clear path
def go_to(x_target, y_target):
	pos = get_xy()
	while pos != (x_target, y_target):
		if pos[0] != x_target:
			delta_x = (x_target - pos[0]) % static.world_size
			if delta_x <= static.world_size // 2:
				field.action(move,East)
				pos = ((pos[0] + 1) % static.world_size, pos[1])
			else:
				field.action(move,West)
				pos = ((pos[0] - 1 + static.world_size) % static.world_size, pos[1])
		if pos[1] != y_target:
			delta_y = (y_target - pos[1]) % static.world_size
			if delta_y <= static.world_size // 2:
				field.action(move,North)
				pos = (pos[0], pos[1] + 1 % static.world_size)
			else:
				field.action(move,South)
				pos = (pos[0], (pos[1] - 1 + static.world_size) % static.world_size)
				
# Go to target coordinates without world wrap
# Assumes path can be bloced
def go_to_limited(x_target, y_target):
	pos = get_xy()
	while pos != (x_target, y_target):
		moved = True
		if pos[0] != x_target:
			if pos[0] < x_target:
				moved = field.action(move,East)
				if moved:
					pos = (pos[0] + 1, pos[1])
			else:
				moved = field.action(move,West)
				if moved:
					pos = (pos[0] - 1, pos[1])
		if pos[1] != y_target:
			if pos[1] < y_target:
				moved = field.action(move,North)
				if moved:
					pos = (pos[0], pos[1] + 1)
			else:
				moved = field.action(move,South)
				if moved:
					pos = (pos[0], pos[1] - 1)
		if not moved:
			return False
	return True