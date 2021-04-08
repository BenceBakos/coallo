from pathlib import Path
import json


### config
"""
{
	"visualizer": "default",         #switch between visualizer methods ar possible, visit coallo/visualize.py
	"json_error_output": true,		 
	"json_warning_output": true,		 
	"json_visualizer_output": false	,
	"only_parse": false,
	"only_warnings": false,
}
"""

config = json.loads(Path('conf.json').read_text())



### cli arguments
"""
	(first argument is mandatory, others are optional, also order of the rest is optional)
	arguments separated with spaces: 
	 - model file path
	 - visualizer=default
	 - json_error_output=true
	 - json_visualizer_output=false
"""

import sys
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

del args[0]

### overwrite cli arguments
for arg in args:
	splitted_arg = arg.split('=')

	if len(splitted_arg) != 2:
		continue

	config[splitted_arg[0]] = splitted_arg[1]

### read model text
raw_model_text = ""
try:
	raw_model_text = model_file.read_text()
except:
	raise Exception("Unable to read model file")


### parse model
# syntax errors (repeating names, bad method/circle/type names, embedded lists, unexpected tokens)
# {"types":{Type1...},"circles":{Circle1...}, "methods":{Method1...} }

import coallo.parse

parse_result = coallo.parse.parse(raw_model_text)

if parse_result and len(parse_result.errors) != 0:
	if config['json_error_output']:
		print("ERROR")
		print(json.dumps(parse_result.errors))
		exit()
	else:
		for e in parse_result.errors:
			print(json.dumps(e))

print(parse_result.model.elements_cicrle)
print(parse_result.model.elements_type)

"""
# run checks (raises errors like "Missing return type Int"...)
import coallo.warning

warnings = coallo.warning.warning(parse_result.model)


if len(warnings) != 0:
	print("WARNING")

	if config['json_warning_output']:
		print(json.dumps(warnings))
	else:
		for warn in warnings:
			print(warn)

# visualization
import coallo.visualize

if config['visualizer'] == "default":
	coallo.visualize.visualize_default(parse_result.model)
"""