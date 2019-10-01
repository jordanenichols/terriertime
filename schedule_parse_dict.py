#!/usr/bin/env python3
from PIL import Image
import math
import json

def init_image(schedule):
    image = Image.open(schedule)
    image = image.convert('L')
    return image
def init_week():
    week = {}
    week['Days'] = []
    week['Days'].append({
	'name': 'Sunday',
	'class_time': []
    }) 
    week['Days'].append({
	'name': 'Monday',
	'class_time': []
    })
    week['Days'].append({
	'name': 'Tuesday',
	'class_time': []
    })
    week['Days'].append({
	'name': 'Wednesday',
	'class_time': []
    })
    week['Days'].append({
	'name': 'Thursday',
	'class_time': []
    })
    week['Days'].append({
	'name': 'Friday',
	'class_time': []
    })
    week['Days'].append({
	'name': 'Saturday',
	'class_time': []
    })
    return week
def calc_hour(pix):
	return (pix-20) // 24 + 7	
def calc_min(pix):
	return 5 * round(((pix - ((calc_hour(pix) - 7) * 24 + 20)) * (60/23)) / 5)
def parse_image(week, image):
	x = [92, 153, 215, 278, 340, 402, 464]
	for current_day in range(7):
		current_day_coords = []
		for current_y in range(20,404):
			current_pixel = image.getpixel((x[current_day], current_y))
			if not current_pixel in [255,204]:
				current_day_coords.append(current_y)
		gaps = [[s,e] for s, e in zip(current_day_coords, current_day_coords[1:]) if s+1 < e]
		edges = iter(current_day_coords[:1] + sum(gaps, []) + current_day_coords[-1:])
		current_day_blocks = list(zip(edges, edges))
		current_day_times = []
		for block in current_day_blocks:
			class_begin = [calc_hour(block[0]), calc_min(block[0])]
			class_end = [calc_hour(block[1]), calc_min(block[1])]    
			current_day_times.append((class_begin,class_end))
		week['Days'][current_day]['class_time'] = current_day_times
def convert_to_json(week):
	with open('schedule.json', 'w', encoding = 'utf-8') as json_file:
		json.dump(week, json_file, ensure_ascii = False, indent = 4)
image = init_image("ScheduleImageServlet.gif")
week = init_week()
parse_image(week, image)
convert_to_json(week)
