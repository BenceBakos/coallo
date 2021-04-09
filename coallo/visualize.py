
from PIL import Image,ImageDraw

import math

def recursive_depth(children,d):

	if len(children) == 0:
		return d

	for ch in children:

		r = recursive_depth(ch['children'],d)

		if r > d:
			d = r

	return d + 1

def recursive_child_sum(children,sum):

	if len(children) == 0:return 1

	for ch in children:
		sum += recursive_child_sum(ch['children'],sum)

	return sum -1



filename = "visual.png"


# BOUNDING BOX SIZES
px_item_ellipse_height = 50
px_item_line_height = 50
px_item_height = px_item_line_height + px_item_ellipse_height

px_item_ellipse_width = 50
px_item_line_width = 50
px_item_width = px_item_line_width + px_item_ellipse_width


def draw_branch_item(name,x,y,draw,first = False):
	if first:
		draw.ellipse((x,y,x + px_item_ellipse_width,y + px_item_ellipse_height), fill="white", outline="black")
	else:
		draw.ellipse((x,y,x + px_item_ellipse_width,y + px_item_ellipse_height), fill="white", outline="black")

def recursive_draw_children(children, curr_x, curr_y, draw):

	ch_count_half = math.floor(len(children))

	first_ch = True

	for ch in children:

		if first_ch:
			draw_branch_item(ch['name'],curr_x,curr_y,draw,True)
		else:
			draw_branch_item(ch['name'],curr_x,curr_y,draw)

		curr_y += px_item_height





def visualize_default(elements):
	branches = elements['branches']

	root = False
	for (name,br) in branches.items():
		if br['root']:
			root = br

	if not root:
		raise Exception("At least one root must exists!")

	depth = recursive_depth(root['children'],0)
	
	# sum of children (height) 
	children_sum = recursive_child_sum(root['children'],0)

	#draw recursively
	img_width  = depth * px_item_width + 200
	img_height = children_sum * px_item_height + 200
	print(img_width)
	print(img_height)
	print("----------")
	img = Image.new('RGB', (img_width, img_height), color = 'white')

	draw = ImageDraw.Draw(img)

	recursive_draw_children(root['children'],math.floor(img_width * 0.01),math.floor(img_height * 0.01),draw)

	img.save(filename)