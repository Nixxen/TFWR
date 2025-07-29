# Debug handlers for build in structures
import log
import static

# Debug wrapper for executing a function.
# Can save some ticks if call is only used for fetching debug data
def execute(function, parameter = None, override = False):
	if not log.enabled_debug and not override:
		return
	if parameter == None:
		return function()
	return function(parameter)
	

# Debug print each item of a list
def list(moves, header = "", override = False):
	if not log.enabled_debug and not override:
		return
	if header != "":
		log.debug([header], override)
	else:
		log.debug(["List debug:"], override)
	for move in moves:
		log.debug([move], override)
		
# Debug print a dict represented as a grid of the field
# Text_width is the expected max width of the value.
# Paddind will be auto adjusted up to that point
def dict(grid, header = "", override = False, text_width = 1):
	def pad_left(times):
		pad = ""
		for _ in range(times):
			pad += " "
		return pad
		
	grid_width = text_width + 1
	if not log.enabled_debug and not override:
		return
	if header == "":
		log.debug(["Dict debug:"], override)
	else:
		log.debug([header], override)
	y = static.world_size - 1
	while y >= 0:
		line = ""
		for x in range(static.world_size):
			pos = (x, y)
			val = grid[pos]
			if val == None:
				pad = pad_left(text_width)
				line += pad + "."
			else:
				pad = pad_left(grid_width - len(str(val)))
				line += pad + str(val)
		log.debug([line], override)
		y -= 1

# Debug print a set of positions, represented as a grid of the field
def set(input_set, header = "", override = False):
	if not log.enabled_debug and not override:
		return
	if header == "":
		log.debug(["Set debug:"], override)
	else:
		log.debug([header], override)
	y = static.world_size - 1
	while y >= 0:
		line = ""
		for x in range(static.world_size):
			pos = (x, y)
			if not pos in input_set:
				line += " ."
			else:
				line += " x"
		log.debug([line], override)
		y -= 1