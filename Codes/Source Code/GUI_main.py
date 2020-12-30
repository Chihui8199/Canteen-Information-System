from PyQt5 import QtWidgets, uic, QtCore
from GUI_func import *
import sys


# authors: Guat Kwan, Lan, Chi Hui
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('GUI2.ui', self)
        self.setWindowTitle('NTU Canteen Helper')

        # homepage (page1)
        # ----------------------------------------------------------
        # all stalls button
        self.view_all_stalls.clicked.connect(lambda: page(self, 1))
        # currently opened stalls button
        self.open_stalls.clicked.connect(lambda: open_stall_btns(self))
        # custom datetime button
        self.custom_dt.clicked.connect(lambda: page(self, 6))
        self.custom_dt.clicked.connect(lambda: self.view_button.setEnabled(False))
        self.custom_dt.clicked.connect(lambda: clear_customisation(self))

        # all stalls page (page2)
        # ----------------------------------------------------------
        # home button
        self.home_p2.clicked.connect(lambda: page(self, 0))
        # stall buttons
        self.chickenrice.clicked.connect(lambda: info_reg(self, 'Chicken Rice'))
        self.handmade.clicked.connect(lambda: info_reg(self, 'Handmade Noodle'))
        self.indian.clicked.connect(lambda: info_reg(self, 'Indian Food'))
        self.miniwok.clicked.connect(lambda: info_reg(self, 'Mini Wok'))
        self.western.clicked.connect(lambda: info_reg(self, 'Western Food'))
        self.mc.clicked.connect(lambda: info_time(self, 'McDonald\'s'))
        self.vegetarian.clicked.connect(lambda: info_day(self, 'Vegetarian'))

        # stall info page for reg menus (page3)
        # ----------------------------------------------------------
        # home buttons for operating hour, menu and wait time tabs
        self.home_p3.clicked.connect(lambda: page(self, 0))
        self.home_p3.clicked.connect(self.enter_waittime_1.clear)
        self.home_p3.clicked.connect(self.error_msg_1.clear)
        # calculate wait time button
        self.enter_button_1.clicked.connect(lambda: time_wait(self))

        # stall info page for time menus (page4)
        # ----------------------------------------------------------
        # home buttons for operating hour, menu and wait time tabs
        self.home_p4.clicked.connect(lambda: page(self, 0))
        self.home_p4.clicked.connect(self.enter_waittime_2.clear)
        self.home_p4.clicked.connect(self.error_msg_2.clear)
        # calculate wait time button
        self.enter_button_2.clicked.connect(lambda: time_wait(self))

        # stall info page for day menus (page5)
        # ----------------------------------------------------------
        # home buttons for operating hour, menu and wait time tabs
        self.home_p5.clicked.connect(lambda: page(self, 0))
        self.home_p5.clicked.connect(self.enter_waittime_3.clear)
        self.home_p5.clicked.connect(self.error_msg_3.clear)
        # calculate wait time button
        self.enter_button_3.clicked.connect(lambda: time_wait(self))

        # current stalls page (page6)
        # ----------------------------------------------------------
        # home button
        self.home_p6.clicked.connect(lambda: page(self, 0))

        # customised datetime page (page7)
        # ----------------------------------------------------------
        # home button
        self.home_p7.clicked.connect(lambda: page(self, 0))
        # enter custom date and time button
        self.enter_timeInput.clicked.connect(lambda: customised_datetime(self))
        self.enter_timeInput.clicked.connect(lambda: custom_time_label(self))
        # view opened stalls button
        self.view_button.clicked.connect(lambda: open_stall_btns(self))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()

    # gets the current date time and display it in GUI
    def update_label():
        current_time = datetime.strftime(datetime.now(), "%A, %b %d, %Y %I:%M:%S%p")
        w.time.setText(current_time)

    # this calls update_label every 1s so the time displayed changes every second
    timer = QtCore.QTimer()
    timer.timeout.connect(update_label)
    timer.start(1000)

    sys.exit(app.exec_())
