
# author: wxl @ 2020-11-4
# info: 1、在现有的文件树结构中随机再次创建文件树 -- 降低文件结构的相似度
#       2、将随机生成的C#垃圾类代码，随机的放入到第一步创建的文件数中


import os
import random
import shutil

import Utils
import copy

class CreateDirectoryTree():

    _target_dir_path_1 = 'D:\\UserProj\\jlClient\\Assets\\LuaFramework\\Scripts\\SurplusScripts\\RandomClassForWrap\\'
    _target_dir_path_2 = ''

    def Start(self):
        _mixcode_path = os.getcwd() + '\\RandomCodeClass\\'
        _new_dir_tree = self.run_create_dir()
        self.run_move_mix_file(_new_dir_tree, _mixcode_path)

    # -------------------------------------1、目录树操作-----------------------------------------------------#
    # 在当前路径内，在额外创建5个文件夹，路径结构相对当前路径随机
    def run_create_dir(self):
        _dir_paths_1 = []
        _dir_paths_2 = []
        _dir_num_2 = 0
        _dir_num_1, _dir_paths_1 = self.get_cur_path_dir_num(self._target_dir_path_1, _dir_paths_1)
        # _dir_num_2, _dir_paths_2 = self.get_cur_path_dir_num(self._target_dir_path_2, _dir_paths_2)

        _dir_paths = []
        _dir_paths.append(self._target_dir_path_1)
        # _dir_paths.append(self._target_dir_path_2)
        _dir_paths += _dir_paths_1 + _dir_paths_2
        _dir_num = len(_dir_paths)

        _create_new_dirs = []
        for _num in range(_dir_num):
            _cur_dir_path = _dir_paths[_num]
            _create_new_dirs += self.random_create_dir_tree_in_path(_cur_dir_path, 5)
        return _create_new_dirs

    # 得到当前路径内文件夹的个数
    # 得到当前路径内所有的文件夹路径结构
    def get_cur_path_dir_num(self, _dir_path, _result_list):
        _fileList = os.listdir(_dir_path)
        for _unit_file in _fileList:
            _filePath = os.path.join(_dir_path, _unit_file)
            if os.path.isdir(_filePath):
                self.get_cur_path_dir_num(_filePath, _result_list)
                _result_list.append(_filePath)
                continue
        return len(_result_list), _result_list

    # 在指定的路径内，随机创建多级目录树
    # 返回创建的最新的路径
    def random_create_dir_tree_in_path(self, _path, _create_dir_num):
        _random_dir_path = []
        _random_dir_path.append(_path)
        for i in range(_create_dir_num):
            _random_dir_name = Utils.random_name('MixWrap_')
            _tar_path = random.choice(_random_dir_path)
            if 'Editor' in _tar_path or 'Scenes' in _tar_path:
                _random_dir_path.remove(_path)
                if len(_random_dir_path) == 0:
                    break
                continue
            _create_dir_path = _tar_path + '\\' + _random_dir_name
            _random_dir_path.append(_create_dir_path)
            os.mkdir(_create_dir_path)
        if len(_random_dir_path) != 0:
            _random_dir_path.remove(_path)
        return _random_dir_path
    # --------------------------------------------------------------------------------------------------------------#

    # --------------------------------2、将生成的垃圾代码，放入到新创建的目录树中-----------------------------------#
    # 移动混淆代码
    def run_move_mix_file(self, _tar_dir, _mix_code_dir_path):
        _file_names = []
        _file_paths = []
        Utils.get_fileinfo_from_dir(_mix_code_dir_path, _file_names, _file_paths, '.cs')

        _target_dir = []
        for _unit_file in _file_paths:
            # 随机放入，随机结束后，重新随机
            if len(_target_dir) == 0:
                _target_dir = _tar_dir[:]
            if len(_target_dir) == 0:
                a = 0
            _dir = random.choice(_target_dir)

            shutil.copy(_unit_file, _dir+'\\')
            _target_dir.remove(_dir)

    # 得到文件数量
    def get_file_num(self):
        _target_dir_path_1 = 'D:\\UserProj\\jlClient\\Assets'

        # _target_dir_path_2 = 'D:\\UserProj\\jlClient\\Assets\\Scripts\\'

        _file_names_1 = []
        _file_paths_1 = []
        Utils.get_fileinfo_from_dir(_target_dir_path_1, _file_names_1, _file_paths_1, '.cs')

        _file_names_2 = []
        _file_paths_2 = []
        # Utils.get_fileinfo_from_dir(_target_dir_path_2, _file_names_2, _file_paths_2, '.cs')

        print(len(_file_names_1) + len(_file_names_2))



dirTree = CreateDirectoryTree()
dirTree.Start()
# dirTree.get_file_num()