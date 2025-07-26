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
			kill_signal = strategy.poison_pills[order_item]
			strategy.function[order_item](order_amount, kill_signal)
			if poison_pill.triggered(kill_signal):
				break
	
if __name__ == "__main__":
	main()
