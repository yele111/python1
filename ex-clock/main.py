
from MainWidget import MainWidget
from PySide2.QtWidgets import QApplication
import os
import sys
import PySide2
sys.path.append('../')

a=1
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

def main():
    app = QApplication(sys.argv) 
    
    mainWidget = MainWidget() #新建一个主界面
    mainWidget.show()    #显示主界面
    
    exit(app.exec_()) #进入消息循环
    
    
if __name__ == '__main__':
    main()
