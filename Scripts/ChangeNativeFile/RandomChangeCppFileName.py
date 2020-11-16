
# author: wxl @ 2020-11-5
# info: 对给定的文件进行重新命名
#       1、对给定名称最后一个‘_’之前的内容进行重命名
#       2、需要给出需要改名的文件名称，以及固定更换的命名

import os
import random
import Utils


class RandomChangeCppFileName():


    def start(self):
        _file_names = []
        _file_paths = []
        Utils.get_fileinfo_from_dir(os.getcwd() + '\\CppFile', _file_names, _file_paths, '.cpp')

        _exist_rename_file = False
        for _index in range(len(_file_names)):
            _unit_file_name = _file_names[_index]
            _name_early_part = _unit_file_name[:_unit_file_name.rfind('_')]  # 文件名的前部分
            _name_latter_part = _unit_file_name[_unit_file_name.rfind('_'):] # 文件名的后部分
            _new_name = self.get_new_file_name(_name_early_part)
            if _new_name == None:
                continue
            _exist_rename_file = True
            _path, _file_name = os.path.split(_file_paths[_index])
            _new_name = _new_name + _name_latter_part
            _new_file_path = os.path.join(_path, _new_name)
            print('random change file name, old name: ' + _file_name + ' ------> new name: ' + _new_name)
            os.rename(_file_paths[_index], _new_file_path)

        if _exist_rename_file == False:
            print('没有需要重命名的文件')

    # 通过旧名字获取到新的名称
    def get_new_file_name(self, _old_name):
       _name_dict = self.get_old_and_new_names()
       if _old_name in _name_dict.keys():
           _new_name = _name_dict[_old_name] + self.random_name()
           return _new_name
       return None

    # 新旧名字的对应关系
    def get_old_and_new_names(self):
        _names = {
            'Bulk_Assembly-CSharp': 'Batch_Packabe_CS_Code_',
            'Bulk_Generics': 'Batch_Produce_GT_',
            'Il2CppCompilerCalculateTypeValues': 'Il2CppEditorCountTypeValues_'
        }
        return _names

    def random_name(self):
        _name_len = random.randint(4, 7)
        _alphabet_upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        _alphabet_lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        _random_val = random.choice(_alphabet_upper)
        return _random_val

app = RandomChangeCppFileName()
app.start()
# os.system('pause')