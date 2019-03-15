import sys
from PyQt5.QtWidgets import QApplication , QMainWindow
from start import Ui_MainWindow
from autoverixss import *
import sys
global targeturl

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

def start():
    global targeturl
    # targeturl = sys.argv[1]
    # print("lalal",myWin.input_url.text())
    try:
        targeturl = myWin.input_url.text()
    except:
        print("未获取到 url 信息")
        sys.exit(0)
    # targeturl = "http://www.no1.edu.sh.cn/NEWS/SHOW_OUT/TeacherGrowthPocket/main_style00002/school_plan_list.asp(POST)start_month=&start_year=&PLAN_ID=&order_name=e.TEACHER_PLAN_EXAMPLE_TIME&end_year=&start_day=&subject_name=&have_update_record=></a><svg/%20onload=wfzxrx(6623)>&end_month=&end_day=&grade_name=&order_direct=desc&user_id=&PLAN_NAME=&Page=2"
    # PAYLOAD["url"] = re.sub("\w{6}\(\d{4}\)",PAYLOAD["1"],targeturl)
    print("验证URL：", targeturl)
    # rebuildurl()
    # checkxss()
    # prepare_check()
    rebuild()
    prepare_check()

if __name__=="__main__":
    app = QApplication(sys.argv) #the standard way to init QT
    myWin = MyMainWindow()
    myWin.show()
    # myWin.startx.clicked.connect(lambda :rebuild())

    myWin.startx.clicked.connect(lambda: start())
    sys.exit(app.exec_())