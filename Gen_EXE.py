import os
import shutil

dir = os.path.abspath(os.curdir)
dir = dir + '\dist'                
files = os.listdir(dir)
size = len(files)
new_name = ""
for i in range(size):
 if files[i].find('.exe') != -1:                
    old_name = files[i]
    size_str = len(old_name)
    old_name = old_name[:size_str - 4]
    new_name = old_name + ".py"
    print(old_name)
cmd_copy = 'copy main.py ' + new_name
print(cmd_copy)
os.popen(cmd_copy)

os.system("pyinstaller --noconsole --onefile " + new_name)
path = os.path.join(os.path.abspath(os.path.dirname(__file__)), new_name)
os.remove(path)