# -*- coding:utf-8 -*-
'''
扫描中文
'''

import os

import re

exclude_dir = ['lib', 'data', 'extensions', 'editor', 'cinematic']
exclude_file = ['__init__.py', 'ScanChinese.py', 'action_manager.py', 'DebugHelper.py', 'SuperGmPanel.py', 'client_consts.py']
start_with = ['.', '..']
exclude_str =['logger.debug', 'logger.info', 'logger.warn', 'logger.error', 'logger.critical', 'print', 'USLogger']
output_list = []
output_set = set()

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
            read_line(file_path)
        
        temp = d_names[::]
        while( len(d_names) > 0):
            d_names.pop()

        for d in temp:
            if d in exclude_dir:
                continue
            scan(os.path.join(dirctory, d)) 
        

def read_line(file_path):
    with open(file_path, 'r') as f:
        number = 0
        mul_comment_symbols = ('\'\'\'', '\"\"\"')
        is_commentt_line = False
        for line in f:
            for comment in mul_comment_symbols:
                if line.find(comment) != -1:
                    if is_commentt_line:
                        is_commentt_line = False
                        continue
                    else:
                        is_commentt_line = True
                        break
            if is_commentt_line:
                continue

            symbol = line.find('#')
            if symbol != -1:
                line  = line[0:symbol]
            if not line:
                continue
            number += 1
            idx = 0
            while(True):
                left_element = '\''
                right_element = '\''
                left = line.find(left_element, idx) # 左引号
                if left == -1:
                    left_element = '\"'
                    right_element = '\"'
                    left = line.find(left_element, idx)
                    if left == -1:
                        break
                right = line.find(right_element, left+1) #右引号
                if right == -1:
                    break
                idx = right+1

                content = line[(left+1):right]
                if not content:
                    break
                if content.isalnum() or content.isdigit():
                    break
                
                find = False
                for string in exclude_str:
                    if string in line:
                        find = True
                        break
                if find:
                    break

                u_content = ''
                if isinstance(content, unicode):
                    u_content = content
                else:
                    u_content = content.decode('utf-8')
                match = re.match(ur'.*[\u4e00-\u9fa5]+', u_content)
                if match:
                    out_str =  '文件路径：%s, 匹配内容：%s, 行数：%s, 行文本: %s' %(file_path, content, number, line)
                    print out_str
                    output_list.append(out_str + '\n')
                    output_set.add(content + '\n')

#扫描字符 取脚本所在的路径为初始路径
if __name__ == '__main__':
    path = os.path.realpath(__file__)
    dir_path, _ = os.path.split(path)
    scan_path = os.path.join(dir_path, 'script')
    print 'scan_path %s' % scan_path

    print '********************分割线 开始扫描***************************'
    scan(scan_path)
    with open( os.path.join(dir_path, u'扫描中文文本内容.txt') , 'w') as writter:
        writter.writelines(output_list)

    with open( os.path.join(dir_path, u'提取中文内容.txt') , 'w') as writter:
        l = list(output_set)
        writter.writelines(l)
    print '********************分割线 扫描结束***************************'
    print '********************总共统计：%s*****************************' % len(output_set)