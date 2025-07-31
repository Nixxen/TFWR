
def ceil(num):
	return -(-num // 1)
	
def floor(num):
	return num // 1

def main():
	numbers = [1, 1.1, 2, 2.1, 2.9]
	for x in numbers:
		rounded_up_x = ceil(x)
		quick_print(x, "Up ->", rounded_up_x)
		rounded_down_x = floor(x)
		quick_print(x, "Down ->", rounded_down_x)
		
if __name__ == "__main__":
	main()