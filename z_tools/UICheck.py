# -*- coding:utf-8 -*-
'''
	检查导出的 language_xx.py 表中不存在的key
'''

import os
import sys
from collections import defaultdict

exist_files = []
fonts_file = defaultdict(list)

langugae_module_data = {}

def read_language_file_path(root_path):
    sys.path.append(root_path)
    sys.path.append(os.path.join(root_path, 'script/lib'))

    language_list = []
    for path, sub_path, files in os.walk(os.path.join(root_path, 'script/data/common/')):
        for file_name in files:
            if file_name.startswith('language') and file_name.endswith('.pyc'):
                sub_path = 'script.data.common.%s' %file_name[:-4]
                module = __import__(sub_path, fromlist=[''])
                langugae_module_data[file_name[:-4]] = module.data

def check_module(root_path):
    not_found_key = defaultdict(list)
    for name, module_data in langugae_module_data.iteritems():
        for check_name, check_data in langugae_module_data.iteritems():
            if name == check_name:
                continue
            
            for key in module_data.iterkeys():
                if key not in check_data:
                    not_found_key[key].append(check_name)

    out_put_str = ''
    for key, name_list in not_found_key.iteritems():
        out_put_str += '\n%s\t' %key
        for name in name_list:
            out_put_str += '%s\t' %name
    
    with open(os.path.join(root_path, u'查找结果.txt'), 'w') as writter:
        writter.write(out_put_str)




# 扫描字符 取脚本所在的路径为初始路径
if __name__ == '__main__':
    path = os.path.realpath(__file__)			
    root_path, _ = os.path.split(path)
    read_language_file_path(root_path)
    check_module(root_path)

