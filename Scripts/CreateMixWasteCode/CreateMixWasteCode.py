# author: wxl @ 2020-11-12
# info: 1、创建垃圾混淆代码总入口

import os
import random
import time

from Scripts.CreateMixWasteCode.GenerateClass import GenerateClass


class CreateMixWasteCode( ):

    _generate_class = None

    def start(self):
        self._generate_class = GenerateClass()
        _user_input = self.get_user_input()
        while(_user_input != '6'):
            if _user_input == '1':
                _s_time = time.time()
                _save_path = self.get_user_save_path()
                self._generate_class.create_class(50, 0, False, self._generate_class.loop_call_no_param_struct)
                self._generate_class.save_class(os.path.join(_save_path, 'NoParamClass'))
                self._generate_class.create_class(50, 1, False, self._generate_class.loop_call_one_param_struct)
                self._generate_class.save_class(os.path.join(_save_path, 'OneParamClass'))
                _e_time = time.time()
                print('\n1 - create base class finish,run time: ' + str(round(_e_time - _s_time, 5)) + ' save path: ' + _save_path +  '\n')
            elif _user_input == '2':
                self.run_create_class(_dir_name='PureMixCode')
            elif _user_input == '3' or _user_input == '4' or _user_input == '5':
                if len(self._generate_class._no_param_func_return_vlue_dict) <= 0 or \
                        len(self._generate_class._one_param_func_return_vlue_dict) <= 0 or \
                        len(self._generate_class._one_param_func_param_vlue_dict) <= 0:
                    print('error! error info:循环调用基础类为空，请先执行‘1’，生成循环调用基础类！！')
                else:
                    _s_time = time.time()
                    if _user_input == '3':
                        self.run_create_class(_call_other=True, _dir_name='MixCodeRecuresiveCall')
                    elif _user_input == '4':
                        self.run_create_class(self._generate_class.create_lua_export_code, self._generate_class.save_lua_export_code, True, 'ToLuaExportCall')
                    elif _user_input == '5':
                        self.run_create_class(self._generate_class.create_custom_settings_code, self._generate_class.save_custom_settings_code, True, 'CustomSetting')
            _user_input = self.get_user_input()

    # 执行创建类
    def run_create_class(self, _call_back=None, _finish_call_back=None, _call_other=False, _dir_name=''):
        _create_class_num = input('请输入生成垃圾类的数量：')
        while _create_class_num.isdigit() is False:
            _create_class_num = input('请输入生成垃圾类的数量：')
        _save_path = self.get_user_save_path()
        _s_time = time.time()
        self._generate_class.create_class(int(_create_class_num), random.randint(1, 4), _call_other, _call_back)
        _e_time = time.time()
        print('\n1 - create waste class finish,run time: ' + str(round(_e_time - _s_time, 5)) + '\n')

        _s_time = time.time()
        _save_path = os.path.join(_save_path, _dir_name)
        self._generate_class.save_class(_save_path)
        if _finish_call_back != None:
            _finish_call_back(_save_path)
        _e_time = time.time()
        print('\n2 - save waste class finish,run time: ' + str(round(_e_time - _s_time, 5)) + 'save path: ' + _save_path + '\n')

    # 用户操作
    def get_user_input(self):
        _operation_explain = '\n请选择要执行的操作：\n' \
                             '1、构建循环调用的基础类\n' \
                             '2、构建垃圾代码，无循环调用\n' \
                             '3、构建垃圾代码，并有循环调用的\n' \
                             '4、构建在Wrap类中调用的代码，并有循环调用\n' \
                             '5、构建导出Wrap类的垃圾代码，并有循环调用\n' \
                             '6、退出\n'\
                             '** 要生成有循环调用的垃圾代码，则必须先执行第一步！\n' \
                             '执行操作：'
        _user_input = input(_operation_explain)
        return _user_input

    # 得到生成文件的保存路径
    def get_user_save_path(self):
        _save_path = input('请输入基础类的保存路径，在该路径内会添加文件夹：NoParamClass、OneParamClass、MixCodeRecuresiveCall、ToLuaExportCall、CustomSetting\n'
                           '保存路径：')
        while os.path.isdir(_save_path) == False:
            _save_path = input('请输入基础类的保存路径，在该路径内会添加文件夹：NoParamClass、OneParamClass、MixCodeRecuresiveCall、ToLuaExportCall、CustomSetting\n'
                '保存路径：')
        return _save_path


app = CreateMixWasteCode()
app.start( )
