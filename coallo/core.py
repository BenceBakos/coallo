
from pathlib import Path
import sys

def load_file():
	args = sys.argv
	del args[0]

	if len(args) == 0:
		raise Exception("File path must be specified! (First argument)")
		exit()

	model_file = Path(args[0])

	if not model_file.exists():
		raise Exception("File '"+args[0]+"' does not exits!")
		exit()

	if not model_file.is_file():
		raise Exception("Path '"+args[0]+"' must point to a file!")
		exit()

	return model_file.read_text()

import json
def main():

	# load file content

	# parse file
	from coallo.parse import parse_file

	elements = parse_file(load_file())

	print(json.dumps(elements))

	# visualize

	from coallo.visualize import visualize_default

	visualize_default(elements)
