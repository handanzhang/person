# -*- coding:utf-8 -*-

#文件路径 res/

# 根据合图plist生成json文件，使用ccm导出csb

import os
import xml.dom.minidom as minidom
import json

def get_plist_path(dir_path):
    out_put = []
    for name in os.listdir(dir_path):
        if os.path.isdir(name):
            continue
        if name.endswith('.plist'):
            out_put.append( os.path.join(dir_path, name))
    return out_put

# 读取plist里面的png路径
def read_plist(plist_path, path_dict):
    dom_tree = minidom.parse(plist_path)
    if not dom_tree:
        return
    root = dom_tree.documentElement
    png_node_list = []
    find_png_node(root, png_node_list)
    print plist_path, ' size: png_node_list:  ', len(png_node_list)
    plist_store_path = 'gui/packed_res/' + os.path.basename(plist_path)
    for node in png_node_list:
        path = node.data
        if path in path_dict:
            print 'conflict path：', path
        path_dict[path] = plist_store_path

# 查找png node
def find_png_node(node, png_node_list):
    for sub_node in node.childNodes:
        if sub_node.nodeType in (node.TEXT_NODE,):
            if sub_node.data.startswith('gui/'):
                png_node_list.append(sub_node)
        find_png_node(sub_node, png_node_list)

path = os.path.dirname(os.path.realpath(__file__))
plist_dir_path = os.path.join(path, 'gui/packed_res')
plist_file_path_list = get_plist_path(plist_dir_path)
path_dict = {} #路径映射
for plist_path in plist_file_path_list:
    read_plist(plist_path, path_dict)
with open(os.path.join(plist_dir_path, u'packed_path.json'), 'w') as writter:
    json.dump(path_dict, writter, indent=2)

