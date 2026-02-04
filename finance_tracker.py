# _________________________________ DEPENDENCIES _________________________________
import datetime
import pandas as pd
import os
import re
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.font as tkfont
from tkcalendar import Calendar
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# _________________________________ PARAMETERS _________________________________
window = tk.Tk(className='Expense tracker')

# ------------ global variables
account_file = 'accounts.txt'
finance_file = 'finances.txt'

screen_w = window.winfo_screenwidth()
screen_h = window.winfo_screenheight()

selected_account = tk.StringVar() # saves selected account or accounts
selected_account.set('Select Account')

selected_account_label = tk.StringVar() # show item selection for multiselect button
selected_account_label.set('Select Accounts')
trunc_acc = tk.StringVar()

selected_time = tk.StringVar() # selected time (1/3/6/9/12 months or all time)
selected_time.set('all time')

selected_date = tk.StringVar() # input date for new entry
selected_date.set(None)

bg_common = "#aaaaaa" # common background
bg_text = "#d4d4d4" # background for text (input fields or selection)
bg_button = '#85929b' # passive button color
bg_selected = "#777777" # background when selecting items (table or choices)

fg_common = 'black' # common text (output, input, active button)
fg_button = 'white' # text for passive buttons, labels, headers
fg_error = '#ffb5b5' # error message text color

# for windows DejaVu Sans
# for linux Helvetica
font_header = tkfont.Font(family='Helvetica', size=-36, weight='bold')
font_label = tkfont.Font(family='Helvetica', size=-22, weight='bold')
font_text = tkfont.Font(family='Helvetica', size=-16) # font for common text (table, text in graphs)
font_entry = tkfont.Font(family='Helvetica', size=-16, weight='bold')
font_error = tkfont.Font(family='Helvetica', size=-12, weight='bold')

# calendar icon
calendar_hash = """
iVBORw0KGgoAAAANSUhEUgAAABMAAAATCAYAAAByUDbMAAAACXBIWXMAAAsSAAALEgHS3X78AAAC
q0lEQVQ4T5VUS6hSURS9/v/fpybxxESUR1MHzRUHKihIA5u8gaHkSGgQ1Eh4CA0isaIGEZJBGUUN
GtQoaNKHmgQPc/IoCiJEi/AV/k9rX++9Xe1FduBw3fvsvdba69wrxwmrXC471Wo1QyhtjUbzRjxf
66nX618qFIqOSqV6HQ6H/WJTNBrdxNlHnLF4PG5dBcPZ/T8IvF7vVVKDpuFB7BaL5YlSqSS1XL1e
17daLb1Qx5rNpnKphwp1Ot03KFsCMxqNj0GUoGKqMZvNKRDOBRsoTQQRetJ5LpfT8kn4ZahUKjqR
xWAwvALQjhhbrda7IHsL0usiGI2P/DHRY/j9TGSQ1Lrd7hD8eCqXHwgEqmj+ApLTgiUMNc/llwXg
fR4smUy65M1Op/OMPIaiPSi7hdt9QYpWN2HY7fY5h8J38Oe9vNnj8RwX41gstkHFkUiEngcuEE0g
gHHValVFTEC+t1qZzWY3yFyM9yCfz5t9Pt9Fv9/vobpQKHRJrCcwh8PB3zgHdgs10bbZbDeCweBZ
eLJLiqD6IdVkMplDQnyUYgAsmhe/f4Oh4UM6nbYA/SR82QPod6h5hNG8fxtNnpfGpKRWq/2Ex1gs
gI8narWaEuqs2NuFQsGcSCR0qMvBDv5rMJlM23JlyDPpDQa6RDYajW632231cDg8jH2z3++Tavt4
PL6Ds00qpLxcHaZZhKQM40kerDPa6ph0AaKyJSCAs1KppMW4W9isWCweSaVSHiLEy7nVaDQU8Hmp
hzHG8WDT6XQfr4dEhnE6s9mMYSRaHTSOXS7XfDKZdOZY1Eg1cnVI/+RjAO0K/2X/OyFfj94ZLuqz
mgJ8j9e63e4VjEHf14SY11nCNBooVuJ2z0uz4WpPIXkOfzVOsJj+BQZCsuHHYDD4Chsu9Hq9y78A
i+P16JcUynwAAAAASUVORK5CYII=
"""
calendar_icon = tk.PhotoImage(data=calendar_hash)

# list of purpose suggestions
purpose_list = []

# ------------ custom style configuration
style = ttk.Style()
style.theme_use('default')
# frame / spacer (empty space)
style.configure('TFrame',
                background = bg_common)
# treeview (table of saved data)
style.configure('Treeview', # table of data (below header)
                background = bg_text,
                fieldbackground = bg_common,
                font = font_text)
style.configure('Treeview.Heading', # header (1-ist line)
                background = bg_button,
                foreground=fg_button,
                font = font_text)
style.map('Treeview.Heading', # header when selected
          background=[('active', bg_button)])
style.map('Treeview', # table of data when selected
          background=[('selected', bg_selected)],
          foreground=[('selected', fg_button)])
# entry
style.configure('TEntry',
                fieldbackground = bg_text,
                foreground = fg_common,
                padding = 5)
# button
style.configure('TButton', # button when passive (just displayed)
                background = bg_button,
                foreground = fg_button,
                font = font_entry,
                padding = (4, 8))
style.map('TButton', # button when pressed
          background = [('active', bg_text)],
          foreground = [('active', fg_common)])
window.option_add('*TButton*takeFocus', 0) # disable dotted line when button is pressed
# label (above widget)
style.configure('field.TLabel',
                background = bg_common,
                foreground = fg_button,
                font = font_label)
# header (first text on the page)
style.configure('header.TLabel',
                background = bg_common,
                foreground = fg_button,
                font = font_header)
# chart header (first text of chart)
style.configure('chart.TLabel',
                background = bg_button,
                foreground = fg_button,
                font = font_label,
                padding = 2)

# _________________________________ HELPER FUNCTIONS _________________________________
# ------------ keyboard integration
# close app with Esc 
def close_window(event):
    window.destroy()
window.bind('<Escape>', lambda event: close_window(event))

# ------------ window control
# set window size/position
def set_window(frame, w, h, parent=None, reposition=False):
    # get bottom left coordinates
    x = (screen_w / 2) - (w / 2)
    y = (screen_h / 3) - (h / 3)
    # position window
    if reposition is True and parent is not None: # reposition = True, position in the middle of the screen/parent widget
        parent.update_idletasks()
        px = parent.winfo_x()
        py = parent.winfo_y()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        x = px + (pw / 2) - (w / 2)
        y = py + (ph / 2) - (h / 2)
        frame.geometry('%dx%d+%d+%d' % (w, h, x, y))
    elif reposition is True:
        frame.geometry('%dx%d+%d+%d' % (w, h, x, y))
    else:
        frame.geometry('%dx%d' % (w, h))

# reload window 
# goes through all widgets on window and erases them
def reset_window(frame, w=600, h=600):
    # rebuild window to specific size, choice/input windows general 600x600
    set_window(frame, w, h)
    
    # destroy all widgets, to make window completely empty (anything below menu)
    for widget in main_frame.winfo_children():
        widget.destroy()

# ------------ widgets
# error message
def create_error_msg(frame):
    error = ttk.Label(frame, text='', font=font_error, background=bg_common, foreground=fg_error)
    error.pack()
    return error

# create header/label widget
def create_text_widget(frame, widget_type, text, spacer_pady=0, header_pady=30, label_pady=10):
    # header
    if widget_type == 'header':
        header = ttk.Label(frame, text=text, style='header.TLabel')
        header.pack(pady=header_pady)
        spacer = ttk.Frame(frame)
        spacer.pack(pady=spacer_pady)
    # label
    elif widget_type == 'label':
        spacer = ttk.Frame(frame)
        spacer.pack(pady=spacer_pady)
        label = ttk.Label(frame, text=text, style='field.TLabel')
        label.pack(pady=label_pady)

# create entry
def create_entry(frame, entry_pady=5):
    entry = ttk.Entry(frame, font=font_entry)
    entry.pack(pady=entry_pady)
    return entry

# create button
def create_button(frame, text, button_pady, spacer_pady, command, text_var=None, w=15):
    spacer = ttk.Frame(frame)
    spacer.pack(pady=spacer_pady)
    button = ttk.Button(frame, command=command, text=text, textvariable=text_var, style='TButton', width=w)
    button.pack(pady=button_pady)

# creat top level (popup)
def create_toplevel(frame, w, h):
    toplevel = tk.Toplevel(frame)
    toplevel.withdraw()
    toplevel.configure(background=bg_common)
    set_window(toplevel, w, h, parent=window, reposition=True)
    toplevel.deiconify()
    toplevel.grab_set()
    return toplevel

# create listbox
def create_listbox(frame, var_list, select_mode, command):
    listbox = tk.Listbox(frame, listvariable=var_list)
    listbox.pack()
    if select_mode == 'single':
        listbox.configure(selectmode=tk.SINGLE)
        listbox.bind('<<ListboxSelect>>', command)
    else:
        listbox.configure(selectmode=tk.MULTIPLE)
        listbox.bind('<ButtonRelease-1>', command)
    listbox.configure(background=bg_text, foreground=fg_common, font=font_text, selectbackground=bg_selected, selectforeground=fg_button)
    return listbox

# ------------ file actions
# read file
def read_file():
    acc_dict = {}
    with open(account_file, 'r') as file:
        for line in file:
            # delete \n
            line = line.strip()
            # divide into account name and class (in file acc-class)
            value, key = line.split('-')
            # add all values with same key as a list to that key - {'key':[a,b,c]}
            acc_dict.setdefault(key, []).append(value)
    return acc_dict

# create pandas table 
def create_table():
    # filter by account
    def filter_account(df):
        account_list = selected_account.get().split(',')
        account_list = [acc.strip() for acc in account_list] # strip anything extra
        filtered_df = df[df['account'].isin(account_list)] # check if selected accounts are in the full account list
        return filtered_df
    
    # filter by time
    def filter_time(df):
        date = selected_time.get()
        # calculate date (n month from the date of last input (not from current day)) + 00.00.00 time 
        max_date = df['date'].max().normalize()
    
        if date == '1 month':
            min_date = max_date - pd.DateOffset(months=1)
        elif date == '3 months':
            min_date = max_date - pd.DateOffset(months=3)
        elif date == '6 months':
            min_date = max_date - pd.DateOffset(months=6)
        elif date == '9 months':
            min_date = max_date - pd.DateOffset(months=9)
        elif date == '1 year':
            min_date = max_date - pd.DateOffset(years=1)
        elif date == 'all time':
            return df
    
        filtered_df = df[(df['date'] >= min_date) & (df['date'] <= max_date)] # keep only date in bounds min_date-max_date
        return filtered_df
    
    # create dataframe
    df = pd.read_csv(finance_file, sep='|')
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d') # transform text to pd date
    df.sort_values(by='date', inplace=True)
    
    # add column for current amount (how much money in total at specific date) -> day1 = 23.00, day2 = 10.00 -> day1_sum = 23.00, day2_sum = 33.00
    df['signed_amount'] = df.apply(lambda row: row['amount'] if row['symbol'] == '+' else -row['amount'], axis=1).apply(lambda x: round(x, 2)) # if symbol '+' -> +number, else -> -number, then format 00.00
    df['current_amount'] = df.groupby('account')['signed_amount'].cumsum().apply(lambda x: round(x, 2)) # group by account, add 'signed_amount' for each new line, format as 00.00
    # get account list for filter
    if selected_account.get() == 'all' and selected_time.get() == 'all time':
        df = df.copy()
        df['date'] = df['date'].dt.date # take away 00.00.00 from dates
        return df
    elif selected_account.get() != 'all' and selected_time.get() == 'all time':
        # filter by accounts
        filtered_df = filter_account(df)
        filtered_df = filtered_df.copy()
        filtered_df['date'] = filtered_df['date'].dt.date
        return filtered_df       
    elif selected_account.get() == 'all' and selected_time.get() != 'all time':
        # filter by date
        filtered_df = filter_time(df)
        filtered_df = filtered_df.copy()
        filtered_df['date'] = filtered_df['date'].dt.date
        return filtered_df  
    else:
        filtered_df = filter_account(df)
        filtered_df = filter_time(filtered_df)
        filtered_df = filtered_df.copy()
        filtered_df['date'] = filtered_df['date'].dt.date
        return filtered_df

# finance purpose list
def make_purpose_list():
###
# read the finance.txt file and extract last column of all rows
# save the values into list to auto-suggest purpose in entry window
###
    all_purposes = []
    with open(finance_file, 'r') as file:
        for line in file:
            # get the 5-th value (5-th column = purpose)
            purpose = [p for p in line.strip().split('|')][4]
            all_purposes.append(purpose)
    # get unique values and convert back to list
    purpose_list = list(set(all_purposes))
    return purpose_list

# ------------ listbox function
# select single item
def select_single_item(event, label_var, error_msg=None):
    # get widget
    listbox = event.widget
    # get selection (return index of selection)
    selected = listbox.curselection()
    # if selecting empty space or similar, don't react
    if not selected:
        return
        
    # retrieve selection values (take first element from indexes list, becouse selected only 1 items)
    index = selected[0]
    selected_value = listbox.get(index)
        
    # set global selected account label (change button text to see what's selected and write to txt)
    label_var.set(selected_value)
    
    # clear error after selection
    if error_msg:
        error_msg.config(text='', background=bg_common)
    listbox.master.destroy()

# ------------ fail checks
# check if selected account is valid for window 
def check_selected_acc(window, error_msg=None):
    # entry/chart only takes 1 account, if previously more selected, reset it
    if window == 'chart' or window == 'entry':
        if len(selected_account.get().split(',')) >= 2 or selected_account.get() == 'all': # if selected account is list from more than 1 value or this value is 'all', reset the global variable
            selected_account.set('Select Account')
    # change button text if account is chosen in different window (single select: entry/chart)
    elif window == 'history' or window == 'overview' or window == 'export':
        if selected_account.get() != 'Select Account':
            selected_account_label.set(selected_account.get())
        elif selected_account.get() == 'Select Account' and selected_account_label.get() != 'Select Accounts': # if entry/chart resets accounts, reset button text
            selected_account_label.set('Select Accounts')
    # check if account selected in main_fuction single/multi/table/graph/chart/export
    elif window == 'display': 
        if selected_account.get() == 'Select Account':
            error_msg.config(text='Account must be selected', background=bg_button)
            return False
        else:
            error_msg.config(text='', background=bg_common)
            return True
    return True

# check wrong/missing input
def input_check(error_msg, type, value, text): # error widget, value to compare, text to input
    # missing input
    if type == 'missing':
        # check if account is chosen
        if value == 'Select Account': # account is not selcted, throw error message and prevent activation
            error_msg.config(text='Must select account', background=bg_button)
            return False
        elif value == '':
            error_msg.config(text=text, background=bg_button)
            return False
        else: # hide the error message if all good
            error_msg.config(text='', background=bg_common)
            return True
    # wrong amount format
    elif type == 'number':
        if not re.match(r'^[+-]?\d+(\.\d{1,2})?$', value): # checks for amount to have: +/-/nothing at start and number to match 0, 0.0, 0.00 (without space)
            error_msg.config(text=text, background=bg_button)
            return False
        else:
            error_msg.config(text='', background=bg_common)
            return True
    # char limit
    elif type == 'text':
        if len(value) >= 31:
            error_msg.config(text=text, background=bg_button)
            return False
        else:
            error_msg.config(text='', background=bg_common)
            return True

# _________________________________ MAIN FUNCTIONS _________________________________
# ------------ selection
# select single account 
def load_account_single(label_var, error_msg):
###
# open new window for accounts selection using listbox
# read account txt file and split them in account and class (account1-live\n account2-live\n -> {'live':[account1, account2]})
# put accounts in the listbox and activate script (saving selection) after clicking on account + close the popup
### 
    toplevel = create_toplevel(main_frame, 220, 220)
    # read data from txt and write to dict
    acc_dict = read_file()
    
    # flatten all values into 1 list - {'key1':[a, b], 'key2':[c, d]} -> [a, b, c, d]
    all_accounts = [acc for accounts in acc_dict.values() for acc in accounts]
    # convert to tuple and add as listbox variables
    account_var = tk.Variable(value=tuple(all_accounts))
    
    # create listbox widget
    listbox = create_listbox(toplevel, account_var, 'single', lambda event: select_single_item(event, label_var, error_msg))

# select multiple accounts 
def multi_choice_account(label_var, error_msg):
    toplevel = create_toplevel(main_frame, 220, 280)
    # deselect all/other
    ###
    # follow user selected accounts to prevent choosing 'all' when other selections are made and opposite
    # if 'all' is selected after other selections are made, deselect selection except 'all'
    # if any selection is made after 'all' is selected, deselect 'all'
    # check the logic after button release, to show how selections are changed live
    ###
    def check_for_all(event):
        clicked_index = listbox.nearest(event.y)
        clicked_item = listbox.get(clicked_index)
        selected = listbox.curselection()
        selected_acc = [listbox.get(i) for i in selected]
        
        # all check
        if clicked_item == 'all':
            # if 'all' selected alongside other selections
            for i in range(len(all_accounts)):
                # if first element is not 'all', means it is selected last
                if listbox.get(i) != 'all':
                    # clear anything but 'all'
                    listbox.selection_clear(i)
            # update selection
            listbox.selection_set(clicked_index)
        else:
            # all was selected, but not current selection
            if 'all' in selected_acc:
                for i in range(len(all_accounts)):
                    # if first element is all
                    if listbox.get(i) == 'all':
                        # deselect 'all' but keep other selection
                        listbox.selection_clear(i)
    
    # save selection            
    def save_selection():
        # gather selected accounts
        selected = listbox.curselection()
        if not selected:
            error_account.config(text='Must select at least 1 account', background=bg_button)
            return
        else:
            error_account.config(text='', background=bg_common)
        
        # gather actual values - change list of indexes to actual values of those indexes
        selected_acc = [listbox.get(i) for i in selected]
        # save list as string
        selected_string = ', '.join(selected_acc)
        # save selcted accounts
        selected_account.set(selected_string)
        # shorten visual representation if too long (show on button)
        label_var.set(selected_string if len(selected_acc) <= 2 else ', '.join(selected_acc[:2]) + '...')
        
        if error_msg:
            error_msg.config(text='', background=bg_common)
        
        listbox.master.destroy()
        
    # display selection
    acc_dict = read_file()
    all_accounts = [acc for accounts in acc_dict.values() for acc in accounts]
    all_accounts.append('all') # add posibility to choose all accounts
    account_var = tk.Variable(value=tuple(all_accounts))
    
    listbox = create_listbox(toplevel, account_var, 'multiple', check_for_all)
    error_account = create_error_msg(toplevel)
    create_button(toplevel, 'Confirm', 10, 0, save_selection)

# select time period 
def choose_time(label_var):
###
# read txt file and create pandas table, keep only rows that have same account as chosen accounts from popup and date (create_table)
# creat treeview widget that saves dataframe object
# group data by account, make account 'parent' and rows of that account as 'children', so it becomes foldable
###
    toplevel = create_toplevel(main_frame, 220, 220)
    values = ['1 month', '3 months', '6 months', '9 months', '1 year', 'all time']
    time_var = tk.Variable(value=tuple(values))
    listbox = create_listbox(toplevel, time_var, 'single', lambda event: select_single_item(event, label_var))

# select date for new entry
def choose_date():
###
# create popup with calendar, choose the date with mouse click
# once selected, popup closes and selected date replaces today's date
###
    toplevel = create_toplevel(main_frame, 400, 280)
    create_text_widget(toplevel, 'label', 'Selected entry date', label_pady=20)
    calendar = Calendar(toplevel, selectmode='day', date_pattern='yyyy-mm-dd')
    calendar.pack()
    def show(e):
        selected_date.set(calendar.get_date())
        toplevel.destroy()
    calendar.bind('<<CalendarSelected>>', show)

# ------------ create new data 
# add new account
def add_new_account():
###
# open popup to input account which is saved to account txt as <input>-live
# before input go through the file and check if such account is already exist
###
    toplevel = create_toplevel(main_frame, 220, 200)
    create_text_widget(toplevel, 'label', 'Input new account', label_pady=15)
    entry = create_entry(toplevel)
    error_msg = create_error_msg(toplevel)
    
    def new_account():
        account = entry.get()
        # check if account input is not empty
        if not input_check(error_msg, 'missing', account, 'Input field cannot be empty'):
            return
        # check if same account already exist
        with open(account_file, 'r') as file:
            content = file.readlines()
            for line in content:
                line = line.strip().split('-')[0]
                if account == line:
                    error_msg.config(text='Such account already exist', background=bg_button)
                    return
        # write to file if not duplicate
        with open(account_file, 'a') as file:
            file.write(account + '-live' + '\n')
        toplevel.destroy()
        
    create_button(toplevel, 'Confirm', 15, 0, new_account)

# save new entry 
def save_entry(amount, text, error_amount, error_text, error_account, frame):
###
# takes data from widgets (saved account and inputs)
# transform the data: amount (split to state -/+ and format as float -> .00); 
#                     purpose (text to lowercase to not acidentaly make 2 seperate purposes Gift and gift - same, but code will think different)
# add inputs to txt, then reset window and replace widgets with empty ones
###
    # get selections
    account = selected_account.get()
    text = text.get().lower()
    # get amount in text form without spaces -> '- 20', '-20', ' - 20' becomes '-20'
    amount_text = amount.get().strip()
    
    # check if account is chosen
    if not input_check(error_account, 'missing', account, 'Account must be selected'):
        return
    # check if amount is not empty
    if not input_check(error_amount, 'missing', amount_text, 'Must input amount (format: 9999 OR -99.99 OR +9999.9)'):
        return
    # check if amount is correct form
    if not input_check(error_amount, 'number', amount_text, 'Input should be in format: 9999 OR 9999.99 OR -9999.9'):
        return
    # check if purpose is not empty
    if not input_check(error_text, 'missing', text, 'Must input source/destination (30 characters or less)'):
        return
    # check if purpose don't exceed 30 characters
    if not input_check(error_text, 'text', text, 'Text should be 30 characters or less'):
        return
    
    # add gain/spent variable depending on symbol +/-/nothing
    if amount_text.startswith('-'):
        state = '-'
        amount_text = amount_text[1:].strip() # save characters after 1-st element (-)
    elif amount_text.startswith('+'):
        state = '+'
        amount_text = amount_text[1:].strip()
    else:
        state = '+'
    amount_val = float(amount_text)
    
    # check if date is selected
    if selected_date.get() == 'None':
        date = datetime.datetime.now().strftime('%Y-%m-%d') # format as YYYY-MM-DD
    else:
        date = selected_date.get()
    
    # write into file
    output = f'{date}|{account}|{state}|{amount_val:.2f}|{text}' # 2025-07-11|bank|-|234.00|bought new tv
    with open(finance_file, 'a') as file:
        file.write(output + '\n')
    selected_account.set('Select Account')
    reset_window(window)
    create_entry_window(frame)
    
    # extende purpose list if new purpose input
    if text not in purpose_list:
        purpose_list.append(text)

# show purpose suggestion
def show_suggestion(frame, text):
###
# show list of all existing 'purpose' from the txt file
# clicking on suggestion inputs it into the entry field
# list auto-updates after each letter and checks for any match
###
    def hide(e):
        listbox.place_forget()
    
    # update showed values in listbox    
    def update_listbox(e):
        search = text.get().strip().lower()
        # check for entry match to all saved purpose list
        matches = [v for v in purpose_list if search in v.lower()] if search else []
        # if match found and on entry field
        if matches and text.focus_get() == text:
            # empty out the list
            listbox.delete(0, tk.END)
            for m in matches:
                # if match found insert to list
                listbox.insert(tk.END, m)
            # config height to how many suggestions found
            listbox.configure(height=len(matches))
            # place below entry and on top of other widgets
            x, y, w, h = text.winfo_x(), text.winfo_y(), text.winfo_width(), text.winfo_height()
            listbox.place(x=x, y=y+h, width=w)
            listbox.lift()
        else:
            listbox.place_forget()
        
    # replace entry input with suggestion
    def fill_entry(e):
        if listbox.curselection():
            selected = listbox.get(listbox.curselection()[0])
            text.delete(0, tk.END)
            text.insert(0, selected)
            listbox.place_forget()
    
    # create listbox and put directly below entry
    listbox = tk.Listbox(frame)
    listbox.configure(background=bg_text, foreground=fg_common, font=font_text)
    listbox.place_forget()
    
    # update list suggestions, hide when when not in focus, replace entry
    text.bind('<KeyRelease>', update_listbox)
    text.bind('<FocusOut>', hide)
    listbox.bind('<<ListboxSelect>>', fill_entry)

# export data 
def export_data(frame, type, name, error_account, error_name):
###
# export whole data (with total + current amounts) into .csv or .xlsx formats
# take file name and path, pass to to_excel or to_csv functions
###
    df = create_table()
    # drop signed_amount, only used for calculations
    df = df.drop('signed_amount', axis=1)
    file_name = name.get()
    
    # check
    if not check_selected_acc('display', error_account):
        return
    if not input_check(error_name, 'missing', file_name, 'File must have a name'):
        return

    # open file choosing window (where to save the file)
    file_dest = filedialog.askdirectory(title='Select folder to save file')
    if not file_dest:
        return
    
    file_path = os.path.join(file_dest, f'{file_name}.{type}')
    
    # export type based on which window opened
    if type == 'csv': 
        df.to_csv(file_path, index=False)
    else: 
        df.to_excel(file_path, index=False)
        
    selected_account_label.set('Select Accounts')
    selected_account.set('Select Account')
    selected_time.set('all time')
    reset_window(window)
    create_export_window(type, frame)

# ------------ display
# create overview table 
def display_table(error_account):
    if not check_selected_acc('display', error_account):
        return
    reset_window(window, 1100, 800)
    tree = ttk.Treeview(main_frame)
    tree['columns'] = ('date', 'gain/spent', 'amount', 'current amount', 'purpose')
    
    # display column names
    tree.heading('#0', text='account') # 'parent' column
    tree.heading('date', text='Date')
    tree.heading('gain/spent', text='Gain/Spent')
    tree.heading('amount', text='Amount')
    tree.heading('current amount', text='Current amount')
    tree.heading('purpose', text='Purpose')
    
    # config columns width
    tree.column('#0', width=170)
    tree.column('date', width=45)
    tree.column('gain/spent', width=40, anchor=tk.CENTER)
    tree.column('amount', width=65, anchor=tk.CENTER)
    tree.column('current amount', width=100, anchor=tk.CENTER)
    tree.column('purpose', width=310, anchor=tk.CENTER)
    
    # populate treeview grouped by account
    df = create_table()
    grouped_df = df.groupby('account')
    for account, group in grouped_df:
        total = group['amount'].sum()
        # input parent (account name) and total
        parent_id = tree.insert('', tk.END, text=f'{account} (Total: {total:.2f})', tag='account_row')
        # go through all rows based on account
        for _, row in group.iterrows():
            # insert values
            round(row['current_amount'], 2)
            tree.insert(parent_id, tk.END, values=(row['date'], row['symbol'], row['amount'], row['current_amount'], row['purpose']), tag='finance_row')
            
    tree.pack(expand=True, fill=tk.BOTH, selectmode=None)
    tree.tag_configure('account_row', background=bg_button, foreground=fg_button)
    tree.tag_configure('finance_row', background=bg_text, foreground=fg_common)

# create history graph 
def plot_graph(error_account):
###
# display scatter plot with connected lines of changing amount for selected accounts
# y axis - date, x axis - amount, each date is total amount at that moment
# example: 2025-02-16 +30.00, 2025-02-17 -20.00 -> 2025-02-16 = 30.00, 2025-02-17 = 10.00
###
    if not check_selected_acc('display', error_account):
        return
    reset_window(window, 900, 760)
    create_text_widget(main_frame, 'header', f'{selected_time.get()} history')
    
    # get values
    df = create_table()
    # create graph
    fig = Figure(figsize=(11, 7))
    fig.set_facecolor(bg_common) # color of background (not graph itself)
    ax = fig.add_subplot(111)
    ax.set_facecolor(bg_text) # color of graph
    
    scatter_plots = [] # need to store multiple accounts for hover
    for account, group in df.groupby('account'):
        x = group['date']
        y = group['current_amount']
        sc = ax.scatter(x, y, label=account, picker=True)
        ax.plot(x, y)
        scatter_plots.append((sc, group)) # append scatter plot and actual data
        
    # config plot
    ax.set_xlabel('Date')
    ax.set_ylabel('Amount')
    
    legend = ax.legend()
    legend.get_frame().set_facecolor(bg_text) # background color in legend
    legend.get_frame().set_edgecolor(fg_common) # border color (and text)
    
    ax.xaxis.set_major_locator(mdates.AutoDateLocator()) # how many dates to show dynamically (longer time - longer tick between date on x axis)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d')) # shows dates as YYYY-MM-DD
    fig.autofmt_xdate() # rotates dates to not overflow on each other
    # place canvas
    canvas = FigureCanvasTkAgg(fig, master=main_frame)
    canvas.draw()
    # create toolbar
    toolbar = NavigationToolbar2Tk(canvas, main_frame)
    toolbar.update()
    # anotation object (show data when hovering on point)
    ###
    # create empty annotation object that displays nothing and save every scatter point and their actual dataframes (for multiple accounts)
    # check if mouse hovering inside the plot, if yes, check if it is near any point
    # if mouse is near the point, go through every scatter plot and find close points
    # when mouse is on the point get the location of row in any scatter point and display annotation
    ###
    annot = ax.annotate('', xy=(0, 0), xytext=(-10, 20), textcoords='offset points', # put empty text placeholder, xy - starting point (the hover), xytext - where the text is (20 points out)
                        bbox = dict(boxstyle='round', fc=bg_text, edgecolor=fg_common), # background of annotation
                        arrowprops = dict(arrowstyle='->')) # show which point is hovered by pointing ->
    annot.set_visible(False)
    
    # update annotation
    def update_annot(sc, ind, group):
        # get coordinates of hovered object
        x, y = sc.get_offsets()[ind['ind'][0]] # get_offsets - get all scatter points (x, y), ind - the selected point
        # get values 
        date_str = group.iloc[ind['ind'][0]]['date'].strftime('%Y-%m-%d') # iloc - get row of the index
        amount = group.iloc[ind['ind'][0]]['current_amount']
        annot.xy = (x, y)
        # format and set text
        text = f'{date_str}\n{amount:.2f}'
        annot.set_text(text)
        
    # hover function
    def hover(event):
        # get current visibility (do annotation exist currently or not)
        vis = annot.get_visible()
        # if mouse point inside the plot
        if event.inaxes == ax:
            # go through all scatter points and actual data
            for sc, group in scatter_plots:
                # check if mouse is near a point in any scatter plot
                cont, ind = sc.contains(event)
                # if mouse is on the point
                if cont:
                    # get the annotation and draw it
                    update_annot(sc, ind, group)
                    annot.set_visible(True)
                    canvas.draw_idle()
                    return
        # if annotation was visible before (from earliear hover), hide it
        if vis:
            annot.set_visible(False)
            canvas.draw_idle()
            
    # connect hover function to plot
    canvas.mpl_connect('motion_notify_event', hover)
    # place toolbar
    canvas.get_tk_widget().pack()

# create pie chart 
def plot_chart(error_account):
###
# display 2 pie charts for 1 account, 1-st for spending, 2-nd for earning stacked vertically
# calculate total spending/earning and plot how much of total % is each reason (where spent/earnt the money)
# example: total spending is 1000, 300 is labeled as 'gift', 300 'job', 400 'hussle', chart will have 30% 'gift', 30% 'job', 40% 'hussle' in chart plot
###
    if not check_selected_acc('display', error_account):
        return
    reset_window(window, 740, 840)
    df = create_table()
    # label of what account chosen
    create_text_widget(main_frame, 'header', f'{selected_account.get()} earning/spending', header_pady=15)

    # find total spending/earning
    total_earning = df[df['symbol'] == '+']['amount'].sum()
    total_spending = df[df['symbol'] == '-']['amount'].sum()
    
    # custom label
    def custom_label(window_frame, text, color):
        frame = ttk.Frame(window_frame)
        frame.pack(pady=15)
        label = ttk.Label(frame, text=text, style='chart.TLabel', foreground=color)
        label.pack(fill='x')
        return frame
    
    # figure
    def create_chart(symbol, total_value):
        # purposes and their % from total 
        percent = df[df['symbol'] == symbol].groupby('purpose')['amount'].sum() # group all +/- rows by purpose and sum all amounts for each purpose
        labels = [f'{purposes}\n({value:.2f})' for purposes, value in zip(percent.index, percent)] # group purpose text and total value of slice
        fig = Figure(figsize=(6, 2))
        fig.set_facecolor(bg_text)
        ax = fig.add_subplot(111)
        _, label, autotext = ax.pie(percent, labels=labels, autopct='%1.2f%%', labeldistance=1.2)
        return fig, label, autotext
    
    # earning pie 
    frame_pos = custom_label(main_frame, f'Earnings (Total: {total_earning:.2f})', '#31ffd2')
    frame_pos.pack(fill='y', expand=True)
    # figure
    fig_pos, _, autotext_pos = create_chart('+', total_earning)
    
    # spending pie
    frame_neg = custom_label(main_frame, f'Spendings (Total: -{total_spending:.2f})', '#ffa1a1')
    frame_neg.pack(fill='y', expand=True)
    fig_neg, _, autotext_neg = create_chart('-', total_spending)
    
    # bold %
    for a in autotext_pos:
        a.set_fontweight('bold')
    for a in autotext_neg:
        a.set_fontweight('bold')
        
    # build widgets
    canvas_poc = FigureCanvasTkAgg(fig_pos, master=frame_pos)
    canvas_neg = FigureCanvasTkAgg(fig_neg, master=frame_neg)
    canvas_poc.get_tk_widget().pack(fill='both', expand=True)
    canvas_neg.get_tk_widget().pack(fill='both', expand=True)

# _________________________________ WINDOW UI _________________________________
# entry UI
def create_entry_window(frame):
    reset_window(window)

    # reset date selection on refresh
    if selected_date != 'None':
        selected_date.set(None)

    if not check_selected_acc('entry'):
        return

    # header
    create_text_widget(frame, 'header', 'New Entry')

    # account choice
    create_text_widget(frame, 'label', 'Choose account')
    button_frame = ttk.Frame(frame) # to position account buttons in row
    button_frame.pack(pady=5)
    error_account = create_error_msg(frame)

    # buttons for account action and date (custom)
    date = ttk.Button(button_frame, image=calendar_icon, command=choose_date, width=4, compound='center')
    date.pack(side=tk.LEFT, padx=0, pady=0)
    account = ttk.Button(button_frame, textvariable=selected_account, command=lambda: load_account_single(selected_account, error_account), width=15) # left button
    account.pack(side=tk.LEFT, padx=0, pady=0)
    add_account = ttk.Button(button_frame, text='+', command=add_new_account, width=4) # right button
    add_account.pack(side=tk.LEFT, padx=0, pady=0)

    # amount field
    create_text_widget(frame, 'label', 'Input amount', 10)
    amount = create_entry(frame)
    error_amount = create_error_msg(frame)

    # purpose (text field)
    create_text_widget(frame, 'label', 'Gain source / Spent destination', 10)
    text = create_entry(frame)
    show_suggestion(frame, text)
    error_text = create_error_msg(frame)

    # activation button
    create_button(frame, 'Save', 15, 15, lambda: save_entry(amount, text, error_amount, error_text, error_account, frame))

# overview UI
def create_overview_window(frame):
    reset_window(window)
    if not check_selected_acc('overview'):
        return
        
    # header
    create_text_widget(frame, 'header', 'Finance Overview')
    # account choice
    create_text_widget(frame, 'label', 'Choose accounts', 20)
    create_button(frame, None, 5, None, lambda: multi_choice_account(selected_account_label, error_account), selected_account_label)
    error_account = create_error_msg(frame)

    # date
    create_text_widget(frame, 'label', 'Choose time period', 30)
    create_button(frame, None, 0, 0, lambda: choose_time(selected_time), selected_time)
    
    # button to activate
    create_button(frame, 'Show', 20, 44, lambda: display_table(error_account))

# history UI
def create_history_window(frame):
    reset_window(window)
    if not check_selected_acc('history'):
        return
        
    # header
    create_text_widget(frame, 'header', 'Finance History', 20)
    
    # account choice
    create_text_widget(frame, 'label', 'Choose account')
    create_button(frame, None, 5, None, lambda: multi_choice_account(selected_account_label, error_account), selected_account_label)
    error_account = create_error_msg(frame)
    
    # date choice
    create_text_widget(frame, 'label', 'Choose time period', 30)
    create_button(frame, None, 0, 0, lambda: choose_time(selected_time), selected_time)
    
    # button to activate
    create_button(frame, 'Plot', 20, 44, lambda: plot_graph(error_account))

# chart UI
def create_chart_window(frame):
    reset_window(window)
    if not check_selected_acc('chart'):
        return
        
    # header
    create_text_widget(frame, 'header', 'Earning/Spending chart', 20)
    
    # account choice
    create_text_widget(frame, 'label', 'Choose account')
    create_button(frame, None, 5, None, lambda: load_account_single(selected_account, error_account), selected_account)
    error_account = create_error_msg(frame)
    
    # date choice
    create_text_widget(frame, 'label', 'Choose time period', 30)
    create_button(frame, None, 0, 0, lambda: choose_time(selected_time), selected_time)
    
    # button to activate
    create_button(frame, 'Plot', 20, 44, lambda: plot_chart(error_account))

# export UI
def create_export_window(file_type, frame):
    reset_window(window)
    if not check_selected_acc('export'):
        return
        
    # choose text based on menu selection
    if file_type == 'csv':
        text_choice = 'Export to CSV'
        button_choice = 'Save to CSV'
    elif file_type == 'xlsx':
        text_choice = 'Export to xlsx'
        button_choice = 'Save to xlsx'
        
    # header
    create_text_widget(frame, 'header', text_choice, 0)

    # account choice
    create_text_widget(frame, 'label', 'Choose account')
    create_button(frame, None, 5, None, lambda: multi_choice_account(selected_account_label, error_account), selected_account_label)
    error_account = create_error_msg(frame)
    
    # date choice
    create_text_widget(frame, 'label', 'Choose time period', 10)
    create_button(frame, None, 0, 0, lambda: choose_time(selected_time), selected_time)
    
    # file name
    create_text_widget(frame, 'label', 'Name the file', 18)
    name = create_entry(frame)
    error_name = create_error_msg(frame)
    
    # activation button
    create_button(frame, button_choice, 15, 15, lambda: export_data(frame, file_type, name, error_account, error_name))

# menu
def create_menu_window(frame):
    menu = tk.Menu(window)
    window.config(menu=menu)

    # main submenu
    file_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label='Window', menu=file_menu)
    # submenu choices
    file_menu.add_command(label='New', command=lambda: create_entry_window(frame))
    file_menu.add_command(label='Overview', command=lambda: create_overview_window(frame))
    file_menu.add_command(label='History', command=lambda: create_history_window(frame))
    file_menu.add_command(label='Chart', command=lambda: create_chart_window(frame))

    # export submenu
    export_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label='Export', menu=export_menu)
    export_menu.add_command(label='To CSV', command=lambda: create_export_window('csv', frame))
    export_menu.add_command(label='To xlsx', command=lambda: create_export_window('xlsx', frame))

    # help submenu
    # help_menu = tk.Menu(menu)
    # menu.add_cascade(label='Help', menu=help_menu)
    # help_menu.add_command(label='Files')
    # help_menu.add_command(label='New entry')
    # help_menu.add_command(label='Overview')
    # help_menu.add_command(label='History')
    # help_menu.add_command(label='Chart')
    # help_menu.add_command(label='Export')
    
# _________________________________ INITIATE APP _________________________________
# check if files exist
if not os.path.exists(finance_file):
    with open(finance_file, 'w') as file:
        file.write('date|account|symbol|amount|purpose' + '\n')
if not os.path.exists(account_file):
    with open(account_file, 'a') as file:
        pass

# create purpose suggestion list
if os.path.exists(finance_file):
    purpose_list = make_purpose_list()

# create app
set_window(window, 600, 600, reposition=True)
main_frame = tk.Frame(window, background=bg_common)
main_frame.pack(fill='both', expand='True')
create_menu_window(main_frame)
create_entry_window(main_frame)
window.mainloop()