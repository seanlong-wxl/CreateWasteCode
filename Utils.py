import os
import random
import re
import time

from random_words import RandomWords

# 随机生成英文单词
_rw = RandomWords()

# 语言关键字表
_language_kayword_list = ['sbyte', 'byte', 'char', 'short', 'ushort', 'int', 'uint', 'long', 'ulong', 'float', 'double',
                          'bool', 'decimal', 'enum', 'struct', 'public', 'protected', 'Internal', 'private', 'abstract',
                          'async', 'const', 'extern', 'out', 'override', 'readonly', 'sealed', 'static', 'unsafe',
                          'virtual', 'volatile', 'if', 'else', 'switch', 'case', 'do', 'for', 'foreach', 'in', 'while',
                          'break', 'continue', 'default', 'goto', 'return', 'yield', 'throw', 'try', 'catch', 'finally',
                          'checked', 'unchecked', 'fixed', 'lock', 'yield', 'params', 'ref', 'namespace', 'using', 'as',
                          'await', 'is', 'new', 'where', 'class', 'T', 'sizeof', 'typeof', 'true', 'false', 'stackalloc',
                          'nameof', 'explicit', 'implicit', 'operator', 'base', 'this', 'null', 'default', 'add', 'remove',
                          'get', 'global', 'partial', 'set', 'value', 'string', 'type', 'event', 'interface', 'delegate',
                          'object', '']

def random_name(_frist_name):
    _name_len = random.randint(4, 7)
    _alphabet_upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                       'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    _alphabet_lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z']
    _name = random.choice(_alphabet_upper)
    for i in range(_name_len):
        _name += random.choice(_alphabet_lower)
    return _frist_name + _name


# 得到指定路径内的所有文件
# 返回信息包括：文件名+后缀，文件路径
def get_fileinfo_from_dir(_dir_path, _file_name_list , _file_path, _suffix):

    _fileList = os.listdir(_dir_path)
    for _unit_file in _fileList:
        _filePath = os.path.join(_dir_path, _unit_file)
        if os.path.isdir(_filePath):
            get_fileinfo_from_dir(_filePath, _file_name_list, _file_path, _suffix)
            continue

        _file_name, _file_suffix = os.path.splitext(_unit_file)
        if '' is _suffix or None is _suffix:
            _file_name_list.append(_unit_file)
            _file_path.append(_filePath)
        elif _file_suffix == _suffix:
            _file_name_list.append(_unit_file)
            _file_path.append(_filePath)


# 随机生成英文单词
def random_english_word(_filter=[]):

    _random_val = remove_symbol(_rw.random_word())
    while(_random_val == None or _random_val in _language_kayword_list or _random_val in _filter):
        _random_val = remove_symbol(_rw.random_word())
    return _random_val

# 去除符号
def remove_symbol(_val):
    reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
    return re.sub(reg, '', _val)


# 生成指定类内容
# _file_names = []
# _file_paths = []
# get_fileinfo_from_dir(os.getcwd() + '\\MixCode\\BattleModel\\fb', _file_names, _file_paths, '.cs')
#
# _func_total_body = ''
# _random_name_list = []
#
# for _name in _file_names:
#     if 'TR' not in _name: continue
#
#     _base_name = _name.split('.')[0]
#     _random_val = random.randint(1, 3)
#
#     _varable_name = random_english_word()
#     while(_varable_name in _random_name_list):
#         _varable_name = random_english_word()
#     _random_name_list.append(_varable_name)
#
#     _func_case_body = str.format('\t\t\tcase "{0}":\n', _base_name)
#
#     _func_body = ''
#     if _random_val == 1:
#         _str_1 = str.format('\t\t\t\t{0} {1} = ({2})LocalDataManager.getInstance().GetDataById(_param_val, typeof({3}));\n', _base_name, _varable_name, _base_name, _base_name)
#         _str_2 = str.format('\t\t\t\tif ({0} == null) return;\n', _varable_name)
#         _str_3 = str.format('\t\t\t\tDebuger.Log("Command_Switch - " + {0}.id);\n', _varable_name)
#         _str_4 = '\t\t\t\tbreak;\n'
#         _func_body = _str_1 + _str_2 + _str_3 + _str_4
#     else:
#         _str_1 = str.format('\t\t\t\tHashtable {0} = LocalDataManager.getInstance().GetDatas(typeof({1}));\n',_varable_name, _base_name)
#         _str_8 = str.format('\t\t\t\tif ({0} == null) return;\n', _varable_name)
#         _str_2 = str.format('\t\t\t\tforeach (DictionaryEntry t in {0}){1}\n', _varable_name, '{')
#         _random_tr_name = random_english_word()
#         while (_random_tr_name in _random_name_list):
#             _random_tr_name = random_english_word()
#         _random_name_list.append(_random_tr_name)
#         _str_3 = str.format('\t\t\t\t\t{0} {1} = {2}.Value as {3};\n', _base_name, _random_tr_name, 't', _base_name)
#         _str_4 = str.format('\t\t\t\t\tDebuger.Log("Command_Switch - " + {0}.id);\n',_random_tr_name)
#         _str_5 = str.format('\t\t\t\t\tbreak;\n')
#         _str_6 = '\t\t\t\t}\n'
#         _str_7 = '\t\t\t\tbreak;\n'
#         _func_body = _str_1 + _str_8 + _str_2 + _str_3 + _str_4 + _str_5 + _str_6 + _str_7
#
#     _func_case_body += _func_body
#     _func_total_body += _func_case_body
#
# print(_func_total_body)


