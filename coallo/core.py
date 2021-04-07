from pathlib import Path
import json


# config
"""
{
	"visualizer": "default",         #switch between visualizer methods ar possible, visit coallo/visualize.py
	"json-error-output": true,		 
	"json-visualizer-output": false	
}
"""
config = json.loads(Path('conf.json').read_text())


# cli arguments(overwrite config)
"""
	(first argument is mandatory, others are optional, also order of the rest is optional)
	arguments separated with spaces: 
	 - model file path
	 - visualizer=default
	 - json-error-output=true
	 - json-visualizer-output=false
"""

import sys
args = sys.argv
del args[0]

# read model text
import coallo.parse


# parse coallo and return with elements:
# syntax errors (repeating names, bad method/circle/type names, embedded lists, unexpected tokens)
# {"types":{Type1...},"circles":{Circle1...}, "methods":{Method1...} }

# run checks (raises errors like "Missing return type Int"...)

# visualization