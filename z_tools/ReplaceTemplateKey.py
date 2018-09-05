
# -*- coding:utf-8 -*-
'''
 template文件替换对应值
'''

import os
import sys
import json
from collections import defaultdict


find_path = ''
replace_key = ''
replace_value = ''


def read_exist_json_file(root_path):
    ret = []
    for path, sub_path, files in os.walk(os.path.join(root_path, find_path)):
        for file_name in files:
            if file_name.endswith('.json'):
                ret.append(os.path.join(path, file_name))
    return ret

def parse(exist_files):
    for file_path in exist_files:
        json_dict = {}
        changed = False
        with open(file_path, 'r') as io:
            json_dict = json.load(io)
            changed = parse_unit(json_dict, file_path)

        if json_dict and changed:
            with open(file_path, 'w') as io:
                json.dump(json_dict, io, indent=4, separators=(',', ': '))

def parse_unit(json_dict, file_path):
    changed = False
    for key in json_dict.iterkeys():
        if key == 'child_list':
            value = json_dict[key]
            for child in value:
                if parse_unit(child, file_path):
                    changed = True
        elif key == replace_key:
            json_dict[key] = replace_value
            changed = True
    return changed

# 扫描字符 取脚本所在的路径为初始路径
if __name__ == '__main__':

    find_path = 'gui/template/'
    replace_key = sys.argv[1]
    replace_value = sys.argv[2]
    path = os.path.realpath(__file__)
    root_path, _ = os.path.split(path)
    ret = read_exist_json_file(root_path)
    parse(ret)
