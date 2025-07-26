import static
import loglevel

enabled_debug = loglevel.debug <= static.loglevel
enabled_info = loglevel.information <= static.loglevel
enabled_warning = loglevel.warning <= static.loglevel
enabled_error = loglevel.error <= static.loglevel


def error(args, override = False):
	if not enabled_error and not override:
		return
	prefix = "[Err]:"
	message = ""
	for arg in args:
		if message != "":
			message = message + " "
		message = message + str(arg)
	quick_print(prefix, message)

def warn(args, override = False):
	if not enabled_warning and not override:
		return
	prefix = "[Wrn]:"
	message = ""
	for arg in args:
		if message != "":
			message = message + " "
		message = message + str(arg)
	quick_print(prefix, message)

def info(args, override = False):
	if not enabled_info and not override:
		return
	prefix = "[Inf]:"
	message = ""
	for arg in args:
		if message != "":
			message = message + " "
		message = message + str(arg)
	quick_print(prefix, message)

def debug(args, override = False):
	if not enabled_debug and not override:
		return
	prefix = "[Dbg]:"
	message = ""
	for arg in args:
		if message != "":
			message = message + " "
		message = message + str(arg)
	quick_print(prefix, message)

def main():
	x = 1
	y = 2
	quick_print("Static loglevel", static.loglevel)
	debug(["Validation failed at", (x, y), "-> east"])
	info(["Validation failed at", (x, y), "-> east"])
	warn(["Validation failed at", (x, y), "-> east"])
	error(["Validation failed at", (x, y), "-> east"])
	
if __name__ == "__main__":
	main()
