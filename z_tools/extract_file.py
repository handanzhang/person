# -*- coding:utf-8 -*-

'''
提取SkillTagAction内定义的Action函数，用装饰器的方法重新定义在不同的 Impl文件中
'''
import os
import re

from SkillTagAction import  SkillTagActionFactory, SkillTagActionType

only_client_type_set = SkillTagActionFactory.only_client_type_set
only_client_type_for_me_set = SkillTagActionFactory.only_client_type_for_me_set
only_server_type_set = SkillTagActionFactory.only_server_type_set
oonly_client_except_watcher_set = SkillTagActionFactory.only_client_except_watcher_set


out_file_content = '''
#-*- coding:utf-8 -*-

from public.helper import ConfHelper
from mobilelog.LogManager import LogManager
from public import consts
from public.consts import CreepSubType, UnitEventType, MoneyJumpType
import math3d
import math
from public.helper import CalculateHelper
from public.helper.behavior_tree import BTNode
from public.component.UnitEvent import UnitInAreaEvent, UnitBeWorldFilterEvent, UnitOperationEvent
from public.component.CollisionComp import SensorBoxType
import Globals
import CallBack
from public.units import UnitState
from public.movepattern.MovePatternFactory import MovePatternType
from public.units.Unit import UnitStateCache
from collections import defaultdict
import random
from public.helper import SnapshotHelper
from public.helper import MathHelper
from public.skill.SkillTagAction import SkillTagActionFactory, SkillTagActionType,SkillTagActionUseType, SkillTagAction


register_action_cls = SkillTagActionFactory.register_action_cls
ONLY_CLIENT_TYPE_SET = SkillTagActionUseType.ONLY_CLIENT_TYPE_FOR_ME
ONLY_CLIENT_TYPE_FOR_ME = SkillTagActionUseType.ONLY_CLIENT_TYPE_FOR_ME
ONLY_SERVER_TYPE_SET = SkillTagActionUseType.ONLY_SERVER_TYPE_SET
ONLY_CLIENT_EXCEPT_WATCHER_SET = SkillTagActionUseType.ONLY_CLIENT_EXCEPT_WATCHER_SET\n\n
'''

class_name_to_use_type = {}


id_to_param_name = {}

for key, value in SkillTagActionType.__dict__.iteritems():
	id_to_param_name[value] = key


def extract_content(start, end):


	parent_file_path = os.path.realpath(__file__)

	for action_type in range(start, end, 1):
		cls = SkillTagActionFactory.tag_action_cls_dict.get(action_type)
		use_type = []
		if cls:
			class_name_to_use_type[cls.__name__] = (use_type, action_type)
			if action_type in only_client_type_set:
				use_type.append('ONLY_CLIENT_TYPE_SET')

			if action_type in only_client_type_for_me_set:
				use_type.append('ONLY_CLIENT_TYPE_FOR_ME')

			if action_type in only_server_type_set:
				use_type.append('ONLY_SERVER_TYPE_SET')

			if action_type in oonly_client_except_watcher_set:
				use_type.append('ONLY_CLIENT_EXCEPT_WATCHER_SET')

	read_path = os.path.join(os.path.split(parent_file_path)[0], 'SkillTagAction.py')

	out_put_path = os.path.join(os.path.split(parent_file_path)[0], 'ActionImpl','SkillTagActionImpl_XX.py')

	with open( read_path, 'r') as reader:
		file_content = reader.read()
		name_start_end = []
		for name in class_name_to_use_type.iterkeys():
			extract_class(file_content, name, name_start_end)
		name_start_end.sort(cmp = lambda x, y: -1 if x[0] < y[0] else 1)
		combine_class(file_content, name_start_end)

	global out_file_content
	with open(out_put_path, 'w') as writer:
		writer.write(out_file_content)

def extract_class(file_content, name, name_start_end):
	re_str = r'\bclass.*' + name
	match = re.search(re_str, file_content, re.M)
	if match:
		name_start_end.append((match.start(), name))


def combine_class(file_content, name_start_end):
	global out_file_content
	i = 0
	while (i < len(name_start_end) - 1):
		action_type = class_name_to_use_type[name_start_end[i][1]][1]
		use_type_list = class_name_to_use_type[name_start_end[i][1]][0]
		decorator = '@register_action_cls(SkillTagActionType.' + id_to_param_name[action_type]
		if use_type_list:
			for use_type in use_type_list:

				decorator += ', '+ use_type
		decorator += ')\n'

		start = name_start_end[i][0]
		end = name_start_end[i + 1][0]
		sub_str = file_content[start:end]
		i += 1
		out_file_content += decorator + sub_str

	action_type = class_name_to_use_type[name_start_end[i][1]][1]
	use_type_list = class_name_to_use_type[name_start_end[i][1]][0]
	decorator = '@register_action_cls(SkillTagActionType.' + id_to_param_name[action_type]
	if use_type_list:
		for use_type in use_type_list:
			decorator += ', ' + use_type
	decorator += ')\n'

	start = name_start_end[i][0]
	sub_str = file_content[start:]
	i += 1
	out_file_content += decorator + sub_str



