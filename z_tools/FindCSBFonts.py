# -*- coding:utf-8 -*-
'''
查找csd文件中字体资源的引用
'''



import os
import sys
import xml.dom.minidom as minidom
from collections import defaultdict
exist_csd_file = []
fonts_file = defaultdict(list)

class OutPutInfo(object):
    def __init__(self, file_name, parnet_name):
        self.file_name = file_name
        self.parnet_name = parnet_name


def read_exist_csd_file(root_path):
    for path, sub_path, files in os.walk(root_path):
        for file_name in files:
            if file_name.endswith('.csd'):
                exist_csd_file.append(os.path.join(path, file_name))


def parse(file_path_collection):
    for file_path in file_path_collection:
        dom_tree = minidom.parse(file_path)
        if not dom_tree:
            continue
        elements = dom_tree.documentElement.getElementsByTagName('FontResource')

        for ele in elements:
            fonts_file[ele.getAttribute('Path')].append(OutPutInfo(file_path, ele.parentNode.getAttribute('Name')))


# 扫描字符 取脚本所在的路径为初始路径
if __name__ == '__main__':
    path = os.path.realpath(__file__)			
    root_path, _ = os.path.split(path)
    read_exist_csd_file(root_path)
    parse(exist_csd_file)
    out_put_str = ''
    for key, value in fonts_file.iteritems():
        out_put_str += key + '\n'
        for v in value:
            out_put_str += '\t' + v.file_name + '\t' + v.parnet_name + '\n'
    with open(os.path.join(root_path, u'CSB文件包含的字体.txt'), 'w') as writter:
        writter.write(out_put_str)

