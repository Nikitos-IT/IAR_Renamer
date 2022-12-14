import sys  # sys нужен для передачи argv в QApplication
import os  # Отсюда нам понадобятся методы для отображения содержимого директорий
import glob, os
import argparse
import shutil
from itertools import chain
import fnmatch 

from PyQt5 import QtWidgets


import design  # Это наш конвертированный файл дизайна


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Start_Rename) 
        self.lineEdit.returnPressed.connect(self.Start_Rename)
        self.label_3.setText("Ver 3.3") #Версия программы
        project_t = glob.glob("*.ewp")
        if not project_t:                
            self.textBrowser.setText("Косяки и хотелки пишите на kashirihin@mail.ru" + '\n' + "Не вижу файл проекта" + '\n' + "--------------------------------" + '\n')
        else:
            self.textBrowser.setText(
                "Косяки и хотелки пишите на kashirihin@mail.ru" + '\n' + "--------------------------------" + '\n')
            old_name_t = project_t[0]
            size_str_t = len(old_name_t)
            old_name_t = old_name_t[:size_str_t - 4]
            self.lineEdit.setText(str(old_name_t))
    
        
    

    def Start_Rename(self):
       def Send_txt(txt):
        temp_txt = self.textBrowser.toPlainText()     
        self.textBrowser.setText(temp_txt + txt + '\n')
        
       str4brouse = ''
       name = self.lineEdit.text()

       if name == '':
        Send_txt("Не введено имя проекта")
        Send_txt("--------------------------------")

        
       else:
           Send_txt("Новое имя проекта: " + name)
           def get_name(f):
            return os.path.splitext(os.path.basename(f))[0]

           def remove_by_mask(mask):
            for fl in glob.glob(mask):
              os.remove(fl)
              
           def faund_and_delete():
            old_name = project
            size_str = len(old_name)
            old_name = old_name[:size_str - 4]
            if old_name != "Code":
                Send_txt("Ищу старые файлы с маской: " + old_name)
                
                dir = os.path.abspath(os.curdir)
                dir = dir + '\settings'                
                files = os.listdir(dir)
                size = len(files)
                for i in range(size):
                 if files[i].find(old_name) != -1:                
                    pathdel = os.path.join(dir, files[i])
                    os.remove(pathdel)
                    Send_txt("Удален settings/" + files[i])
                    
                dir = os.path.abspath(os.curdir)
                Test_dir = ''
                with os.scandir(dir) as listOfEntries:
                    for entry in listOfEntries:
                        if entry.is_dir():

                            try:
                                Test_dir = dir + "\\" + str(entry.name) + '\Obj'
                                files2 = os.listdir(Test_dir)
                                print(Test_dir, "Тут есть обж")
                                break

                            except:
                                print(Test_dir,"Тут нет обж")


                dir = Test_dir
                files = os.listdir(dir)
                size = len(files)
                for i in range(size):
                 if files[i].find(old_name) != -1:                
                    pathdel = os.path.join(dir, files[i])
                    os.remove(pathdel)
                    Send_txt("Удален /Obj/" + files[i])

           project = glob.glob("*.ewp");
           if not project:                
                Send_txt("Не вижу файл проекта")
                Send_txt("--------------------------------") 
           else:   
                project = project[0]
                Send_txt("Найден проект: " + project)
                new_project = name + ".ewp"

                # Rename project
                os.rename(project, new_project)
                Send_txt("Файл проекта переименован")

                # Delete misc files
                remove_by_mask("*.dep")
                remove_by_mask("*.ewd")
                remove_by_mask("*.ewt")
                if os.path.exists("Debug"):
                    shutil.rmtree('Debug')
                if os.path.exists("Release"):
                    shutil.rmtree('Release')
                Send_txt("Удалены старые файлы")

                # Repalece in eww
                workspace = glob.glob("*.eww");
                if workspace:
                 ws = workspace[0]
                 filedata = None
                 with open(ws, 'r') as f:
                   filedata = f.read()
                 
                 filedata = filedata.replace(project, new_project)
                 with open(ws, 'w') as f:
                   f.write(filedata)
                 Send_txt("Закончена перезапись Workspace")
                 os.rename(ws, get_name(new_project)+".eww")
                 if get_name(ws) == get_name(project):
                   Send_txt("Готово, приступаю к удалению")
                   faund_and_delete()
                   Send_txt("Готово, проект переименован!")
                   Send_txt("--------------------------------") 
                 else:
                   Send_txt("Проект переименован не до конца, что то пошло не так. Но может все будет работать") 
                   Send_txt("--------------------------------")

   

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()