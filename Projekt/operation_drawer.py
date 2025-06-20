# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 11:37:56 2025

@author: Jakub
"""

import tkinter as tk

FONT_SIZE = 14
TEXT_PAD_X = 10
TEXT_PAD_Y = 5
BRACKET_WIDTH = 15


def draw_horizontal_operation(canvas, param1, param2, start_x, start_y, separator_char):
    all_drawn_items = []
    
    content_start_x = start_x + BRACKET_WIDTH + TEXT_PAD_X
    content_y = start_y + TEXT_PAD_Y

    p1_id = canvas.create_text(content_start_x, content_y, text=param1, anchor="nw", font=("Consolas", FONT_SIZE))
    all_drawn_items.append(p1_id)
    
    p1_bbox = canvas.bbox(p1_id)
    separator_text = f" {separator_char} " 
    separator_x = p1_bbox[2]
    separator_id = canvas.create_text(separator_x, content_y, text=separator_text, anchor="nw", font=("Consolas", FONT_SIZE))
    all_drawn_items.append(separator_id)

    separator_bbox = canvas.bbox(separator_id)
    p2_x = separator_bbox[2]
    p2_id = canvas.create_text(p2_x, content_y, text=param2, anchor="nw", font=("Consolas", FONT_SIZE))
    all_drawn_items.append(p2_id)

    min_x_content = min(canvas.bbox(item)[0] for item in all_drawn_items if canvas.bbox(item))
    max_x_content = max(canvas.bbox(item)[2] for item in all_drawn_items if canvas.bbox(item))
    min_y_content = min(canvas.bbox(item)[1] for item in all_drawn_items if canvas.bbox(item))
    max_y_content = max(canvas.bbox(item)[3] for item in all_drawn_items if canvas.bbox(item))
    
    content_height = max_y_content - min_y_content

    bracket_font_scale = 1.5
    bracket_vertical_center = min_y_content + content_height / 2

    bracket_left_id = canvas.create_text(min_x_content - TEXT_PAD_X, bracket_vertical_center, 
                                        text="(", anchor="e", font=("Consolas", int(FONT_SIZE * bracket_font_scale)), fill="black")
    bracket_right_id = canvas.create_text(max_x_content + TEXT_PAD_X, bracket_vertical_center, 
                                         text=")", anchor="w", font=("Consolas", int(FONT_SIZE * bracket_font_scale)), fill="black")
    all_drawn_items.extend([bracket_left_id, bracket_right_id])

    arc_offset_y = 5
    arc_start_x = canvas.bbox(bracket_left_id)[0]
    arc_end_x = canvas.bbox(bracket_right_id)[2]
    
    arc_y = min(canvas.bbox(bracket_left_id)[1], canvas.bbox(bracket_right_id)[1]) - arc_offset_y
    arc_height_segment = 5
    
    canvas.create_line(arc_start_x, arc_y + arc_height_segment, 
                       (arc_start_x + arc_end_x) / 2, arc_y, 
                       arc_end_x, arc_y + arc_height_segment, 
                       smooth=True, fill="black", width=3)
    
    all_bboxes = [canvas.bbox(item) for item in all_drawn_items if canvas.bbox(item)]
    
    if not all_bboxes:
        return 0, 0 

    overall_min_x = min(bbox[0] for bbox in all_bboxes)
    overall_max_x = max(bbox[2] for bbox in all_bboxes)
    overall_min_y = min(bbox[1] for bbox in all_bboxes)
    overall_max_y = max(bbox[3] for bbox in all_bboxes)

    final_width = overall_max_x - overall_min_x + TEXT_PAD_X
    final_height = (overall_max_y - overall_min_y) + arc_height_segment + arc_offset_y + TEXT_PAD_Y

    return final_width, final_height


def draw_vertical_operation(canvas, param1_content, param2_content, start_x, start_y, separator_char):
    elements_info = []
    current_y = start_y + TEXT_PAD_Y
    max_content_width = 0

    content_x_offset = start_x + BRACKET_WIDTH + TEXT_PAD_X
    
    if isinstance(param1_content, dict) and param1_content.get('type') == 'pozioma':
        p1_width, p1_height = draw_horizontal_operation(canvas, param1_content['param1'], param1_content['param2'], content_x_offset, current_y, separator_char)
        elements_info.append({'x': content_x_offset, 'y': current_y, 'width': p1_width, 'height': p1_height})
        max_content_width = max(max_content_width, p1_width)
        current_y += p1_height + TEXT_PAD_Y
    else:
        p1_id = canvas.create_text(content_x_offset, current_y, text=param1_content, anchor="nw", font=("Consolas", FONT_SIZE))
        bbox = canvas.bbox(p1_id)
        width = bbox[2] - bbox[0] if bbox else 0
        height = bbox[3] - bbox[1] if bbox else FONT_SIZE
        elements_info.append({'x': bbox[0], 'y': bbox[1], 'width': width, 'height': height})
        max_content_width = max(max_content_width, width)
        current_y += height + TEXT_PAD_Y

    separator_text = separator_char
    sep_id = canvas.create_text(content_x_offset, current_y, text=separator_text, anchor="nw", font=("Consolas", FONT_SIZE))
    bbox = canvas.bbox(sep_id)
    width = bbox[2] - bbox[0] if bbox else 0
    height = bbox[3] - bbox[1] if bbox else FONT_SIZE
    elements_info.append({'x': bbox[0], 'y': bbox[1], 'width': width, 'height': height})
    max_content_width = max(max_content_width, width)
    current_y += height + TEXT_PAD_Y

    if isinstance(param2_content, dict) and param2_content.get('type') == 'pozioma':
        p2_width, p2_height = draw_horizontal_operation(canvas, param2_content['param1'], param2_content['param2'], content_x_offset, current_y, separator_char)
        elements_info.append({'x': content_x_offset, 'y': current_y, 'width': p2_width, 'height': p2_height})
        max_content_width = max(max_content_width, p2_width)
        current_y += p2_height + TEXT_PAD_Y
    else:
        p2_id = canvas.create_text(content_x_offset, current_y, text=param2_content, anchor="nw", font=("Consolas", FONT_SIZE))
        bbox = canvas.bbox(p2_id)
        width = bbox[2] - bbox[0] if bbox else 0
        height = bbox[3] - bbox[1] if bbox else FONT_SIZE
        elements_info.append({'x': bbox[0], 'y': bbox[1], 'width': width, 'height': height})
        max_content_width = max(max_content_width, width)
        current_y += height + TEXT_PAD_Y

    if not elements_info:
        return 0, 0

    min_y_content_overall = min(info['y'] for info in elements_info)
    max_y_content_overall = max(info['y'] + info['height'] for info in elements_info)
    total_content_height = max_y_content_overall - min_y_content_overall
    
    bracket_line_width = 2

    arc_bbox_x1 = start_x
    arc_bbox_y1 = min_y_content_overall
    
    arc_bbox_x2 = start_x + BRACKET_WIDTH * 2
    arc_bbox_y2 = max_y_content_overall

    canvas.create_arc(arc_bbox_x1, arc_bbox_y1, arc_bbox_x2, arc_bbox_y2,
                      start=90, extent=180,
                      style=tk.ARC, outline="black", width=bracket_line_width)

    final_width = max_content_width + BRACKET_WIDTH + (2 * TEXT_PAD_X)
    final_height = total_content_height + (2 * TEXT_PAD_Y)

    return final_width, final_height


def draw_operation_smartly(canvas, op_data, start_x, start_y, separator_char):
    if op_data['type'] == 'pozioma':
        return draw_horizontal_operation(canvas, op_data['param1'], op_data['param2'], start_x, start_y, separator_char)
    elif op_data['type'] == 'pionowa':
        return draw_vertical_operation(canvas, op_data['param1'], op_data['param2'], start_x, start_y, separator_char)
    else:
        canvas.create_text(start_x, start_y, text=f"Nieznany typ operacji: {op_data['type']}", anchor="nw", fill="red")
        return 100, 20