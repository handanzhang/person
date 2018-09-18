# -*- coding:utf-8 -*-
'''
	检查json中的button checkbutton textfield，修改默认的label字体
'''

import os
import sys
from collections import defaultdict
import json

def read_json_file(absolute_path):
    json_object = None
    with open(absolute_path, 'r') as reader:
        json_object = json.load(reader)
        scan_json_file(json_object)

    if json_object:
        with open(absolute_path, 'w') as writter:
            json.dump(json_object, writter, indent=2)


check_set = {'CCButton', 'CCEditBoxExt'}
def scan_json_file(json_object):
    for key, value in json_object.items():
        if key is unicode:
            key =  unicode.encode(key, 'utf-8')
        if key == 'type_name' and value in check_set:
            print key, value
            json_object['fontName'] = "gui/fonts/simhei_plus.ttf"

        if key == 'child_list':
            for child in value:
                scan_json_file(child)

# 扫描字符 取脚本所在的路径为初始路径
if __name__ == '__main__':
    path = os.path.realpath(__file__)
    root_path, _ = os.path.split(path)

    if len(sys.argv) < 2:
        print '没有足够的参数'
    else:
        file_path= sys.argv[1]

        if file_path.find('/') != -1:
            absolute_path = file_path
        else:
            absolute_path = os.path.join(root_path, file_path)
        print 'absolute path: %s' %absolute_path
        read_json_file(absolute_path)

