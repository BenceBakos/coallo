
from PIL import Image,ImageDraw, ImageFont

import math

def recursive_longest_name(children,max_len):

	if len(children) == 0:return 0

	for ch in children:
		if len(ch['name']) > max_len:
			max_len = len(ch['name'])

	recursive_res = recursive_longest_name(ch['children'],max_len)

	if recursive_res > max_len:
		max_len = recursive_res

	return max_len

def draw_branch_item(draw,name,x,y,width,height):
	draw.ellipse((x,y,x + width,y + height), fill="white", outline="black")

	text_x  = math.floor( (width - ( len(name) * px_char_width ) ) / 2 )
	text_y = math.floor(height * 0.5) - px_char_height
	draw.text((x + text_x,y + text_y),name,font=fnt,fill = "black")


px_font_size = 13
fnt = ImageFont.truetype('coallo/Roboto-Regular.ttf', px_font_size)

px_char_width =  math.floor(px_font_size * 0.5)
px_char_height = math.floor(px_font_size * 0.8)

longest_name = ""

px_ellipse_width = lambda: math.floor(longest_name * px_char_width) + 20
px_ellipse_height = lambda: math.floor(px_ellipse_width() * 0.4) 

px_line_length = 10

px_ellipse_padding = 20

def recursive_build_graph(branch,is_beginner, is_ending):
	
	is_beginner_local = is_beginner
	is_ending_local = is_ending

	children_images = []

	width_max = 0

	height_sum = 0

	ch_count = 0

	for ch in branch['children']:

		is_beginner = ch_count == 0
		is_ending   = ch_count == len(branch['children']) - 1

		child_image = recursive_build_graph(ch,is_beginner,is_ending)
		children_images.append(child_image)

		# width maximum
		if child_image.width > width_max:
			width_max = child_image.width

		# height sum
		height_sum += child_image.height

		ch_count += 1

	image = None

	if len(branch['children']) > 0:
		width = px_ellipse_width() + px_ellipse_padding + width_max
		height = height_sum
		image = Image.new('RGB', (width, height), color = 'white')
		draw = ImageDraw.Draw(image)

		paste_x = px_ellipse_width() + px_ellipse_padding
		paste_y = 0

		for ch_img in children_images:
			image.paste(ch_img,(paste_x,paste_y))
			paste_y += ch_img.height

		branch_x = 0
		branch_y = math.floor((height/2) - (px_ellipse_height()/2))
		
		item_width_half = math.floor(px_ellipse_width() / 2)

		line_start_x = 0
		line_end_x = height

		if is_beginner_local:
			line_start_x = math.floor(height / 2)

		if is_ending_local:
			line_end_x = math.floor(height / 2)

		draw.line( (item_width_half, line_start_x, item_width_half ,line_end_x), fill="black", width=1)

		draw_branch_item(draw,branch['name'],branch_x,branch_y,px_ellipse_width(),px_ellipse_height())

	else:
		width = px_ellipse_width() + px_ellipse_padding
		height = px_ellipse_height() + (2 * px_line_length)
		image = Image.new('RGB', (width, height), color = 'white')
		draw = ImageDraw.Draw(image)

		branch_x = 0
		branch_y = px_line_length

		width_half = math.floor(px_ellipse_width() / 2)

		line_start_x = 0
		line_end_x = height

		if is_beginner_local:
			line_start_x = math.floor(height / 2)

		if is_ending_local:
			line_end_x = math.floor(height / 2)

		draw.line( (width_half, line_start_x, width_half ,line_end_x), fill="black", width=1)
		
		draw_branch_item(draw,branch['name'],branch_x,branch_y,px_ellipse_width(),px_ellipse_height())
				

	return image




def visualize_default(elements):
	global longest_name

	branches = elements['branches']
	root = False
	for (name,br) in branches.items():
		if br['root']:
			root = br

	if not root:
		raise Exception("At least one root must exists!")
	
	longest_name = recursive_longest_name(root['children'],0)
	if len(root['name']) > longest_name:
		longest_name = len(root['name'])

	
	recursive_build_graph(root,True,True).save("visual.png")