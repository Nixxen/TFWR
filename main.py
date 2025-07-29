import strategy
import static
import poison_pill
import log

if not log.enabled_debug:
	clear()

def main():
	while True:
		plant_stack = strategy.determine()
		log.info(["Plant stack: ", plant_stack])
		while plant_stack: 
			order_item, order_amount = plant_stack.pop()
			kill_signal = strategy.get_poison_pill(order_item)
			strategy.function[order_item](order_amount, kill_signal)
			if poison_pill.triggered(kill_signal):
				break
		prev_unlock = strategy.get_previous_unlock()
		if prev_unlock:
			unlock(prev_unlock)
			log.info(["Completed gathering resources for", prev_unlock, " - Unlocked"])
			# TODO: Check if we can afford it
	
if __name__ == "__main__":
	main()
