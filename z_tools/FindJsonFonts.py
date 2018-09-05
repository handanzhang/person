# -*- coding:utf-8 -*-
'''
	查找字体在json中的引用
'''

import os
import sys
import json
from collections import defaultdict

exist_files = []
fonts_file = defaultdict(list)


def read_exist_json_file(root_path):
    for path, sub_path, files in os.walk(os.path.join(root_path, 'res/gui/template/')):
        for file_name in files:
            if file_name.endswith('.json'):
                exist_files.append(os.path.join(path, file_name))


def parse(exist_files):
    for file_path in exist_files:
        with open(file_path, 'r') as reader:
        	json_dict = json.load(reader)
        	parse_unit(json_dict, file_path)

def parse_unit(json_dict, file_path):
	for key, value in json_dict.iteritems():
		if key == 'child_list':
			for child in value:
				parse_unit(child, file_path)
		elif key == 'fontName':
			list_path = fonts_file[value]
			if fonts_file not in list_path:
				list_path.append(file_path)

# 扫描字符 取脚本所在的路径为初始路径
if __name__ == '__main__':
    path = os.path.realpath(__file__)			
    root_path, _ = os.path.split(path)
    read_exist_json_file(root_path)
    parse(exist_files)
    out_put_str = ''
    for key, value in fonts_file.iteritems():
        out_put_str += key + '\n'
        for v in value:
            out_put_str += '\t' + v + '\n'
    with open(os.path.join(root_path, u'Json文件包含的字体.txt'), 'w') as writter:
        writter.write(out_put_str)

