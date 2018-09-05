# -*- coding:utf-8 -*-

'''
查找gui图片在json文件中的引用
	参数：图片名称 以gui为根目录
	输出：文件名称 
			引用json文件

'''

import os
import json
import sys


exist_json_file = []


def read_exist_json_file(root_path):
    global exist_json_file
    exist_json_file = []
    for path, sub_path, files in os.walk(os.path.join(root_path, 'res/gui/template/')):
        for file_name in files:
            if file_name.endswith('.json'):
                exist_json_file.append(os.path.join(path, file_name))


def find_png_json(root_path, file_path):
    i = 0
    while( i < len(exist_json_file)):
        json_file = exist_json_file[i]
        with open(json_file, 'r') as reader:
            json_dict = json.load(reader)
            if parse_json(json_dict, file_path):
                i += 1
            else:
                exist_json_file.remove(json_file)

def parse_json(json_dict, file_path):
    for key, value in json_dict.iteritems():
        if key == 'child_list':
            for child in value:
                if parse_json(child, file_path):
                    return True
        else:
            if isinstance(value, dict):
                if parse_json(value, file_path):
                    return True
            else:
                if isinstance(value, (str,unicode)) and value.encode('utf-8').endswith('.png'):
                    if os.path.normpath(value) == file_path:
                        return True
    return False


#扫描字符 取脚本所在的路径为初始路径
if __name__ == '__main__':
    out_put_str = '请将文件放置在游戏根目录下面\n目前只支持查询png文件在gui/template/下面的引用，代码，配置中暂时不支持查询\n'
    path = os.path.realpath(__file__)			
    root_path, _ = os.path.split(path)
    if not sys.argv:
        out_put_str += '错误：请输入参数\n'
    else:
        for i in range(len(sys.argv)):
            if i == 0:
                continue
            png_file_path = sys.argv[i]
            dir_name, file_name = os.path.split(png_file_path)
            if not file_name.endswith('.png'):
                out_put_str += '错误：工具目前只支持查询png文件\n'
            else:
                out_put_str += '查找%s的引用:\n' %file_name
                file_path = os.path.join(dir_name[dir_name.find('gui'):], file_name)
                read_exist_json_file(root_path)
                find_png_json(root_path, file_path)
                if not exist_json_file:
                    out_put_str += '\t没有json文件引用%s\n' %file_name
                else:
                    for name in exist_json_file:
                        out_put_str += '\t%s被%s引用\n' %(file_name, os.path.basename(name))
    with open( os.path.join(root_path, u'图片引用的Json文件.txt') , 'w') as writter:
        writter.write(out_put_str)


