from datetime import datetime
from PyQt5.QtCore import QDate, QTime
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox
import json

# import menu database
with open('menu_db.json') as json_file:
    menu_db = json.load(json_file)

# import operating hours database
with open('opr_hr_db.json') as json_file:
    opr_hr_db = json.load(json_file)

# Date and time variables and functions
# -------------------------------------------------------------------------------------------

# current day in full text format
day_now = datetime.today().strftime('%A')

# current date and time
datetime_now = datetime.now()

# global wait time
waitTime = 0


# authors: Guat Kwan, Lan
# This changes the pages of the stacked widget in GUI.
# day_now and datetime_now is used to store both current datetime and custom
# datetime. Placing them within the function will reset it back to the current
# datetime whenever there is a page change.
# input: index = index of the page you want to set to (int)
# output: No output
def page(self, index):
    self.stackedWidget.setCurrentIndex(index)
    global day_now
    day_now = datetime.today().strftime('%A')
    global datetime_now
    datetime_now = datetime.now()


# author: Lan
# convert datetime to alphabetical day
# input: dt = datetime to convert (datetime)
# output: alphabetical day in week (string)
def dt_to_day(dt):
    day = dt.strftime('%A')
    return day


# author: Lan
# For converting string time into datetime object by
# combining desired date and the string time.
# input: date_time = a datetime or a date object to be combined with the time (date/datetime)
#        time = the time to be converted (string)
# output: a datetime generated from the input date and time (datetime)
def time_to_dt(date_time, time):
    input_time = datetime.strptime(time, '%H:%M:%S').time()
    date_time_comb = datetime.combine(date_time, input_time)
    return date_time_comb


# author: Lan
# For converting time from hh:mm:ss format to am/pm
# (mainly for displaying of operating hours)
# input: datetime to be converted (datetime)
# output: time in am/pm format (time)
def time_to_ampm(date_time):
    return date_time.strftime('%I:%M%p')


# Data retrieving functions
# -------------------------------------------------------------------------------------------
# author: Chi Hui
# For getting operating hours based on given day
# input: stall = the stall to retrieve info from (string)
#        input_day = the day of the opr hr (string)
# output: the opr hrs of the stall on the specified day (list)
def opr_hr_any(stall, input_day):
    wkday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    # To classify mon-fri under weekday
    if input_day in wkday:
        day = 'Weekday'
    else:
        day = input_day
    return opr_hr_db[stall][day]


# author: Chi Hui
# For accessing wait time
# input: stall = the stall to retrieve info from (string)
# output: wait time of stall (int)
def wait_time(stall):
    return menu_db[stall]['Wait Time']


# author: Chi Hui
# For accessing type/availability of special menu
# input: stall = the stall to retrieve info from (string)
# output: type of special menu (day, time or none) (string)
def special(stall):
    return menu_db[stall]['Special']


# author: Chi Hui
# For accessing breakfast/lunch timings.
# Need for start or end because timings are stored as [start_time, end_time].
# input: stall = the stall to retrieve info from (string)
#        period = 'Breakfast' or 'Lunch' (string)
#        start_or_end = 0 or 1, 0 for start time, 1 for end time (int)
# output: the starting or ending time of the breakfast/lunch period (string)
def sp_time(stall, period, start_or_end):
    return menu_db[stall]['Special Timings'][period][start_or_end]


# author: Chi Hui
# For getting regular menus (those without specials)
# For accessing overall menu (those with specials)
# input: stall = the stall to retrieve info from (string)
# output: dict of item:price for stalls without specials (dict)
#         dict of (day/time):menu for stalls with specials (dict)
def menu_reg(stall):
    return menu_db[stall]['Menu']


# author: Chi Hui
# For getting daily menus
# input: stall = the stall to retrieve info from (string)
#        day = the day of the menu (string)
# output: dict of item:price (dict)
def menu_day(stall, day):
    if day != 'Sunday':
        return menu_reg(stall)[day]
    else:
        return menu_reg(stall)['Saturday']


# author: Chi Hui
# For getting breakfast/lunch menus
# input: stall = the stall to retrieve info from (string)
#        period = 'Breakfast' or 'Lunch' (string)
# output: dict of item:price (dict)
def menu_time(stall, period):
    return menu_reg(stall)[period]


# author: Guat Kwan
# Retrieves the menu dict of the stall based on the specified day and time.
# input: stall = the stall to retrieve info from (string)
#        day = the day of the menu (string)
#        date_time = time but must be in datetime format (datetime)
# output: dict of item:price based on specified stall, day and time (dict)
def get_now_menu(stall, day, date_time):
    if special(stall) is None:
        return menu_reg(stall)

    elif special(stall) == 'Day':
        return menu_day(stall, day)

    elif special(stall) == 'Time':
        bf_start = time_to_dt(date_time, sp_time(stall, 'Breakfast', 0))
        bf_end = time_to_dt(date_time, sp_time(stall, 'Breakfast', 1))
        if bf_start < date_time <= bf_end:
            return menu_time(stall, 'Breakfast')
        else:
            return menu_time(stall, 'Lunch')


# Content generating functions
# -------------------------------------------------------------------------------------------

# author: Guat Kwan
# For converting dict of items:price into string
# so that it can be set on a label.
# input: menu = the menu to convert into string (dict)
# output: a formatted string of menu items and price that can be placed onto a label (string)
def menu_to_string(menu):
    text_list = []
    for item, price in menu.items():
        text_list.append(str(item) + ': ' + str(price) + '\n\n')
    return ''.join(text_list)


# author: Guat Kwan
# For generating formatted string of operating hours to be
# placed in operating hour label.
# input: stall = the stall to retrieve info from (string)
# output: a formatted string of day and opr hrs that can be placed onto a label (string)
def disp_opr_hr(stall):
    opr_hr = {
        'Weekday': opr_hr_any(stall, 'Weekday'),
        'Saturday': opr_hr_any(stall, 'Saturday'),
        'Sunday': opr_hr_any(stall, 'Sunday'),
        'Public Holidays': opr_hr_any(stall, 'PH')
    }
    text_list = []
    for key, value in opr_hr.items():
        if value == 'Closed':
            text_list.append(str(key) + ': Closed\n\n')
        elif type(value) == list:
            dt_begin = time_to_dt(datetime_now, value[0])
            dt_end = time_to_dt(datetime_now, value[1])
            text_list.append(str(key) + ': ' + str(time_to_ampm(dt_begin)) + ' - '
                             + str(time_to_ampm(dt_end)) + '\n\n')
    return ''.join(text_list)


# author: Guat Kwan
# For listing all the stalls that are open currently
# input: day = the day to check for (string)
#        date_time = the time to check for (datetime)
# output: list of open stalls (list)
def find_open_stalls(day, date_time):
    open_stalls = []
    for stall in opr_hr_db.keys():
        opr_hr = opr_hr_any(stall, day)
        if opr_hr != 'Closed':
            start_time = time_to_dt(date_time, opr_hr[0])
            end_time = time_to_dt(date_time, opr_hr[1])
            if start_time <= date_time <= end_time:
                open_stalls.append(stall)
            else:
                continue
    return open_stalls


# GUI functions
# -------------------------------------------------------------------------------------------
# author: Guat Kwan
# Function to send users to stall info page and set the
# contents based on the stall selected (for regular menu stalls)
# input: self
#        stall = the stall to retrieve info from (string)
# output: none
def info_reg(self, stall):
    self.stackedWidget.setCurrentIndex(2)

    global waitTime
    waitTime = wait_time(stall)

    menu_dict = menu_reg(stall)
    text_menu = menu_to_string(menu_dict)
    self.menulabel.setText(text_menu)

    text_opr = disp_opr_hr(stall)
    self.oprhrlabel.setText(text_opr)


# author: Guat Kwan
# Function to send users to stall info page and set the
# contents based on the stall selected (for time menu stalls)
# input: self
#        stall = the stall to retrieve info from (string)
# output: none
def info_time(self, stall):
    self.stackedWidget.setCurrentIndex(3)

    global waitTime
    waitTime = wait_time(stall)

    text_opr = disp_opr_hr(stall)
    self.oprhrlabel_2.setText(text_opr)

    menu_bf = menu_time(stall, 'Breakfast')
    menu_lunch = menu_time(stall, 'Lunch')
    text_menu_bf = menu_to_string(menu_bf)
    text_menu_lunch = menu_to_string(menu_lunch)
    self.bfmenu.setText(text_menu_bf)
    self.lunchmenu.setText(text_menu_lunch)


# author: Guat Kwan
# Function to send users to stall info page and set the
# contents based on the stall selected (for day menu stalls)
# input: self
#        stall = the stall to retrieve info from (string)
# output: none
def info_day(self, stall):
    self.stackedWidget.setCurrentIndex(4)
    global waitTime
    waitTime = wait_time(stall)

    day_label = {'Monday': self.mon_menu,
                 'Tuesday': self.tue_menu,
                 'Wednesday': self.wed_menu,
                 'Thursday': self.thu_menu,
                 'Friday': self.fri_menu,
                 'Saturday': self.sat_menu}

    for day, label in day_label.items():
        menu_dict = menu_day(stall, day)
        text_menu = menu_to_string(menu_dict)
        label.setText(text_menu)

    text_opr = disp_opr_hr(stall)
    self.oprhrlabel_3.setText(text_opr)


# author: Guat Kwan
# Function to send users to stall info page and set the
# contents based on the stall selected (for all stalls, only shows current menu)
# input: self
#        stall = the stall to retrieve info from (string)
#        day = day of menu (string)
#        date_time = time of menu (datetime)
# output: none
def info_current(self, stall, day, date_time):
    self.stackedWidget.setCurrentIndex(2)

    global waitTime
    waitTime = wait_time(stall)

    now_menu = get_now_menu(stall, day, date_time)
    text_menu = menu_to_string(now_menu)
    self.menulabel.setText(text_menu)

    text_opr = disp_opr_hr(stall)
    self.oprhrlabel.setText(text_opr)


# author: Lan
# Prompts a message box showing the operating hours of the stall
# when a closed stall is clicked.
# input: self
#        stall = the stall to retrieve info from (string)
# output: a message box with operating hours of the closed stall
def close_msg(self, stall):
    text_opr = disp_opr_hr(stall)
    msg = QMessageBox()
    msg.move(290, 275)
    msg.setStyleSheet("QLabel{min-height: 150px; min-width: 500px;}");
    msg.setText('\nOperating Hours:\n\n' + text_opr)
    msg.setWindowTitle('Stall Closed')
    msg.setStandardButtons(QMessageBox.Close)
    font = QtGui.QFont('Papyrus', 14)
    font.setBold(True)
    msg.setFont(font)
    msg.exec()


# author: Guat Kwan
# Changes colour of buttons based on which stalls are open
# and connect buttons to info_current function if they are open
# Green buttons lead to info page while red does nothing
# input: self
# output: none
def open_stall_btns(self):
    global day_now
    global datetime_now
    self.stackedWidget.setCurrentIndex(5)
    list_open_stall = find_open_stalls(day_now, datetime_now)
    stall_btn = {'Chicken Rice': self.chickenrice_4,
                 'Handmade Noodle': self.handmade_4,
                 'Indian Food': self.indian_4,
                 'McDonald\'s': self.mc_4,
                 'Mini Wok': self.miniwok_4,
                 'Vegetarian': self.vegetarian_4,
                 'Western Food': self.western_4}

    for stall, btn in stall_btn.items():
        try:
            btn.disconnect()
        except:
            pass
        if stall in list_open_stall:
            btn.setStyleSheet("background-color: rgb(85, 255, 127);")
            btn.clicked.connect(lambda checked, x=stall: info_current(self, x, day_now, datetime_now))
        else:
            btn.setStyleSheet("background-color: rgb(243, 91, 94);")
            btn.clicked.connect(lambda checked, x=stall: close_msg(self, x))


# author: Chi Hui
# Function checks that number entered by user is an integer that is between 0 to 100
# input: input(retrieves number(string) from user_input label)
#        error(label that allows us to print the error message (label in PyQt))
# output: error message on the type of error (if user input is wrong)
#         the wait time for the stall (if user input is right)
def wait_time_check(input, error):
    try:
        no_in_queue = int(input.toPlainText())
        if 101 > no_in_queue >= 0:
            error.clear()
            global waitTime
            wt = no_in_queue * waitTime
            error.setText('Waiting time: ' + str(wt) + ' minute(s)')
        else:
            input.clear()
            error.setText('Please enter a positive number'
                          ' within 0 and 100 inclusive.')
    except ValueError:
        error.clear()
        error.setText('Please enter an integer.')


# author: Chi Hui
# Function gets user_input (string) and the error_label(label in PyQt) in the different waittime pages
# Input: self
# Output: None
def time_wait(self):
    sender = self.sender()
    if sender == self.enter_button_1:
        user_input = self.enter_waittime_1
        error_label = self.error_msg_1
        wait_time_check(user_input, error_label)

    elif sender == self.enter_button_2:
        user_input = self.enter_waittime_2
        error_label = self.error_msg_2
        wait_time_check(user_input, error_label)

    elif sender == self.enter_button_3:
        user_input = self.enter_waittime_3
        error_label = self.error_msg_3
        wait_time_check(user_input, error_label)


# author: Lan
# This function gets the date and the date time from the users.
# It converts the inputs to suitable format and updates the global day and datetime.
# input: self
# output: none
def customised_datetime(self):
    # get value from the calendar
    ca = self.calendar.selectedDate()
    custom_date = ca.toPyDate()

    # get value from the hour_in and minute_in spin box
    hour = self.hour_in.value()
    minute = self.minute_in.value()
    custom_time_str = str(hour) + ':' + str(minute) + ':' + '00'

    # update the global variables
    global datetime_now
    datetime_now = time_to_dt(custom_date, custom_time_str)
    global day_now
    day_now = dt_to_day(datetime_now)

    self.enter_timeInput.setEnabled(True)
    self.view_button.setEnabled(True)


# author: Lan
# This function displays the customised day and datetime on the GUI
# input: self
# output: none
def custom_time_label(self):
    self.label_3.setText('Your selected day is a ' + day_now
                         + ' and your selected time is ' + time_to_ampm(datetime_now))


# author: Lan
# This function clears the customised datetime from the users once the task is done.
# input: self
# output: none
def clear_customisation(self):
    self.label_3.clear()
    self.hour_in.setValue(QTime.currentTime().hour())
    self.minute_in.setValue(QTime.currentTime().minute())
    self.hour_in.clear()
    self.minute_in.clear()
    self.calendar.setSelectedDate(QDate.currentDate())
