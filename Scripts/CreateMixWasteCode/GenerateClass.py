# author: wxl @ 2020-11-12
# info:
# 1、创建类、保存类
# 2、生成ToLuaExport类中BeginTry方法添加的代码
# 3、生成CustomSettings类中customDelegateList方法中添加的代码

import os
import random
import shutil
import time


# 创建类
# 参数说明
# _class_num：创建类的数量
import Utils
from Scripts.CreateMixWasteCode import GenerateFunction, GenerateFunctionCallOther


class GenerateClass():
    # 类内容 {类名:类内容}
    _generate_class_content = {}
    # {返回值类型: [类名.方法名()]}
    _no_param_func_return_vlue_dict = {}
    # {返回值类型: [类名.方法名()]}
    _one_param_func_return_vlue_dict = {}
    # {类名.方法名():参数类型}
    _one_param_func_param_vlue_dict = {}
    # 生成CustomSettings类中的GT绑定
    _custom_setting_code = []
    # 生成用于插入wrap逻辑的垃圾代码
    _lua_export_code = []

    # 构建类
    # 参数说明：
    # 1、_class_num：创建类的数量
    # 2：_func_param_num：参数列表的数量(决定函数体的长度)
    # 3：_call_other：是否有其他循环调用
    # 4：_create_func_finish_call_back：类创建完成后的回调方法
    def create_class(self, _class_num, _func_param_num, _call_other, _create_func_finish_call_back=None):
        self._generate_class_content.clear()
        self.create_wrap_call_class()
        for _num in range(_class_num):
            _local_time_begin = time.time()
            _random_class_name_count = random.randint(3, 5)
            _class_name = ''
            for i in range(_random_class_name_count):
                _class_name += Utils.random_english_word().title()
            _class_title = str.format('public class {0}{1}', _class_name, '{\n\n')

            _random_func_count = random.randint(5, 15)
            _func_body_content = ''

            for i in range(_random_func_count):

                if not _call_other:
                    GenerateFunction._filter_repetition = []
                    _code_chunk, _func_name, _param_list, _return_type = GenerateFunction.generate_function(random.randint(2, 5), _func_param_num)
                else:
                    GenerateFunctionCallOther._filter_repetition = []
                    _code_chunk, _func_name, _param_list, _return_type = GenerateFunctionCallOther.generate_function(random.randint(2, 5), _func_param_num, self)
                _func_body_content += _code_chunk
                if _create_func_finish_call_back != None:
                    _create_func_finish_call_back(_class_name, _return_type, _func_name, _param_list)

            _class_content = 'using System.Collections.Generic; \n\n'
            _class_content += _class_title + _func_body_content + '}'
            self._generate_class_content[_class_name] = _class_content
            _local_end_time = time.time()
            print('create class runt time: ' + str(round(_local_end_time - _local_time_begin, 5)) + '  index: ' + str(_num + 1) + ' func num: ' + str(_random_func_count) + '  class name: ' + _class_name)

    # 清除数据
    def clear_data(self):
        self._generate_class_content.clear()
        self._no_param_func_return_vlue_dict.clear()
        self._one_param_func_param_vlue_dict.clear()
        self._one_param_func_return_vlue_dict.clear()
        self._custom_setting_code.clear()
        self._lua_export_code.clear()

    # 保存类内容
    def save_class(self, _save_dir):
        if os.path.exists(_save_dir):
            shutil.rmtree(_save_dir)
        if not os.path.exists(_save_dir):
            os.mkdir(_save_dir)

        for _class_name in self._generate_class_content.keys():
            with(open(os.path.join(_save_dir, _class_name + '.cs'), 'w+')) as wf:
                wf.write(self._generate_class_content[_class_name])
                wf.close()

    # region 创建方法完成后的回调，保存结构用来后期其他函数调用
    # 保存无参被调用函数结构
    # 保存结构：{返回值类型：[类名.方法名()]}
    def loop_call_no_param_struct(self, _class_name, _return_type, _func_base_name, _param_list):
        if _return_type not in self._no_param_func_return_vlue_dict.keys():
            self._no_param_func_return_vlue_dict[_return_type] = [str.format('{0}.{1}', _class_name, _func_base_name)]
        else:
            self._no_param_func_return_vlue_dict[_return_type].append(str.format('{0}.{1}', _class_name, _func_base_name))

    # 保存无参被调用函数结构
    # 保存结构：
    # 1、{返回值类型：[类名.方法名()]}
    # 2、{参数类型:[类名.方法名()]}
    def loop_call_one_param_struct(self, _class_name, _return_type, _func_base_name, _param_list):
        if _return_type not in self._one_param_func_return_vlue_dict.keys():
            self._one_param_func_return_vlue_dict[_return_type] = [str.format('{0}.{1}', _class_name, _func_base_name)]
        else:
            self._one_param_func_return_vlue_dict[_return_type].append(str.format('{0}.{1}', _class_name, _func_base_name))

        for _index in range(len(_param_list)):
            for _type in _param_list[_index]:
                _call_info = str.format('{0}.{1}', _class_name, _func_base_name)
                if _call_info not in self._one_param_func_param_vlue_dict.keys():
                    self._one_param_func_param_vlue_dict[_call_info] = _type
                else:
                    self._one_param_func_param_vlue_dict[_call_info].append(_type)
    # endregion

    # region 生成CS处理生成wrap相关的代码
    # 生成CustomSettings 绑定关系
    # 作用：C#脚本导出供lua使用，避免无用代码被裁剪
    def create_custom_settings_code(self, _class_name, _return_type, _func_base_name, _param_list):
        self._custom_setting_code.append(str.format('\t\t_GT(typeof({0})),\n', _class_name))

    # 保存GT文件
    def save_custom_settings_code(self, _save_path):
        _code = ''.join(self._custom_setting_code)
        with(open(os.path.join(_save_path, '_gt.cs'), 'w+')) as wf:
            wf.write(_code)
            wf.close()

    # 生成方法绑定
    # 作用：
    # 1、在lua生成的wrap文件中进行调用
    # 2、wrap调用的添加方法：在ToLuaExport类的BeginTry()方法中添加相关代码
    def create_lua_export_code(self, _class_name, _return_type, _func_base_name, _param_list):
        self._lua_export_code.append(str.format('\t\tmethods.Add("{0}.{1}()");\n', _class_name, _func_base_name))

    # 生成方法绑定
    # 作用：
    # 1、在lua生成的wrap文件中进行调用
    # 2、wrap调用的添加方法：在ToLuaExport类的BeginTry()方法中添加相关代码
    def save_lua_export_code(self, _save_path):
        self._lua_export_code.append('\t}\n')
        self._lua_export_code.append('}\n')
        _code = ''.join(self._lua_export_code)
        with(open(os.path.join(_save_path, '_gt_method.cs'), 'w+')) as wf:
            wf.write(_code)
            wf.close()

    # 构建被wrap类调用的类
    def create_wrap_call_class(self):
        self._lua_export_code.clear()
        self._lua_export_code.append(
            '/*\n'
            '将以下内容添加到脚本ToLuaExport的BeginTry()方法中，添加内容为：\n'
            '#region 混淆代码添加\n'
            'sb.AppendLineEx("\\t\\t\\tif(LuaConst.wrapType==1)");\n'
            'sb.AppendLineEx("\\t\\t\\t{");\n'
            'sb.AppendLineEx("\\t\\t\\t\\t" + RegisterMethods.GetMethods() + "();");\n'
            'sb.AppendLineEx("\\t\\t\\t}");\n'
            '#endregion\n'
            '*/\n')

        self._lua_export_code.append('using UnityEngine;\nusing System.Collections.Generic;\n\n')
        self._lua_export_code.append('public class RegisterMethods\n')
        self._lua_export_code.append('{')
        self._lua_export_code.append('\tstatic bool inited = false;\n')
        self._lua_export_code.append('\tprivate static List<string> methods = new List<string>();\n')
        self._lua_export_code.append('\tpublic static string GetMethods()\n')
        self._lua_export_code.append('\t{\n')
        self._lua_export_code.append('\t\tInit();\n')
        self._lua_export_code.append('\t\tint index =  Random.Range(0, methods.Count);\n')
        self._lua_export_code.append('\t\tif (index > methods.Count)\n')
        self._lua_export_code.append('\t\t\treturn methods[0];\n')
        self._lua_export_code.append('\t\treturn methods[index];\n')
        self._lua_export_code.append('\t}\n\n')

        self._lua_export_code.append('\tpublic static void Init()\n')
        self._lua_export_code.append('\t{\n')
        self._lua_export_code.append('\t\tif (inited) return;\n')
        self._lua_export_code.append('\t\tinited = true;\n')

    # endregion

    # region 得到循环调用函数
    # 得到可以被调用的无参数函数
    # 参数说明：
    # _return_type:需要的返回值
    def get_no_param_func(self, _return_type):
        if _return_type in self._no_param_func_return_vlue_dict:
            _func = self._no_param_func_return_vlue_dict[_return_type]
            _func_method = random.choice(_func)
            return str.format('{0}()', _func_method)
        else:
            if _return_type == 'int':
                return random.randint(1, 100000)
            elif _return_type == 'float':
                return str.format('{0}*0.1f', str(random.randint(1, 100000)))
            elif _return_type == 'string':
                return str.format('"{0}"', Utils.random_english_word([]))
            else:
                return None

    # 得到可以被调用的一个参数函数
    # 参数说明：
    # _return_type:需要的返回值
    def get_one_param_func(self, _return_type):
        if _return_type in self._one_param_func_return_vlue_dict:
            # 得到有当前返回值的可调用函数
            _func = self._one_param_func_return_vlue_dict[_return_type]
            _func_method = random.choice(_func)

            # 根据函数得到所需要的参数列表
            if _func_method in self._one_param_func_param_vlue_dict:
                _params = self._one_param_func_param_vlue_dict[_func_method]
                _param_func = self.get_no_param_func(_params)
                return str.format('{0}({1})', _func_method, _param_func)

        if _return_type == 'int':
            return random.randint(1, 100000)
        elif _return_type == 'float':
            return str.format('{0}*0.1f', str(random.randint(1, 100000)))
        elif _return_type == 'string':
            return str.format('"{0}"', Utils.random_english_word([]))
        else:
            return None
    # endregion

