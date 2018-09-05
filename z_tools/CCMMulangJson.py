# -*- coding:utf-8 -*-

'''
ccm编辑器下多语言key转化为文本显示
'''

import os
import sys
import json

prefix_path = ''

read_path = ['script/data/common', 'language_zh']
out_path = 'res/info/uieditor_multilang_conf'


def create_json():
    file_prefix_path = os.path.join(prefix_path, read_path[0])
    list_dir = os.listdir(file_prefix_path)
    module_name = ''
    for name in list_dir:
        if name.find(read_path[1]) != -1:
            module_name = name
    if module_name:
        # 读取module
        sys.path.append(file_prefix_path)
        sys.path.append(os.path.join(prefix_path, 'script/lib'))
        module = __import__(read_path[1], fromlist=[''])
        if module:
            data = getattr(module, 'data')
            if data:
                output_data = {}
                for key, content in data.iteritems():
                    output_data[key] = {'1': content.get('value', '')}
                with open(os.path.join(prefix_path, out_path), 'w') as writter:
                    json_str = json.dumps(output_data, ensure_ascii=False, indent=1)
                    writter.write(json_str)


if __name__ == '__main__':
    path = os.path.realpath(__file__)
    dir_path = os.path.split(path)[0]
    global prefix_path
    prefix_path = os.path.join(dir_path)
    create_json()
