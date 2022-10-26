import traceback, os, time, sys, json
from path import path
from ui.titleWindow import TitleWindow
from system_hotkey import SystemHotkey
from ui.Ui_main import Ui_Form
from pytube import YouTube
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QAction, QMenu, QSystemTrayIcon
from PyQt5.QtCore import QThread, pyqtSignal
from biliup.plugins.bili_webup import BiliBili, Data
from qt_material import apply_stylesheet

class RunThread(QThread):
    trigger = pyqtSignal()
    url = ""
    tid = 160

    def __init__(self, url, tid):
        super(RunThread, self).__init__()
        self.url = url
        self.tid = tid

    def __del__(self):
        self.wait()

    def print(self, s):
        print(s)
        s = "{}\n".format(s)
        myWin.widget_2_sub.textBrowser.append(s)
        myWin.widget_2_sub.textBrowser.moveCursor(myWin.widget_2_sub.textBrowser.textCursor().End)

    def run(self):
        try:
            while True:
                try:
                    try:
                        os.remove(path("video_tube.mp4"))
                    except Exception:
                        pass
                    yt = YouTube(self.url)
                    title = yt.title
                    desc = yt.description
                    keywords = yt.keywords or ['TubeToBili']
                    self.print(title)
                    self.print(desc)
                    self.print(keywords)
                    self.print("get successfully")
                    streams = yt.streams.filter(progressive=True).filter(res="720p", subtype="mp4")
                    self.print(streams)
                    streams.first().download(output_path=path(), filename="tube.mp4", filename_prefix="video_")
                    self.print("download successfully")
                    break
                except Exception:
                    self.print(traceback.format_exc())
                    self.print("wait for another try")
                    time.sleep(3)
                    continue
            
            self.print("upload to bilibili after 5 seconds")
            time.sleep(5)

            while True:
                try:
                    self.print("uploading to bilibili...")

                    # 数据处理
                    if len(keywords) > 12:
                        keywords = keywords[:12]
                    if len(title) > 80:
                        title = title[:80]
                    for i in keywords:
                        if len(i) > 20:
                            i = i[:20]
                    
                    # 上传
                    video = Data()
                    video.title = title
                    video.desc = desc
                    video.source = self.url
                    video.tid = int(self.tid)
                    video.set_tag(keywords)
                    with BiliBili(video) as bili:
                        bili.login("bili.cookie", {})
                        video_part = bili.upload_file(path("video_tube.mp4"))  # 上传视频
                        video.append(video_part)  # 添加已经上传的视频
                        # video.cover = bili.cover_up('/cover_path').replace('http:', '')
                        ret = bili.submit()  # 提交视频
                    self.print("Upload to bilibili successfully!")
                    self.print("上传成功，请前往B站创作中心查看稿件")
                    break
                except Exception:
                    self.print(traceback.format_exc())
                    self.print("wait for another try")
                    time.sleep(3)
                    continue
        except Exception:
            pass

class MyMainWindow(QWidget, Ui_Form):
    sig_keyhot = pyqtSignal(str)
    thread = None

    def __init__(self,parent =None):
        super(MyMainWindow,self).__init__(parent)
        # Form init
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowIcon(QIcon("./icon.jpg"))

    def _init(self):
        # trayIconMenu init
        self.openAction = QAction("打开主界面", self)
        self.exitAction = QAction("退出程序", self)
        self.aboutAction = QAction("关于", self)
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.openAction)
        self.trayIconMenu.addAction(self.exitAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.aboutAction)
        self.openAction.triggered.connect(myWin.show)
        self.exitAction.triggered.connect(app.quit)
        # self.aboutAction.triggered.connect(self.about)
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(QIcon(path("icon.jpg")))
        self.trayIcon.setToolTip("TubeToBili")
        self.trayIcon.show()

        # hotkey init
        self.sig_keyhot.connect(self.MKey_pressEvent)
        self.hk_quit,self.hk_show,self.hk_hide = SystemHotkey(), SystemHotkey(), SystemHotkey()
        self.hk_quit.register(('control','q'),callback=lambda x:self.send_key_event("quit"))
        self.hk_show.register(('control', 'up'), callback=lambda x:self.send_key_event("show"))
        self.hk_hide.register(('control', 'down'), callback=lambda x:self.send_key_event("hide"))

        # bilibili cookies init
        with open(path('bili.cookie'), 'r', encoding='utf8') as fp:
            cookies = json.load(fp)
            for i in cookies:
                exec("self.{}.setText('{}')".format(i, cookies.get(i)))

        # clicked connect
        self.startBtn.clicked.connect(self.start)
        self.stopBtn.clicked.connect(self.stop)
    
    def stop(self):
        if self.thread:
            self.thread.quit()
            self.textBrowser.setText("")
        else:
            QMessageBox.warning(self, "停止失败", "您还没有开始")

    def start(self):
        self.textBrowser.setText("Saving cookies")
        with open(path('bili.cookie'), 'r', encoding='utf8') as fp:
            cookies = json.load(fp)
            for i in cookies:
                exec("cookies[i] = self.{}.text()".format(i))
            with open(path("bili.cookie"), "w", encoding="utf8") as wp:
                wp.write(json.dumps(cookies))
        
        QMessageBox.information(self, "注意事项", "请注意\n从YouTube下载视频时，请尽量开启代理的全局模式\n上传B站时，请尽量开启规则模式（PAC模式）\n下载完成后，会有五秒间隔时间\n下载或上传失败后，三秒后会自动重试")

        self.thread = RunThread(self.url.text(), self.tid.text())
        self.thread.start()

    def MKey_pressEvent(self,i_str):
        if i_str == "quit":
            app.quit()
        elif i_str == "show":
            myWin.show()
        elif i_str == "hide":
            myWin.hide()
        
    def send_key_event(self,i_str):
        self.sig_keyhot.emit(i_str)

app = QApplication(sys.argv)
# setup stylesheet
apply_stylesheet(app, theme='dark_teal.xml')
QApplication.setQuitOnLastWindowClosed(False)
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
myWin = TitleWindow(widget_2_sub=MyMainWindow(),icon_path=path("icon.jpg"),title='TubeToBili')
myWin.setWindowIcon(QIcon("./icon.jpg"))
myWin.setWindowTitle("TubeToBili")
myWin.setWindowFlags(QtCore.Qt.FramelessWindowHint)
def run():
    myWin.widget_2_sub._init()
    myWin.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()