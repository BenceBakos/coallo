
from pathlib import Path
import sys
import os

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
	text_raw = load_file()

	# working directory to coallo's folder 
	abspath = os.path.abspath(__file__)
	dname = os.path.dirname(abspath)
	os.chdir(dname+ "/..")

	# parse file
	from coallo.parse import parse_file

	elements = parse_file(text_raw)

	#print(json.dumps(elements))

	# visualize

	from coallo.visualize import visualize_default

	visualize_default(elements)
