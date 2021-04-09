

template_branch = lambda name = "",children = [],root = False:{"name":name,"children":children,"root":root}

def find_branch_children(branches):

	branch_names = []
	for (name,br) in branches.items():
		if br['root']:continue

		branch_names.append(name)

	def recursive_find_children(children):
		for i in range(0,len(children)):
			ch = children[i]
			if ch['name'] in branch_names:
				children[i] = branches[ch['name']]
				children[i]['children'] = recursive_find_children(children[i]['children'])

		return children

	for (name,br) in branches.items():
		try:
			branches[name]['children'] = recursive_find_children(branches[name]['children'])

		except RecursionError as re:
			print('Recursion error!')
			print(re.args[0])
			exit()

	return branches

def get_name(line,indicator):
	return " ".join(line.replace(indicator,'',1).split()).split(' ')[0]

def parse_file(file_text):

	elements = {"branches":{}}

	lines = file_text.split('\n')

	active_branch = False

	# get elements

	for line in lines:

		line_without_whitespace = line.replace(' ','').replace('\t','')

		# root branch
		if line_without_whitespace.startswith('##') and not line_without_whitespace.startswith('###'):
			name = get_name(line,'##')
			elements['branches'][name] = template_branch(name,[],True)

			active_branch = name

			continue

		# branch
		if line_without_whitespace.startswith('###'):
			name = get_name(line,'###')

			elements['branches'][name] = template_branch(name,[])

			active_branch = name

			continue

		# -/* list item branch
		if line_without_whitespace.startswith('-') or line_without_whitespace.startswith('*'):
			
			if active_branch == False:
				continue

			indicator = '*'
			if line_without_whitespace.startswith('-'):
				indicator = '-'

			name = get_name(line,indicator)

			elements['branches'][active_branch]['children'].append(template_branch(name,[]))

			continue

		# non-coallo line
		active_branch = False

	elements['branches'] = find_branch_children(elements['branches'])


	return elements