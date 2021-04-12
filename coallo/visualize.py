
from PIL import Image,ImageDraw, ImageFont

import math


colors = [(105, 105, 105),(128, 128, 128),(169, 169, 169),(192, 192, 192),(47, 79, 79),(85, 107, 47),(139, 69, 19),(107, 142, 35),
(160, 82, 45),(165, 42, 42),(46, 139, 87),(34, 139, 34),(127, 0, 0),(25, 25, 112),(0, 100, 0),(139, 0, 0),(128, 128, 0),(72, 61, 139),
(178, 34, 34),(95, 158, 160),(119, 136, 153),(0, 128, 0),(60, 179, 113),(188, 143, 143),(102, 51, 153),(184, 134, 11),(189, 183, 107),
(0, 139, 139),(205, 133, 63),(70, 130, 180),(210, 105, 30),(154, 205, 50),(32, 178, 170),(205, 92, 92),(0, 0, 139),(75, 0, 130),
(50, 205, 50),(218, 165, 32),(127, 0, 127),(143, 188, 143),(139, 0, 139),(176, 48, 96),(210, 180, 140),(72, 209, 204),(102, 205, 170),
(153, 50, 204),(255, 0, 0),(255, 69, 0),(0, 206, 209),(255, 140, 0),(255, 165, 0),(255, 215, 0),(106, 90, 205),(255, 255, 0),(199, 21, 133),
(0, 0, 205),(222, 184, 135),(64, 224, 208),(127, 255, 0),(0, 255, 0),(148, 0, 211),(186, 85, 211),(0, 250, 154),(138, 43, 226),(0, 255, 127),
(65, 105, 225),(233, 150, 122),(220, 20, 60),(0, 255, 255),(0, 191, 255),(244, 164, 96),(147, 112, 219),(0, 0, 255),(160, 32, 240),(240, 128, 128),
(173, 255, 47),(255, 99, 71),(218, 112, 214),(216, 191, 216),(176, 196, 222),(255, 127, 80),(255, 0, 255),(30, 144, 255),(219, 112, 147),
(240, 230, 140),(250, 128, 114),(238, 232, 170),(255, 255, 84),(100, 149, 237),(221, 160, 221),(176, 224, 230),(135, 206, 235),(255, 20, 147),
(123, 104, 238),(255, 160, 122),(238, 130, 238),(152, 251, 152),(135, 206, 250),(127, 255, 212),(255, 105, 180)]


color_to_branch = {}
color_index = 0

def recursive_color_to_branch(branch):
	global color_index
	global color_to_branch

	if branch['name'] not in color_to_branch:
		color_to_branch[branch['name']] = colors[color_index]
		color_index += 1

		if color_index == len(colors) - 1:
			color_index = 0
			print("WARNING! Colors are repetitive now!")

	for br in branch['children']:
		recursive_color_to_branch(br)


def recursive_longest_name(children,max_len):

	if len(children) == 0:return max_len

	for ch in children:
		if len(ch['name']) > max_len:
			max_len = len(ch['name'])

		recursive_res = recursive_longest_name(ch['children'],max_len)

		if recursive_res > max_len:
			max_len = recursive_res

	return max_len

def draw_branch_item(draw,name,x,y,width,height,color):
	draw.ellipse((x,y,x + width,y + height), fill="white", outline=color)

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

px_ellipse_padding = 10
px_line_padding = 3
px_line_width = 2

px_roots_padding = 30

def recursive_build_graph(branch,is_beginner, is_ending):
	is_beginner_local = is_beginner
	is_ending_local = is_ending

	color = "black"
	#background_color = color_to_branch[branch['name']]

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
		image = Image.new('RGBA', (width, height), color = (255,255,255,0))
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
		
		
		# "curve"
		
		# vertical to
		if not branch['root']:
			draw.line( (item_width_half, px_line_padding, item_width_half ,height- px_line_padding), fill=color, width=px_line_width)
		
		# Vertical from
		draw.line( (item_width_half + px_ellipse_padding, px_line_padding, item_width_half + px_ellipse_padding ,height - px_line_padding), fill=color, width=px_line_width)
		
		# horizontal top
		draw.line( (item_width_half + px_ellipse_padding, px_line_padding, (3*item_width_half + px_ellipse_padding) ,px_line_padding), fill=color, width=px_line_width)
		
		#horizontal bottom
		draw.line( (item_width_half + px_ellipse_padding, height-px_line_padding, (3*item_width_half + px_ellipse_padding) ,height-px_line_padding), fill=color, width=px_line_width)


		# connector line
		draw.line( (item_width_half, line_start_x, item_width_half ,line_end_x), fill=color, width=px_line_width)

		draw_branch_item(draw,branch['name'],branch_x,branch_y,px_ellipse_width(),px_ellipse_height(),color)

	else:
		width = px_ellipse_width() + px_ellipse_padding
		height = px_ellipse_height() + (2 * px_line_length)
		image = Image.new('RGBA', (width, height), color = (255,255,255,0))
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

		# vertical to
		if not branch['root']:
			draw.line( (width_half, px_line_padding, width_half ,height - px_line_padding), fill=color, width=px_line_width)
		
		draw.line( (width_half, line_start_x, width_half ,line_end_x), fill=color, width=px_line_width)
		
		draw_branch_item(draw,branch['name'],branch_x,branch_y,px_ellipse_width(),px_ellipse_height(),color)
				

	return image




def visualize_default(elements):
	global longest_name
	global color_to_branch
	branches = elements['branches']
	

	for (name,br) in branches.items():
		recursive_color_to_branch(br)
	
	root = False

	root_images = []

	width_sum  = 0
	height_max = 0

	for (name,br) in branches.items():
		if br['root']:
			root = br
			longest_name = recursive_longest_name(root['children'],len(root['name']))

			img_res = recursive_build_graph(root,True,True)

			width_sum += img_res.width

			if img_res.height > height_max:
				height_max = img_res.height

			root_images.append(img_res)

	if not root:
		raise Exception("At least one root must exists!")
	

	result_img = Image.new('RGB', (width_sum + (len(root_images) * px_roots_padding), height_max), color = "white")
	
	last_x = 0

	for root_img in root_images:
		result_img.paste(root_img,(last_x,0))

		last_x += root_img.width + px_roots_padding

	result_img.save("visual.png")
	result_img.show()