#!/usr/bin/python
# encoding: utf-8
# @Author: wcgn1122<wcgn1122@corp.netease.com>
# @Description:

#合图之后，删除所有打进图集的图片

import shutil
import os
import sys
import re
import argparse
import time
import subprocess as subp
import xml.dom.minidom as minidom
from xml.dom import Node

PROJECT_RES_PATH = './'
PROJECT_GUI_PATH = os.path.normpath(os.path.join(PROJECT_RES_PATH, 'gui'))
# 合图存放的目录
OUTPUT_PATH = os.path.normpath(os.path.join(PROJECT_GUI_PATH, 'packed_res'))
# 需要合图的目录
# 类似技能图标、装备图标这些，由于每次使用仅占极小部分，如果合图会导致内存浪费
packed_folder_list = [
	'battleui',
	'skill',
	'equipment',
	'hero_icon',
	'tips',
	'hero_icon_round',
]
def transImages(plat):
	# 保存所有的 png 与 plist 的映射
	png_to_plist_map = {}

	if not os.path.exists(OUTPUT_PATH):
		os.makedirs(OUTPUT_PATH)

	temp_root_path = os.path.normpath(os.path.join(PROJECT_RES_PATH, 'temp'))
	temp_root_path = temp_root_path.replace('\\', '/')
	temp_folder = 'temp/gui'
	temp_folder_path = os.path.normpath(os.path.join(PROJECT_RES_PATH, temp_folder))

	for folder_name in packed_folder_list:
		# 删除临时目录
		if os.path.exists(temp_root_path):
			shutil.rmtree(temp_root_path)

		# 当前资源目录
		source_folder_path = os.path.normpath(os.path.join(PROJECT_GUI_PATH, folder_name))
		dest_folder_path = os.path.normpath(os.path.join(temp_folder_path, folder_name))
		# 把当前资源目录 拷贝到特定文件夹中，使得 plist 中的 png 路径能够对应上 ccm 中的路径
		print ' --- temp_root_path: ', temp_root_path, '  source: ', source_folder_path, '   dest: ', dest_folder_path
		shutil.copytree(source_folder_path, dest_folder_path)

		print "压缩 start packer ", source_folder_path
		outFngName = os.path.join(OUTPUT_PATH, folder_name + ".png")
		# outFngName = os.path.join(OUTPUT_PATH, folder_name + ".png")
		outPlistName = os.path.join(OUTPUT_PATH, folder_name + ".plist")
		fixed_outPlistName = outPlistName[4:]
		fixed_outPlistName = fixed_outPlistName.replace('\\', '/')

		# 缓存当前目录中被合图的 png 的名字，方便从源目录删除
		cached_png_names = {}
		has_plist_in_folder = False

		for root, dirs, files in os.walk(temp_root_path, topdown=False):
			for name in files:
				name_path = root + '/' + name
				if not os.path.isfile(name_path):
					continue
				fixed_name_path = name_path.replace('\\', '/')
				if temp_root_path in fixed_name_path:
					fixed_name_path = fixed_name_path[len(temp_root_path) + 1:]

				png_to_plist_map[fixed_name_path] = fixed_outPlistName
				cached_png_names[name] = 1

				# 把当前资源目录中的 plist 以及对应的 png 删除掉，主要是按钮的合图
				if '.plist' in name:
					has_plist_in_folder = True
					file_name = name[0:-6]
					png_file_name = file_name + '.png'
					# print '========= delete: ', root + '//' + png_file_name
					os.remove(name_path)  # 删除 plist
					os.remove(root + '//' + png_file_name)  # 删除 PNG

					png_name_path = root + '/' + png_file_name
					fixed_png_file = png_name_path.replace('\\', '/')
					if temp_root_path in fixed_png_file:
						fixed_png_file = fixed_png_file[len(temp_root_path) + 1:]
					# print ' ............ fixedpng: ', fixed_png_file
					if fixed_png_file in png_to_plist_map:
						del png_to_plist_map[fixed_png_file]
						del cached_png_names[png_file_name]
					del png_to_plist_map[fixed_name_path]
					del cached_png_names[name]

		cmd_str = ''
		if platform == 'win':
			cmd_str += "TexturePacker "
		else:
			cmd_str += "/Applications/TexturePacker.app/Contents/MacOS/TexturePacker "
		cmd_str += "--texture-format png --sheet %s %s --data %s --max-width 2048 --max-height 2048 --dither-fs-alpha --opt RGBA4444 --disable-rotation --size-constraints POT --trim-mode None --padding 1" %(outFngName, temp_root_path, outPlistName)
		print cmd_str
		if os.system(cmd_str) == 0:
			dom_tree = minidom.parse(outPlistName)
			for node in dom_tree.getElementsByTagName('key'):
				if node.firstChild.nodeType == Node.TEXT_NODE:
					name = node.firstChild.data
					if name.endswith('.png'):
						file_name = os.path.split(name)[1]
						if file_name in cached_png_names:
							name_path = source_folder_path + '/' + file_name
							os.remove(name_path)

	# 删除临时目录
	if os.path.exists(temp_root_path):
		shutil.rmtree(temp_root_path)


	# 存储映射表，应用到程序中
	py_file_name = os.path.normpath(os.path.join(OUTPUT_PATH, 'path_to_plist_name.py'))
	with open(py_file_name, 'w') as file:
		file.write('path_to_plist_name=' + str(png_to_plist_map))

# sys.argv
print sys.argv
argu_count = len(sys.argv)
platform = 'win'
if argu_count > 1 and sys.argv[1] == 'ios':
	platform = 'ios'

# 转换图片资源
transImages(platform)