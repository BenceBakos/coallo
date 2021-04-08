


class Model:
	def __init__(self):
		self.elements_cicrle = {}
		self.elements_type = {}

		self.last_circle_key = False
		
		self.last_method_key = False

		self.reserved_keywords = ['extends']


class Process_result:
	def __init__(self,model,errors):
		self.model = model
		self.errors = errors


class Line_processor:
	def __init__(self, processor_method,indicator):
		self.processor_method = processor_method	
		self.indicator = indicator

	def process(self,line,line_number,model):

		def line_without_whitespace(str):
			return str.replace(' ','').replace('\t','')

		if isinstance(self.indicator,list):
			is_indicator = False

			for ind in self.indicator:
				is_indicator = is_indicator or line_without_whitespace(line).startswith(ind)

			if not is_indicator:
				return False
		else:
			if not line_without_whitespace(line).startswith(self.indicator):
				return False
		
		return self.processor_method(line,line_number,model)


# header 3

class Element_type:
	def __init__(self,name,parent=False):
		self.name = name
		self.parent = parent

def process_type(line,line_number,model):
	line = line.replace("###","")
	line_splitted = line.split(" ")

	words = []
	
	# filter empty string
	for word in line_splitted:
		if word == "" or word == "\t":continue

		words.append(word)

	if words[0] in model.elements_type:
		return Process_result(model,[[line_number,"Type already exists!"]])
	
	if  not len(words) == 1 and not len(words) == 3:
		return Process_result(model,[[line_number,"Wrong number of keywords!"]])	
	
	if len(words) == 3:
		if words[1] != "extends":
			return Process_result(model,[[line_number,"Wrong keyword order!"]])

		if words[0] == words[2]:
			return Process_result(model,[[line_number,"Type can't be it's own parent!"]])			

		if words[0] in model.reserved_keywords:
			return Process_result(model,[[line_number,"Type name reserved!"]])			

		model.elements_type[words[0]] = Element_type(words[0],words[2])
		model.reserved_keywords.append(words[0])

	if len(words) == 1:

		if words[0] in model.reserved_keywords:
			return Process_result(model,[[line_number,"Type name reserved!"]])			

		model.elements_type[words[0]] = Element_type(words[0])
		model.reserved_keywords.append(words[0])

	return Process_result(model,[])



# header 2

class Element_circle:
	def __init__(self,name,in_types = False,out_types = False, methods=False):
		self.name = name

		if out_types:
			self.out_types = out_types
		else:
			self.out_types = []

		if in_types:
			self.in_types = in_types
		else:
			self.in_types = []

		if (methods):
			self.methods = methods
		else:
			self.methods = []

def process_circle(line,line_number,model):
	
	is_circle = False
	if "## " in line:
		is_circle = True

	line = line.replace("##","")
	line_splitted = line.split(" ")

	words = []
	
	# filter empty string
	for word in line_splitted:
		if word == "" or word == "\t":continue

		words.append(word)

	types_in = []
	types_out = []
	name = ""

	if len(words) == 0 or len(words) > 3:
		return Process_result(model,[[line_number,"Wrong number of keywords!"]])

	if len(words) == 1 and words[0] in model.reserved_keywords:
		return Process_result(model,[[line_number,"Circle name reserved!"]])

	if len(words) == 2 and (not words[0].startswith('**') or not words[1].startswith('**')) and\
		(not words[0].endswith('**') or not words[1].endswith('**')):

		return Process_result(model,[[line_number,"Invalid type declaration!"]])

	if len(words) == 3 and not words[0].startswith('**') and not words[2].startswith('**') and\
		not words[0].endswith('**') and not words[2].endswith('**'):

		return Process_result(model,[[line_number,"Invalid type declaration!"]])

	if (len(words) == 2 and words[0].startswith('**')) or len(words) == 3:

		types_in_str = words[0].replace('*','').split(',')

		for type_in_str in types_in_str:
			if not type_in_str in model.elements_type:
				return Process_result(model,[[line_number,"Input type does not exists!"]])

			types_in.append(model.elements_type[type_in_str])

	if (len(words) == 2 and words[1].startswith('**')) or len(words) == 3:
		types_out_str = ""

		if len(words) == 2:
			types_out_str = words[1].replace('*','').split(',')
		else:
			types_out_str = words[2].replace('*','').split(',')

		for type_out_str in types_out_str:
			if not type_out_str in model.elements_type:
				return Process_result(model,[[line_number,"Output type does not exists!"]])

			types_in.append(model.elements_type[type_out_str])

	if len(words) == 1:
		name = words[0]

	if len(words) == 2:
		if words[0].startswith('**'):
			name = words[1]
		else:
			name = words[0]

	if len(words) == 3:
		name = words[1]

	model.elements_cicrle[name] = Element_circle(name,types_in,types_out)

	if is_circle:
		model.last_circle_key = name
	else:
		model.last_method_key = name

	return Process_result(model,[])


# list item

class Element_circle_method:
	def __init__(self,name, in_types,out_types):
		self.name = name
		self.in_types = in_types
		self.out_types = out_types


def process_circle_method(line,line_number,model):
	
	while line[0] != '-' or line[0] != '*':
		line = line[1:]
	
	line = line[1:]

	circ_r = process_circle(line,line_number,model)

	## append method to current circle
	circ_r.model.elements_cicrle[circ_r.model.last_circle_key].methods.append(circ_r.model.elements_cicrle[circ_r.model.last_method_key])

	return circ_r


line_processors = [
	Line_processor(process_type,"###"),
	Line_processor(process_circle,"##"),
	Line_processor(process_circle_method,['-','*']),
]

# returns dict: {"errors":[...],"model":{}}
def parse(raw_str):
	errors = []
	model = Model()

	str_lines = raw_str.split('\n')
	
	line_number = 1
	#process lines
	for line in str_lines:

		# skip empty
		if line == "":continue

		# process coallo lines
		process_result = False

		for line_processor in line_processors:
			process_result = line_processor.processor_method(line,line_number,model)
			if isinstance(process_result,Process_result):
				errors = errors + process_result.errors
				model = process_result.model
				continue

	line_number += 1

	# check type parents declared correctly!

	return Process_result(model,errors)