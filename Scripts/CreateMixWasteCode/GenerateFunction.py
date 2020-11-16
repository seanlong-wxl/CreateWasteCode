# author: wxl @ 2020-11-12
# info: 1、创建函数，包含：方法名、参数列表、函数体
# 作用：构建无循环调用的函数体

import Utils
import random

# 变量定义重复过滤
_filter_repetition = []
# 单运算符
_operation_solo_define = ['+', '-', '*']
# 两元运算符
_operation_dual_define = ['+=', '-=', '*=', '=']
# 分隔符
_separator = ['.', '-', '_', '+', '|', '#', '@', ',', '*']
# 类型定义
_types_define = ['int', 'float', 'string', 'List<string>', 'List<int>', 'bool', 'void']


# 生成函数内容
# 参数说明：
# 1、_name_num：参数列表个数
# 2、_code_chunk_num：代码块的数量(参数的个数)
# 返回值说明：
# _func_body_content：方法体
# _func_name_base：方法名
# _param_list：参数列表：[{类型：参数名},....]
# _return_type：返回值类型
def generate_function(_name_num, _code_chunk_num):
    _return_type = get_type([])
    _func_name_base = get_func_name(_name_num)
    _param_str, _param_list = get_func_parameter_list(_code_chunk_num)
    _func_body = get_func_body(_return_type, _param_list)

    _func_name = '\n\tpublic static ' + _return_type + ' ' + _func_name_base + '(' + _param_str + ')'
    _func_body_content = _func_name + '\n\t{\n' + _func_body + '\t}\n'
    return _func_body_content, _func_name_base, _param_list, _return_type


# 得到类型
# _ignore_types:排除列表
def get_type(_ignore_types):
    _type = random.choice(_types_define)
    while _type in _ignore_types:
        _type = random.choice(_types_define)
    return _type


# 随机变量名
# 添加到列表中，进行去重过滤
def get_random_variable_name():
    _param_name = Utils.random_english_word(_filter_repetition)
    _filter_repetition.append(_param_name)
    return _param_name


# 得到函数名
# _name_num：函数名的单词个数
# 返回值说明：函数名
def get_func_name(_name_num):
    _func_name = ''
    for i in range(_name_num):
        _word = Utils.random_english_word()
        _func_name += _word.title()
    return _func_name


# 得到参数列表
# _param_num: 参数个数
# 返回值说明：
# 1、_param_str 构建好的参数列表描述
# 2、_param_list [{类型: 变量名},...]
def get_func_parameter_list(_param_num):
    _param_list = []
    _param_str = ''
    for i in range(_param_num):
        _param_type = get_type(['void'])
        _param_name = get_random_variable_name()

        _param_content = {_param_type: '_' + _param_name}
        if i + 1 != _param_num:
            _param_str += _param_type + ' _' + _param_name + ', '
        else:
            _param_str += _param_type + ' _' + _param_name
        _param_list.append(_param_content)
    return _param_str, _param_list


# region 得到函数体
# 得到函数体以及返回值
# _return_type: 返回值类型 _param_list：参数列表
def get_func_body(_return_type, _param_list):

    _code_chunk = ''
    _func_body = ''
    _return_list_str_val = ''
    _return_list_int_val = ''
    _return_int_val = ''

    # 函数体
    if len(_param_list) > 0:
        for _param_dict in _param_list:
            for _param_type in _param_dict.keys():
                _code_chunk = ''
                if 'List<int>' in _param_type:
                    _code_chunk = get_func_body_for_list_int(_param_dict[_param_type]) + '\n'
                elif 'List<string>' in _param_type:
                    _str_func_random = random.randint(0, 2)
                    if _str_func_random == 1:
                        _code_chunk, _return_list_int_val = get_func_body_for_list_string_1(_param_dict[_param_type])
                    else:
                        _code_chunk, _return_list_str_val = get_func_body_for_list_string_2(_param_dict[_param_type])
                elif 'bool' not in _param_type:
                    _code_chunk, _return_int_val = get_func_body_for_int(_param_dict[_param_type])
                _func_body += _code_chunk + '\n'
    else:
        _str_func_body, _return_int_val = get_func_body_for_int(None)
        _func_body += _str_func_body + '\n'

    # 返回值
    if _return_type == 'void':
        return _func_body
    elif _return_type == 'int':
        _func_body += get_return_int_value(_return_int_val, _return_list_int_val)
    elif _return_type == 'float':
        _func_body += get_return_float_value(_return_int_val, _return_list_int_val)
    elif _return_type == 'string':
        _func_body += get_return_string_value(_return_int_val, _return_list_int_val, _return_list_str_val)
    elif _return_type == 'bool':
        _func_body += get_return_bool_value()
    elif _return_type == 'List<string>':
        _func_body += get_return_list_string_value(_return_int_val, _return_list_int_val, _return_list_str_val)
    elif _return_type == 'List<int>':
        _func_body += get_return_list_int_value(_return_int_val, _return_list_int_val)
    return _func_body


# 得到list<int>对应的函数体
# _list_int_param_name: 参数List<int>类型的变量名
def get_func_body_for_list_int(_list_int_param_name):
    _variable_name = get_random_variable_name()
    _str_0 = str.format('\t\t\tif ({0} != null) {1}\n', _list_int_param_name, '{')
    _str_1 = str.format('\t\t\t\tint {0} = 0;\n', _variable_name)
    _str_2 = str.format('\t\t\t\tfor (int i = 0; i < {0}.Count; i++) {1}\n', _list_int_param_name, '{')
    _str_3 = str.format('\t\t\t\t\t{0} {1} {2}[i];\n', _variable_name, random.choice(_operation_dual_define), _list_int_param_name)
    _str_4 = '\t\t\t\t}\n'
    _str_5 = '\t\t\t}\n'
    _str = _str_0 + _str_1 + _str_2 + _str_3 + _str_4 + _str_5
    return _str


# 得到list<string> 对应的函数体
# _list_int_param_name: 参数List<string>类型的变量名
def get_func_body_for_list_string_1(_list_string_param_name):
    _variable_name = get_random_variable_name()
    _variable_name_1 = get_random_variable_name()
    _str_0 = str.format('\t\t\tint {0}=0;\n', _variable_name)
    _str_1 = str.format('\t\t\tif ({0} != null) {1}\n', _list_string_param_name, '{')
    _str_2 = str.format('\t\t\t\tfor (int i = 0; i < {0}.Count; i++) {1}\n', _list_string_param_name, '{')
    _str_3 = str.format('\t\t\t\t\tint {0} = 0;\n', _variable_name_1)
    _str_4 = str.format('\t\t\t\t\tif (int.TryParse({0}[i], out {1})){2}\n', _list_string_param_name, _variable_name_1, '{')
    _str_5 = str.format('\t\t\t\t\t\t{0} {1} {2};\n', _variable_name, random.choice(_operation_dual_define), _variable_name_1)
    _str_6 = str.format('\t\t\t\t\t{0}\n', '}')
    _str_7 = str.format('\t\t\t\t\telse{0}\n', '{')
    _str_8 = str.format('\t\t\t\t\t\t{0} = 0;\n', _variable_name)
    _str_9 = str.format('\t\t\t\t\t{0}\n', '}')
    _str_10 = str.format('\t\t\t\t{0}\n', '}')
    _str_11 = str.format('\t\t\t{0}\n', '}')
    _str = _str_0 + _str_1 + _str_2 + _str_3 + _str_4 + _str_5 + _str_6 + _str_7 + _str_8 + _str_9 + _str_10 + _str_11
    return _str, _variable_name


# 得到list<string> 对应的函数体2
# _list_int_param_name: 参数List<string>类型的变量名
def get_func_body_for_list_string_2(_list_string_param_name):
    _variable_name = get_random_variable_name()
    _variable_name_2 = get_random_variable_name()
    _str_0 = str.format('\t\t\tstring {0} = "";\n', _variable_name)
    _str_1 = str.format('\t\t\tif ({0} != null) {1}\n', _list_string_param_name, '{')
    _str_2 = str.format('\t\t\t\tfor (int i = 0; i < {0}.Count; i++) {1}\n', _list_string_param_name, '{')
    _str_3 = str.format("\t\t\t\t\tstring[] {0} = {1}[i].Split('{2}');\n", _variable_name_2, _list_string_param_name, random.choice(_separator))
    _str_4 = str.format('\t\t\t\t\tfor (int m = 0; m < {0}.Length; m++) {1}\n', _variable_name_2, '{')
    _str_5 = str.format('\t\t\t\t\t\t{0} += {1}[m];\n', _variable_name, _variable_name_2)
    _str_6 = str.format('\t\t\t\t\t\tDebuger.Log({0});;\n', _variable_name)
    _str_8 = str.format('\t\t\t\t\t{0}\n', '}')
    _str_9 = str.format('\t\t\t\t{0}\n', '}')
    _str_10 = str.format('\t\t\t{0}\n', '}')
    _str = _str_0 + _str_1 + _str_2 + _str_3 + _str_4 + _str_5 + _str_6 + _str_8 + _str_9 + _str_10
    return _str, _variable_name


# 得到int对应的函数体
# _param_name: 参数int类型的变量名
def get_func_body_for_int(_param_name):

    _str_2_1 = ''
    if _param_name is None:
        _param_name = get_random_variable_name()
        _str_2_1 = str.format('\t\t\tstring {0} = "";\n', _param_name)

    _variable_name = get_random_variable_name()
    _variable_name_1 = get_random_variable_name()

    _str_1 = str.format('\t\t\tint {0}=0;\n', _variable_name)
    _str_2 = str.format('\t\t\tint {0} = 0;\n', _variable_name_1)
    _str_3 = str.format('\t\t\tif (!int.TryParse({0}.ToString(), out {1})){2}\n', _param_name, _variable_name_1, '{')
    _str_4 = '\t\t\t\tDebuger.Log("goto int err!");\n'
    _str_5 = '\t\t\t}\n'
    _str_6 = '\t\t\telse {\n'

    _str_7 = ''
    _for_count = random.randint(1, 10)
    _for_variable_list = []
    for i in range(_for_count):
        _for_variable_name = get_random_variable_name()
        _for_variable_value = random.randint(1, 100000)
        _str_7 += str.format('\t\t\t\tint {0} = {1};\n', _for_variable_name, _for_variable_value)
        _for_variable_list.append(_for_variable_name)

    _str_8 = str.format('\t\t\t\t{0} = {1} {2} ', _variable_name, _variable_name_1, random.choice(_operation_solo_define))
    for _index in range(len(_for_variable_list)):
        if _index + 1 != len(_for_variable_list):
            _str_8 += str.format('{0} {1} ', _for_variable_list[_index], random.choice(_operation_solo_define))
        else:
            _str_8 += str.format('{0};', _for_variable_list[_index])

    _str_9 = '\n\t\t\t}\n'
    _str = _str_1 + _str_2 + _str_2_1 + _str_3 + _str_4 + _str_5 + _str_6 + _str_7 + _str_8 + _str_9
    return _str, _variable_name
# endregion


# region 得到函数返回值
# 得到float类型的返回值
def get_return_float_value(_val_1, _val_2):
    _value = ''
    if random.randint(0, 2) == 0 and _val_1 != '':
        _value = str.format('\t\t\treturn {0}*0.1f;\n', _val_1)
    elif _val_2 != '':
        _value = str.format('\t\t\treturn {0}*0.1f;\n', _val_2)
    else:
        _value += str.format('\t\t\treturn {0}*0.1f;\n', random.randint(1, 100000))
    return _value


# 得到int类型的返回值
def get_return_int_value(_val_1, _val_2):
    _value = ''
    if random.randint(0, 2) == 0 and _val_1 != '':
        _value += str.format('\t\t\treturn {0};\n', _val_1)
    elif _val_2 != '':
        _value += str.format('\t\t\treturn {0};\n', _val_2)
    else:
        _value += str.format('\t\t\treturn {0};\n', random.randint(1, 1000000))
    return _value


# 得到List<int> 类型的返回值
def get_return_list_int_value(_val_1, _val_2):
    _value = ''
    if random.randint(0, 2) == 0 and _val_1 != '':
        _value = str.format('\t\t\treturn new List<int>() {0} {1} {2};\n', '{', _val_1, '}')
    elif _val_2 != '':
        _value = str.format('\t\t\treturn new List<int>() {0} {1} {2};\n', '{', _val_2, '}')
    else:
        _value = '\t\t\treturn new List<int>() {};\n'
    return _value


# 得到List<string>类型的返回值
def get_return_list_string_value(_val_1, _val_2, _val_3):
    _random_val = random.randint(0, 3)
    _value = ''
    if _random_val == 0 and _val_1 != '':
        _value += str.format('\t\t\treturn new List<string>() {0} {1}.ToString() {2};\n', '{', _val_1, '}')
    elif _random_val == 1 and _val_2 != '':
        _value += str.format('\t\t\treturn new List<string>() {0} {1}.ToString() {2};\n', '{', _val_2, '}')
    elif _val_3 != '':
        _value += str.format('\t\t\treturn new List<string>() {0} {1}.ToString() {2};\n', '{', _val_3, '}')
    else:
        _value += '\t\t\treturn new List<string>() {};\n'
    return _value


# 得到bool类型的返回值
def get_return_bool_value():
    if random.randint(0, 3) == 1:
        _vale = '\t\t\treturn false;\n'
        return _vale
    else:
        _vale = '\t\t\treturn true;\n'
        return _vale


# 得到string类型的返回值
def get_return_string_value(_val_1, _val_2, _val_3):
    _random_val = random.randint(0, 3)
    _value = ''
    if _random_val == 0 and _val_1 !=  '':
        _value += str.format('\t\t\treturn {0}.ToString();\n', _val_1)
    elif _random_val == 1 and _val_2 != '':
        _value += str.format('\t\t\treturn {0}.ToString();\n', _val_2)
    elif _val_3 != '':
        _value += str.format('\t\t\treturn {0}.ToString();\n', _val_3)
    else:
        _value += str.format('\t\t\treturn "";\n', )
    return _value
# endregion

