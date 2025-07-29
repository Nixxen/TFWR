import log

start_time = {}
last_update = {}
start_items = {}

# Initialize and start a timer for the given item
def start(item):
	global start_time
	global last_update
	global start_items
	start_time[item] = get_time()
	last_update[item] = start_time[item]
	start_items[item] = num_items(item)

# Reports on the item gain for the given item as long as there have been at least
# override_time amount of seconds since the last report. 
def checkpoint(item, override_time = 60):
	global last_update
	if item not in start_time or item not in last_update or item not in start_items:
		log.error(["Can not checkpoint a timer before starting it. Timer for", item])
		return False
	time = get_time()
	if time - last_update[item] < override_time:
		return False
	last_update[item] = time
	now_items = num_items(item)
	items_per_minute = (now_items - start_items[item]) / (time - start_time[item]) * 60
	log.info([item, "per min:", items_per_minute])
	return True
		