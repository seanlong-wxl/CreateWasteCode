
# author：wxl @ 2020-11-5
# info:替换类中出现的 _tn、_mn、_Tn、_Mn(n指1-9)
# 思路整理：
# 1、查找所有的类；
# 2、按内容查找需要替换的关键字
# 3、得到替换的内容
# 4、得到新的内容 _trn、_mrn、_Trn、_Mrn(n指1-9) r指a-z的随机
# 5、键值对的形式保存
# 6、对文件内容进行替换
# 7、替换完成后保存文件
# ****** 查找、替换 需要对内存进行操作，不要对文件操作，不然会很慢

import os
import random
import time
import Utils

class RenameFuncOrVariateName():

    # 原名称 ： 新名称
    _need_rename_dict = {}
    # 类名，类内容
    _cache_file_content = {}
    # 随机池
    _alphabet_lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z']
    #  替换日志
    _save_logs = []

    def get_need_rename_func(self):
        _file_names = []
        _file_paths = []
        Utils.get_fileinfo_from_dir(os.getcwd() + '\\CppFile', _file_names, _file_paths, '.cpp')

        _time_begin = time.time()
        for _path in _file_paths:
            _local_time_begin = time.time()
            self.read_content(_path)
            _local_end_time = time.time()
            print('find runtime: ' + str(round(_local_end_time - _local_time_begin, 5)) + '  file:' + _path)
        _end_time = time.time()
        print('--------->1、 查找重命名方法完成,所用时间: ' + str(_end_time - _time_begin) + '需要重命名的数量：' + str(len(self._need_rename_dict)) + '\n')

        _time_begin = time.time()
        self.replace_find_str()
        _end_time = time.time()
        print('--------->2、 得到新旧名字对应关系完成，所用时间：' + str(_end_time - _time_begin) + '\n')

        _time_begin = time.time()
        self.replace_content()
        _end_time = time.time()
        print('--------->3、 替换完成，所用时间：' + str(_end_time - _time_begin) + '\n')

        _time_begin = time.time()
        self.save_file()
        _end_time = time.time()
        print('--------->4、 保存文件完成，所用时间：' + str(_end_time - _time_begin) + '\n')

    # 读取文件内容
    def read_content(self, _path):
        with(open(_path, 'r', encoding='utf-8')) as rf:
            _line_content = rf.read()
            self._cache_file_content[_path] = _line_content

    # 原名字：新名字得到对应关系
    def replace_find_str(self):
        for i in range(1, 10):
            _key_t = '_t' + str(i)
            self._need_rename_dict[_key_t] = self.random_name('_t') + str(i)

            _key_m = '_m' + str(i)
            self._need_rename_dict[_key_m] = self.random_name('_m') + str(i)

            _key_T = '_T' + str(i)
            self._need_rename_dict[_key_T] = self.random_name('_T') + str(i)

            _key_M = '_M' + str(i)
            self._need_rename_dict[_key_M] = self.random_name('_M') + str(i)

    # 随机第二位的名字
    def random_name(self, _first_str):
        _random_val = _first_str
        _random_val += random.choice(self._alphabet_lower)
        return _random_val

    # 替换文本内容
    def replace_content(self):
        for _key in self._need_rename_dict.keys():
            _local_time_begin = time.time()
            for _path in self._cache_file_content.keys():
                self._cache_file_content[_path] = self._cache_file_content[_path].replace(_key, self._need_rename_dict[_key])
            _local_end_time = time.time()
            print('get random name runtime: ' + str(round(_local_end_time - _local_time_begin, 5)) + '  file:' + _path)

    # 保存文件
    def save_file(self):
        for _path in self._cache_file_content:
            print('save file: ' + _path)
            with(open(_path, 'w+', encoding='utf-8')) as wf:
                wf.write(self._cache_file_content[_path])
                wf.close()
#
app = RenameFuncOrVariateName()
app.get_need_rename_func()
