# -*- coding:utf-8 -*-
'''
查找废弃的json文件
'''


import os
import json


NotInclude = []

exclude_dir = ['lib', 'extensions', 'editor', 'cinematic', 'client_only','engine', 'reload_tool', 'sound', 'storyline', 'wrapper']
exclude_file = ['__init__.py', 'ScanChinese.py', 'DebugHelper.py', 'client_consts.py']
start_with = ['.', '..']

exist_json_file = []


template_path = ''


def read_exist_json_file(dir_path):
    global exist_json_file

    path_list = os.listdir(os.path.join(dir_path, 'res/gui/template/'))
    for name in path_list:
        if name.endswith('.json') and name not in NotInclude:
            exist_json_file.append(name[:-5])


def scan(dir_path):
    for dirctory, d_names, f_names in os.walk(dir_path):
        for f in f_names:
            if f in exclude_file:
                continue
            if f.startswith(start_with[0]) or f.startswith(start_with[1]):
                continue
            if not f.endswith('.py'):
                continue
            file_path = os.path.join(dirctory, f)
            filter_json(file_path)
        
        temp = d_names[::]
        while( len(d_names) > 0):
            d_names.pop()

        for d in temp:
            if d in exclude_dir:
                continue
            scan(os.path.join(dirctory, d)) 
        
def filter_json(file_path):
    with open(file_path, 'r') as reader:
       string = reader.read()
       copy_str = exist_json_file[::]
       for name in copy_str:
            if name not in exist_json_file:
               continue
            find = False
            if string.find('\'' + name + '\'') != -1:
                exist_json_file.remove(name)
                find = True

            if not find:
                if string.find('\"' + name + '\"') != -1:
                    exist_json_file.remove(name)
                    find = True

            if not find:
                if string.find('/' + name + '.json') != -1:
                    exist_json_file.remove(name)
                    find = True

            if find:
                find_template(name)

def find_template(name):
    ss = json.load(open(os.path.join(template_path, 'res/gui/template/%s.json' %name), 'r'))
    Traverse(ss)

def Traverse(map):
    for key, value in map.iteritems():
        if key =='template' or key == 'ccbFile':
            if value in exist_json_file:
                exist_json_file.remove(value)
                find_template(value)
        if key == 'child_list':
            for list_c in value:
                Traverse(list_c)

#扫描字符 取脚本所在的路径为初始路径
if __name__ == '__main__':
    path = os.path.realpath(__file__)
    dir_path, _ = os.path.split(path)
    global template_path
    template_path = dir_path
    scan_path = os.path.join(dir_path, 'script')
    print u'scan_path %s' % scan_path

    print u'********************分割线 开始扫描***************************'
    read_exist_json_file(dir_path)
    # test = 'C:/svndm75/code/client/dev/res/gui/template/panel_guanzhan_battle.json'
    # filter_json(test)
    #find_template('panel_guanzhan_battle')
    scan(scan_path)
    print u'********************分割线 扫描结束***************************'
    print '\n'.join(exist_json_file)
    print u'********************分割线 输出文件 deprecatedJson.txt***************************'
    
    
    with open( os.path.join(dir_path, u'废弃的json文件.txt') , 'w') as writter:
        writter.write('\n'.join(exist_json_file))


