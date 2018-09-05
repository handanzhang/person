# -*- coding:utf-8 -*-
'''
扫描wwis配置中缺失的文件
'''

import sys
import os


exist_wwis_conf_file = {}

out_put_str = ''

def read_exist_conf_file(dir_path):

    path_list = os.listdir(os.path.join(dir_path, 'res/wwise/'))
    for name in path_list:
        if name.endswith('.txt'):
            with open( os.path.join(dir_path, 'res/wwise', name), 'r') as reader:
                key = name[:-4]
                event_list = []
                is_continue = True
                exist_wwis_conf_file[key] = event_list
                for line in reader.readlines():
                    line = line.strip()
                    if line and line[0].isalpha():
                        if line.startswith('Event'):
                            is_continue = False
                            continue
                        else:
                            is_continue = True

                    if is_continue:
                        continue
                    
                    split_str = line.split('\t')
                    i = 0
                    for s in split_str:
                        if s:
                            if i == 1:
                                event_list.append(s)
                                break
                            i += 1 


def scan(dir_path):
    global exist_wwis_conf_file
    sys.path.append(os.path.join(dir_path, 'script\lib'))
    sys.path.append(os.path.join(dir_path, 'script'))
    vo_event = __import__('data.common.vo_event', fromlist=[''])
    
    for taggedict in vo_event.__dict__['data'].itervalues():
        for key, value in taggedict.iteritems():
            if key == 'event':
                parse_event(value, taggedict['key'])

def parse_event(event_str, key):
    global out_put_str 
    split_str = event_str.split('|')
    file_name = split_str[0][6:-10]
    event_name = split_str[1]
    if file_name not in exist_wwis_conf_file:
        out_put_str += 'key: ' + str(key) + '    file_name: ' + file_name + '    event_name: ' + event_name + '\r\n'
        return
        
    if event_name not in exist_wwis_conf_file[file_name]:
        out_put_str += 'key: ' + str(key) + '    file_name: ' + file_name + '    event_name: ' + event_name + '\r\n'
        return

    
#扫描字符 取脚本所在的路径为初始路径
if __name__ == '__main__':
    path = os.path.realpath(__file__)
    dir_path, _ = os.path.split(path)
    print '********************分割线 开始扫描***************************'
    read_exist_conf_file(dir_path)
    scan(dir_path)
    print '********************分割线 扫描结束***************************'
    print '********************分割线 输出文件 deprecatedJson.txt***************************'
    
    
    with open( os.path.join(dir_path, u'wwise扫描结果.txt') , 'w') as writter:
        writter.write(out_put_str)
