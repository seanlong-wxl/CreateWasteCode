工程主要实现的功能：
为ios提升，提供马甲包代码混淆

CreateDirectoryTree.py
主要实现的功能：
1、在给定的目录内向下遍历文件夹，在文件夹内随机创建5个子文件夹；
2、将MixCode文件夹中的.cs文件随机移动到上述创建的文件夹中；
目的：
1、混淆原工程的目录结构
2、在原工程代码中添加混淆垃圾类

ChangeNativeFile
主要实现的功能：
1、RandomChangeCppFileName.py 修改unity导出工程中native文件夹下的cpp文件名
2、RenameFuncOrVariateName.py 修改unity导出工程中native文件夹下的cpp类中的变量名，主要以_tn,_mn,_Tn,_Mn（n值1-9）

CreateMixWasteCode
主要实现的功能：
1、创建垃圾代码
2、创建有循环调用的垃圾代码
3、创建Lua底层调用的垃圾代码
4、创建需要lua调用的垃圾代码，即避免代码裁剪