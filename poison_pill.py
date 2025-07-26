import log

# Returns true if any of the items in the poison pills dictionary are bellow the threshold
def triggered(poison_pills):
	for item in poison_pills:
		if num_items(item) < poison_pills[item]:
			log.info(["Poison pill triggered for ", item, ":",num_items(item), "<", poison_pills[item]])
			return True
	return False
	