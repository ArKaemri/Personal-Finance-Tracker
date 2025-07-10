# ------------------------- dependencies -------------------------
import datetime
import pandas as pd
import os
import re
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.font as tkfont
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# ------------------------- app initialisation -------------------------
# app instance
window = tk.Tk(className='Expense tracker')

# keep acount choice (and for visual change on button) - single acount (for multiple used to only store acount choices)
selected_label = tk.StringVar()
selected_label.set('Select Account')

selected_labels = tk.StringVar()
selected_labels.set('Select Accounts')

selected_date = tk.StringVar()
selected_date.set('all time')

# size of tkinter window
w = 600
h = 600
# common variables
bg_back = "#aaaaaa"
bg_common = "#d4d4d4"
fg_common = 'black'
fg_button = 'white'
bg_button = '#85929b'
bg_selected = "#777777"
error = '#ffb5b5'

font_header = tkfont.Font(family='DejaVu Sans', size=-36, weight='bold')
font_label = tkfont.Font(family='DejaVu Sans', size=-22, weight='bold')
font_text = tkfont.Font(family='DejaVu Sans', size=-16)
font_entry = tkfont.Font(family='DejaVu Sans', size=-16, weight='bold')
font_error = tkfont.Font(family='DejaVu Sans', size=-12, weight='bold')

style = ttk.Style()
style.theme_use('default')

# colors per widget
# frame / spacer
style.configure('TFrame',
                background = bg_back)
# treeview
style.configure('Treeview',
                background = bg_common,
                fieldbackground = bg_back,
                font = font_text)
style.configure('Treeview.Heading',
                background = bg_button,
                foreground=fg_button,
                font = font_text)
style.map('Treeview.Heading',
          background=[('active', bg_button)])
# change selected component color
style.map('Treeview',
          background=[('selected', bg_selected)],
          foreground=[('selected', fg_button)])
# entry
style.configure('TEntry',
                fieldbackground = bg_common,
                foreground = fg_common,
                padding = 5)
# button
style.configure('TButton',
                background = bg_button,
                foreground = fg_button,
                font = font_entry,
                padding = (4, 8))
style.map('TButton',
          background = [('active', bg_common)],
          foreground = [('active', fg_common)])
# disable dotted line when button pressed
window.option_add('*TButton*takeFocus', 0)
# label
style.configure('field.TLabel',
                background = bg_back,
                foreground = fg_button,
                font = font_label)
# header
style.configure('header.TLabel',
                background = bg_back,
                foreground = fg_button,
                font = font_header)
# chart header
style.configure('chart.TLabel',
                background = bg_button,
                foreground = fg_button,
                font = font_label,
                padding = 2)

# get width/height of the screen
screen_w = window.winfo_screenwidth()
screen_h = window.winfo_screenheight()

# get coordinates of windows bottom left corner, to place it in middle
### 
# divide whole screen in 2 - point at middle of the screen
# then move half of actual app to the left - get most left point (do same with height)
# start building app from gotten point (left-bottom pixel), app border goes right for width, up for height (app centered)
###
x = (screen_w / 2) - (w / 2)
y = (screen_h / 2) - (h / 2)

# setup size and placement
# x - multiply, %d - placeholder, % () - replacement in order
window.geometry('%dx%d+%d+%d' % (w, h, x, y))

# ------------------------- close app with Esc -------------------------
# close window by passing variable
def close_window(e):
    window.destroy()
    
# pass Esc key as variable for function
window.bind('<Escape>', lambda e: close_window(e))

# ------------------------- main frame -------------------------
# create empty frame where widgets will appear
main_frame = tk.Frame(window, background=bg_back)
# position it to whole space
main_frame.pack(fill='both', expand='True')

# ------------------------- reload window -------------------------
# goes through all widgets of parent and erases them
def reset_window(width=600, height=600):
    w = width
    h = height
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = (screen_w / 2) - (w / 2)
    y = (screen_h / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    for widget in main_frame.winfo_children():
        widget.destroy()

# ------------------------- load acounts (single) -------------------------
# global var to display chosen acount on button that opens choice menu
# create new window with selections
###
# on button open new window for acounts selection using listbox
# read acount txt file and split them in acount and class (account1-live \n acount2-live -> {'live':[acount1, acount2]})
# put acounts in the listbox and activate script (saving selection) after clicking on acount + close the popup
###
def load_acount_single(label_var):
    # function to select item from listbox
    def select_item(event):
        # get the widget
        listbox = event.widget
        # get the selection (returns indexes of selection - choosing 2-nd acount gives '1')
        selected = listbox.curselection()
        # if selecting empty space or similar, don't react
        if not selected:
            return
        # retrieve selection values (take first element from indexes list, becouse selected only 1 items)
        index = selected[0]
        selected_value = listbox.get(index) # actual value from index position
        # set global selected acount label (change button text to see what's selected and write to txt)
        label_var.set(selected_value)
        # close the popup
        listbox.master.destroy()
        
    top_w = 220
    top_h = 220
    # create and position window
    toplevel = tk.Toplevel(main_frame)
    toplevel.configure(background=bg_back)
    top_sw = toplevel.winfo_screenwidth()
    top_hw = toplevel.winfo_screenheight()
    top_x = (top_sw / 2) - (top_w / 2)
    top_y = (top_hw / 2) - (top_h / 2)
    toplevel.geometry('%dx%d+%d+%d' % (top_w, top_h, top_x, top_y))
    # read data from txt and write to dictionary
    acc_dict = {}
    # read file line by line
    with open('acounts_test.txt') as file:
        for line in file:
            # delete \n
            line = line.strip()
            # divide into account name and class (in file acc-class)
            value, key = line.split('-')
            # add all values with same key as a list to that key - {'key':[a, b, c]}
            acc_dict.setdefault(key, []).append(value)
    # create listbox
    # flatten all values into 1 list - {'key1':[a, b], 'key2':[c, d]} -> [a, b, c, d]
    all_acounts = [acc for acounts in acc_dict.values() for acc in acounts]
    # convert to tuple and add as listbox variables
    acount_var = tk.Variable(value=tuple(all_acounts))
    # create listbox widget
    listbox = tk.Listbox(toplevel, listvariable=acount_var, selectmode=tk.SINGLE)
    listbox.pack()
    # colors
    listbox.configure(background=bg_common, foreground=fg_common, font=font_text)
    # select an item from list (activate immediately after click)
    listbox.bind('<<ListboxSelect>>', select_item)
    # prevent from opening more windows
    toplevel.grab_set()
    
# ------------------------- save entry inputs -------------------------
###
# takes data from widgets (saved acount and inputs)
# transform the data: amount (split to state -/+ and format .00); 
#                     purpose (text to lowercase to not acidentaly make 2 seperate purposes Gift and gift - same, but code will think different)
# add inputs to txt, then reset window and replace widgets with empty ones
###
def save_entry(amount, text, er_amount, er_text, er_acount):
    # get selected acount
    acount = selected_label.get()
    # get and lowercase text
    text = text.get().lower()
    # get the date of input
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    # get the direction (spent or gain money)
    # get amount in text form without spaces - '- 20', '-20', ' - 20' -> '-20' (prevent problems from different input)
    amount_text = amount.get().strip()
    # check if acount is chosen
    if acount == 'Select Account':
        er_acount.config(text='Must select account', background=bg_button)
        return
    else:
        er_acount.config(text='', background=bg_back)
    # check if amount is not empty
    if amount_text == '':
        er_amount.config(text='Must input amount (format: +00 OR 00.00 OR -00.0)', background=bg_button)
        return
    else:
        er_amount.config(text='', background=bg_back)
    # check if amount is numeric
    if not re.match(r'^[+-]?\d+(\.\d{1,2})?$', amount_text):
        er_amount.config(text='Input should be in format: +00 OR 00.00 OR -00.0', background=bg_button)
        return
    else:
        er_amount.config(text='', background=bg_back)
    # check if purpose not empty
    if text == '':
        er_text.config(text='Must input source/destination (30 characters or less)', background=bg_button)
        return
    else:
        er_text.config(text='', background=bg_back)
    # check if purpose is not longer than 30 characters
    if len(text) >= 31:
        er_text.config(text='Text should be 30 characters or less', background=bg_button)
        return
    else:
        er_text.config(text='', background=bg_back)
    # add gain/spent variable depending on symbol +/-/nothing
    if amount_text.startswith('-'):
        state = '-'
        amount_text = amount_text[1:].strip() # save characters after 1-st element (-)
    elif amount_text.startswith('+'):
        state = '+'
        amount_text = amount_text[1:].strip()
    else:
        state = '+'
    # convert amount text to number (float)
    amount_val = float(amount_text)
    # write into file
    output = f'{date}|{acount}|{state}|{amount_val:.2f}|{text}'
    with open('finance_test.txt', 'a') as file:
        file.write('\n' + output)
    # reset window
    selected_label.set('Select Account')
    reset_window()
    create_entry()
    
# ------------------------- add acount -------------------------
###
# on button open popup to input acount which is saved to acount txt as <input>-live
###
def add_new_acount():
    # create popup
    toplevel = tk.Toplevel(main_frame)
    toplevel.configure(background=bg_back)
    top_w = 220
    top_h = 200
    top_sw = toplevel.winfo_screenwidth()
    top_sh = toplevel.winfo_screenheight()
    top_x = (top_sw / 2) - (top_w / 2)
    top_y = (top_sh / 2) - (top_h / 2)
    toplevel.geometry('%dx%d+%d+%d' % (top_w, top_h, top_x, top_y))
    # add entry
    new_label = ttk.Label(toplevel, text='Input new account', style='field.TLabel')
    new_label.pack(pady=15)
    new_entry = ttk.Entry(toplevel, font=font_entry)
    new_entry.pack(pady=5)
    error_msg = ttk.Label(toplevel, text='', font=font_error, foreground=error, background=bg_back)
    error_msg.pack()
    # entry function
    def new_acount():
        # get variable from entry
        acount = new_entry.get()
        # if input empty, show error
        if acount == '':
            error_msg.config(text='Input field cannot be empty', background=bg_button)
            return
        # if variable exist in file, show error
        with open('acounts_test.txt', 'r') as file:
            content = file.readlines()
            for line in content:
                line = line.strip().split('-')[0]
                if acount == line:
                    error_msg.config(text='Such account already exists', background=bg_button)
                    return
        # write to file
        with open('acounts_test.txt', 'a') as file:
            file.write('\n' + acount + '-live')
        # close popup
        toplevel.destroy()
    # add confirm button
    new_button = ttk.Button(toplevel, text='Confirm', command=new_acount, style='TButton', width=15)
    new_button.pack(pady=20)
    toplevel.grab_set()

# ------------------------- entry UI -------------------------
###
# create and display widgets for entry window (add new information to finance.txt)
###
# add entry window
def create_entry():
    # delete widgets on the screen
    reset_window()
    # entry only takes 1 account, if previously more selected, reset it, otherwise - persist
    if len(selected_label.get().split(',')) >= 2:
        selected_label.set('Select Account')
    # label of the window
    header = ttk.Label(main_frame, text='New Entry', style='header.TLabel')
    header.pack(pady=30)
    # acount choice, currently just UI element
    acounts_label = ttk.Label(main_frame, text='Choose acount', style='field.TLabel')
    acounts_label.pack(pady=10)
    button_frame = ttk.Frame(main_frame) # to position acount buttons in row
    button_frame.pack(pady=5)
    error_acount = ttk.Label(main_frame, text='', font=font_error, background=bg_back, foreground=error)
    error_acount.pack()
    acounts = ttk.Button(button_frame, textvariable=selected_label, command=lambda: load_acount_single(selected_label), width=15)
    acounts.pack(side=tk.LEFT, padx=0, pady=0)
    add_acount = ttk.Button(button_frame, text='+', command=add_new_acount, width=4)
    add_acount.pack(side=tk.LEFT, padx=0, pady=0)
    # spacer to put gap between widgets
    spacer1 = ttk.Frame(main_frame, height=30)
    spacer1.pack()
    # amount input field
    amount_label = ttk.Label(main_frame, text='Input amount', style='field.TLabel')
    amount_label.pack(pady=10)
    amount = ttk.Entry(main_frame, font=font_entry)
    amount.pack(pady=5)
    error_amount = ttk.Label(main_frame, text='', font=font_error, background=bg_back, foreground=error)
    error_amount.pack()
    spacer2 = ttk.Frame(main_frame, height=30)
    spacer2.pack()
    # source/desination input field
    purpose_label = ttk.Label(main_frame, text='Gain source / spent destination', style='field.TLabel')
    purpose_label.pack(pady=10)
    text = ttk.Entry(main_frame, font=font_entry)
    text.pack(pady=5)
    error_text = ttk.Label(main_frame, text='', font=font_error, background=bg_back, foreground=error)
    error_text.pack()
    spacer3 = ttk.Frame(main_frame, height=20)
    spacer3.pack()
    # activation button - save to txt file
    button = ttk.Button(main_frame, command=lambda: save_entry(amount, text, error_amount, error_text, error_acount), text='Save', width=15)
    button.pack(pady=20)
    
# ------------------------- multi-choice acount select -------------------------
###
# same as load_acount_single, but choose acounts on button press (not on mouse click) and can choose multiple choices
###
def multi_choice_acount(label_var):
    # create popup
    toplevel = tk.Toplevel(main_frame)
    toplevel.configure(background=bg_back)
    top_w = 220
    top_h = 260
    top_sw = toplevel.winfo_screenwidth()
    top_sh = toplevel.winfo_screenheight()
    top_x = (top_sw / 2) - (top_w / 2)
    top_y = (top_sh / 2) - (top_h / 2)
    toplevel.geometry('%dx%d+%d+%d' % (top_w, top_h, top_x, top_y))
    # save selected acounts
    def save_selection():
        # gather selected acounts
        selected = listbox.curselection()
        if not selected:
            return ''
        # gather actual values - change list of indexes to actual values of those indexes
        selected_acounts = [listbox.get(i) for i in selected]
        # save list as string
        selected_list = ', '.join(selected_acounts)
        # save selected acounts (all of them, passed for creating table)
        selected_label.set(selected_list)
        # shorten visual representation if too long (show on button)
        label_var.set(selected_list if len(selected_acounts) <= 2 else ', '.join(selected_acounts[:2]) + '...')
        # close window 
        listbox.master.destroy()
    # display selection
    acc_dict = {}
    with open('acounts_test.txt', 'r') as file:
        for line in file:
            line = line.strip()
            value, key = line.split('-')
            acc_dict.setdefault(key, []).append(value)
    all_acounts = [acc for acounts in acc_dict.values() for acc in acounts]
    all_acounts.append('all') # add posibility to choose all acounts from list
    acount_var = tk.Variable(value=tuple(all_acounts))
    listbox = tk.Listbox(toplevel, listvariable=acount_var, selectmode=tk.MULTIPLE)
    listbox.pack()
    listbox.configure(background=bg_common, foreground=fg_common, font=font_text, selectbackground=bg_selected, selectforeground=fg_button)
    button = ttk.Button(toplevel, text='Confirm', command=save_selection, width=15)
    button.pack(pady=10)
    toplevel.grab_set()
    
# ------------------------- display pandas table -------------------------
###
# read txt file and create pandas table, keep only rows that have same acount as chosen acounts from popup and date (create_table)
# creat trieview widget that saves dataframe object
# group data by acount, make acount 'parent' and rows of that acount as 'children', so it becomes foldable
###
# choose time same as single account
def choose_time(label_var):
    def select_item(event):
        listbox = event.widget
        selected = listbox.curselection()
        if not selected: 
            return
        index = selected[0]
        selected_value = listbox.get(index)
        label_var.set(selected_value)
        listbox.master.destroy()
    top_w = 220
    top_h = 220
    toplevel = tk.Toplevel(main_frame)
    toplevel.configure(background=bg_back)
    top_sw = toplevel.winfo_screenwidth()
    top_hw = toplevel.winfo_screenheight()
    top_x = (top_sw / 2) - (top_w / 2)
    top_y = (top_hw / 2) - (top_h / 2)
    toplevel.geometry('%dx%d+%d+%d' % (top_w, top_h, top_x, top_y))
    values = ['1 month', '3 months', '6 months', '9 months', '1 year', 'all time']
    time_var = tk.Variable(value=tuple(values))
    listbox = tk.Listbox(toplevel, listvariable=time_var, selectmode=tk.SINGLE)
    listbox.pack()
    listbox.configure(background=bg_common, foreground=fg_common, font=font_text)
    listbox.bind('<<ListboxSelect>>', select_item)
    toplevel.grab_set()
    
# create pandas table filtered by acount
def create_table():
    # create dataframe
    df = pd.read_csv('finance_test.txt', sep='|')
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    # filter by acount
    def filter_acount(dataframe):
        acount_list = selected_label.get().split(',')
        acount_list = [acc.strip() for acc in acount_list]
        filtered_df = dataframe[dataframe['acount'].isin(acount_list)]
        return filtered_df
    # filter by time
    def filter_time(dataframe):
        date = selected_date.get()
        # calculate date (n month from the date of last input (not from current day))
        max_date = dataframe['date'].max().normalize()
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
            return dataframe
        else:
            min_date = dataframe['date'].min()
        filtered_df = dataframe[(dataframe['date'] >= min_date) & (dataframe['date'] <= max_date)]
        return filtered_df
    # add column for cumulative amount (how much amount is total at specific date)
    df['signed_amount'] = df.apply(lambda row: row['amount'] if row['symbol'] == '+' else -row['amount'], axis=1).apply(lambda x: round(x, 2))
    df['current_amount'] = df.groupby('acount')['signed_amount'].cumsum().apply(lambda x: round(x, 2))
    # get acount list for filter
    if selected_label.get() == 'all' and selected_date.get() == 'all time':
        df = df.copy()
        df['date'] = df['date'].dt.date
        return df
    elif selected_label.get() != 'all' and selected_date.get() == 'all time':
        # filter by acounts
        filtered_df = filter_acount(df)
        filtered_df = filtered_df.copy()
        filtered_df['date'] = filtered_df['date'].dt.date
        return filtered_df       
    elif selected_label.get() == 'all' and selected_date.get() != 'all time':
        # filter by acounts
        filtered_df = filter_time(df)
        filtered_df = filtered_df.copy()
        filtered_df['date'] = filtered_df['date'].dt.date
        return filtered_df  
    else:
        filtered_df = filter_acount(df)
        filtered_df = filter_time(filtered_df)
        filtered_df = filtered_df.copy()
        filtered_df['date'] = filtered_df['date'].dt.date
        return filtered_df
    
# display table in window
def display_table():
    reset_window(1100, 800)
    # create widget
    tree = ttk.Treeview(main_frame)
    tree['columns'] = ('date', 'gain/spent', 'amount', 'current amount', 'purpose')
    # display column names
    tree.heading('#0', text='acount')
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
    # populate treeview grouped by acount
    df = create_table()
    # group by acount
    grouped_df = df.groupby('acount')
    for acount, group in grouped_df:
        # get total
        total = group['amount'].sum()
        # input parent (acount name) and total
        parent_id = tree.insert('', tk.END, text=f'{acount} (Total: {total:.2f})', tag='account_row')
        # go through all rows based on acount
        for _, row in group.iterrows():
            # insert values
            round(row['current_amount'], 2)
            tree.insert(parent_id, tk.END, values=(row['date'], row['symbol'], row['amount'], row['current_amount'], row['purpose']), tag='finance_row')
    tree.pack(expand=True, fill=tk.BOTH, selectmode=None)
    tree.tag_configure('account_row', background=bg_button, foreground=fg_button)
    tree.tag_configure('finance_row', background=bg_common, foreground=fg_common)

# ------------------------- overview UI -------------------------
###
# create and display widgets for overview window (table of finance.txt file)
###
def create_overview():
    reset_window()
    # keep previous account choice if it is not multiple
    if selected_label.get() != 'Select Account':
        selected_labels.set(selected_label.get())
    elif selected_label.get() == 'Select Account' and selected_labels.get() != 'Select Acounts':
        selected_labels.set('Select Acounts')
    # label of the window
    header = ttk.Label(main_frame, text='Finance Overview', style='header.TLabel')
    header.pack(pady=20)
    spacer1 = ttk.Frame(main_frame, height=60)
    spacer1.pack()
    # account choice
    acounts_label = ttk.Label(main_frame, text='Choose acounts', style='field.TLabel')
    acounts_label.pack(pady=10)
    acounts = ttk.Button(main_frame, width=15, textvariable=selected_labels, command=lambda: multi_choice_acount(selected_labels))
    acounts.pack()
    spacer2 = ttk.Frame(main_frame, height=60)
    spacer2.pack()
    # date
    date_label = ttk.Label(main_frame, text='Choose time period', style='field.TLabel')
    date_label.pack(pady=10)
    date = ttk.Button(main_frame, textvariable=selected_date, command=lambda: choose_time(selected_date), width=15)
    date.pack()
    spacer2 = ttk.Frame(main_frame, height=100)
    spacer2.pack()
    # button to activate
    button = ttk.Button(main_frame, text='Show', command=display_table, width=15)
    button.pack(pady=30)
    
# ------------------------- plot history graph -------------------------
###
# display scatter plot with connected lines of changing amount for selected acounts
# y axis - date, x axis - amount, each date is total amount at that moment
# example: 2025-02-16 +30.00, 2025-02-17 - 20.00 -> 2025-02-16 = 30.00, 2025-02-17 = 10.00
###
def plot_graph():
    reset_window(900, 760)
    header = ttk.Label(main_frame, text=f'{selected_date.get()} history', style='header.TLabel')
    header.pack(pady=30)
    # get values
    df = create_table()
    # create graph
    fig = Figure(figsize=(9, 6))
    fig.set_facecolor(bg_back)
    ax = fig.add_subplot(111)
    ax.set_facecolor(bg_common)
    scatter_plots = [] # need to store multiple accounts for hover
    for acount, group in df.groupby('acount'):
        x = group['date']
        y = group['current_amount']
        sc = ax.scatter(x, y, label=acount, picker=True) # let interactive function (hover)
        ax.plot(x, y)
        scatter_plots.append((sc, group)) # append scatter plot and actual data
    # config plot
    ax.set_xlabel('Date')
    ax.set_ylabel('Amount')
    legend = ax.legend()
    legend.get_frame().set_facecolor(bg_common)
    legend.get_frame().set_edgecolor(fg_common)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
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
    # when mouse is on the point get the row of location in any scatter point and display annotation
    ###
    annot = ax.annotate('', xy=(0, 0), xytext=(20, 20), textcoords='offset points', # put empty text placeholder
                        bbox = dict(boxstyle='round', fc=bg_common, edgecolor=fg_common), # background of annotation
                        arrowprops = dict(arrowstyle='->')) # show which point is hovered
    annot.set_visible(False)
    # update annotation
    def update_annot(sc, ind, group):
        # get coordinates of hovered object
        x, y = sc.get_offsets()[ind['ind'][0]]
        # get date value 
        date_str = group.iloc[ind['ind'][0]]['date'].strftime('%Y-%m-%d')
        # get amount value
        amount = group.iloc[ind['ind'][0]]['current_amount']
        # get coordinates
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
        # if annotation was visible before (from earliear hover)
        if vis:
            annot.set_visible(False)
            canvas.draw_idle()
    # connect hover function to plot
    canvas.mpl_connect('motion_notify_event', hover)
    # place toolbar
    canvas.get_tk_widget().pack()

# ------------------------- history UI -------------------------
###
# create and display widgets for history window (matplotlib line graph of finance.txt)
###
def create_history():
    reset_window()
    # keep previous account choice if it is not multiple
    if selected_label.get() != 'Select Account':
        selected_labels.set(selected_label.get())
    elif selected_label.get() == 'Select Account' and selected_labels.get() != 'Select Acounts':
        selected_labels.set('Select Acounts')
    # label of the window
    header = ttk.Label(main_frame, text='Finance History', style='header.TLabel')
    header.pack(pady=20)
    spacer1 = ttk.Frame(main_frame, height=60)
    spacer1.pack()
    # account choice
    acounts_label = ttk.Label(main_frame, text='Choose acount', style='field.TLabel')
    acounts_label.pack(pady=10)
    acounts = ttk.Button(main_frame, width=15, textvariable=selected_labels, command=lambda: multi_choice_acount(selected_labels))
    acounts.pack()
    spacer2 = ttk.Frame(main_frame, height=60)
    spacer2.pack()
    # date choice - currently just UI 
    date_label = ttk.Label(main_frame, text='Choose time period', style='field.TLabel')
    date_label.pack(pady=10)
    date = ttk.Button(main_frame, textvariable=selected_date, command=lambda: choose_time(selected_date), width=15)
    date.pack()
    spacer3 = ttk.Frame(main_frame, height=100)
    spacer3.pack()
    # button to activate
    button = ttk.Button(main_frame, command=plot_graph, text='Plot', width=15)
    button.pack(pady=30)
    
# ------------------------- pie chart plot -------------------------
###
# display 2 pie charts for 1 acount, 1-st for spending, 2-nd for earning
# calculate total spending/earning and plot how much of total % is each reason (where spent/earnt the money)
###
def plot_chart():
    reset_window(740, 800)
    df = create_table()
    # label of what acount chosen
    header = ttk.Label(main_frame, text=f'{selected_label.get()} earning/spending', style='header.TLabel')
    header.pack(pady=15)
    # find total spending/earning
    total_earning = df[df['symbol'] == '+']['amount'].sum()
    total_spending = df[df['symbol'] == '-']['amount'].sum()
    # earning pie 
    # frame for 1 chart
    frame1 = ttk.Frame(main_frame)
    # frame1.pack(side='left', padx=10)
    frame1.pack(pady=15)
    # label with total
    label1 = ttk.Label(frame1, text=f'Earnings (Total: {total_earning:.2f})', style='chart.TLabel', foreground='#31ffd2')
    label1.pack(fill='x')
    # purposes and their % from total  
    percent1 = df[df['symbol'] == '+'].groupby('purpose')['amount'].sum()
    # figure
    fig1 = Figure(figsize=(7, 3))
    fig1.set_facecolor(bg_common)
    ax1 = fig1.add_subplot(111)
    _, purposes1, _ = ax1.pie(percent1, labels=percent1.index, autopct=lambda pct: f'{pct:.1f}%\n({pct * total_earning / 100:.2f})')
    # spending pie
    frame2 = tk.Frame(main_frame)
    # frame2.pack(side='right', padx=10)
    frame2.pack(pady=15)
    label2 = ttk.Label(frame2, text=f'Spendings (Total: -{total_spending:.2f})', style='chart.TLabel', foreground="#ffa1a1")
    label2.pack(fill='x')
    percent2 = df[df['symbol'] == '-'].groupby('purpose')['amount'].sum()
    fig2 = Figure(figsize=(7, 3))
    fig2.set_facecolor(bg_common)
    ax2 = fig2.add_subplot(111)
    _, purposes2, _ = ax2.pie(percent2, labels=percent2.index, autopct=lambda pct: f'{pct:.1f}%\n({pct * total_spending / 100:.2f})')
    # color labels white
    for p in purposes1:
        p.set_color(fg_common)
    for p in purposes2:
        p.set_color(fg_common)
    # finalise
    canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
    canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
    canvas1.get_tk_widget().pack()
    canvas2.get_tk_widget().pack()
 
# ------------------------- chart UI -------------------------
###
# create and display widgets for chart window (matplotlib pie chart of finance.txt)
###
def create_chart():
    reset_window()
    # don't reset account choice if they correct for chart
    # chart only takes 1 account, if previously more selected, reset it, otherwise - persist
    if len(selected_label.get().split(',')) >= 2:
        selected_label.set('Select Account')
    # label of the window
    header = ttk.Label(main_frame, text='Earning/Spending Chart', style='header.TLabel')
    header.pack(pady=20)
    spacer1 = ttk.Frame(main_frame, height=60)
    spacer1.pack()
    # account choice
    acounts_label = ttk.Label(main_frame, text='Choose acount', style='field.TLabel')
    acounts_label.pack(pady=10)
    acounts = ttk.Button(main_frame, width=15, textvariable=selected_label, command=lambda: load_acount_single(selected_label))
    acounts.pack()
    spacer2 = ttk.Frame(main_frame, height=60)
    spacer2.pack()
    # date choice - currently just UI 
    date_label = ttk.Label(main_frame, text='Choose time period', style='field.TLabel')
    date_label.pack(pady=10)
    date = ttk.Button(main_frame, textvariable=selected_date, command=lambda: choose_time(selected_date), width=15)
    date.pack()
    spacer3 = ttk.Frame(main_frame, height=100)
    spacer3.pack()
    # button to activate
    button = ttk.Button(main_frame, command=plot_chart, text='Plot', width=15)
    button.pack(pady=30)

# ------------------------- export UI -------------------------
###
# export whole data (with cumulative + current amounts) into .csv or .xlsx formats
# take file name and path, pass to to_excel or to_csv functions
###
def export_data(type, name, er_acc, er_name):
    df = create_table()
    # drop signed_amount, only needed for calculations
    df = df.drop('signed_amount', axis=1)
    file_name = name.get()
    # check empty
    if selected_label.get() == 'Select Account':
        er_acc.config(text='Must select account[s]', background=bg_button)
        return
    else:
        er_acc.config(text='', background=bg_back)
    if file_name == '':
        er_name.config(text='Must input name', background=bg_button)
        return
    else:
        er_name.config(text='', background=bg_back)
    
    file_dest = filedialog.askdirectory(title='Select folder to save file')
    if not file_dest:
        return
    os.makedirs(file_dest, exist_ok=True)
    file_path = os.path.join(file_dest, f'{file_name}.{type}')
    print(file_path)
    
    if type == 'csv':
        df.to_csv(file_path, index=False)
    else:
        df.to_excel(file_path, index=False)
        
    reset_window()
    create_export(type)

# ------------------------- export UI -------------------------
###
# create and display widgets for export window (export finance.txt as .csv or .xlsx)
###
def create_export(file_type):
    # choose text based on menu selection
    if file_type == 'csv':
        text_choice = 'Export to CSV'
        button_choice = 'Save to CSV'
    elif file_type == 'xlsx':
        text_choice = 'Export to xlsx'
        button_choice = 'Save to xlsx'
    reset_window()
    # label of the window
    header = ttk.Label(main_frame, text=text_choice, style='header.TLabel')
    header.pack(pady=30)
    # acount choice, currently just UI element
    acounts_label = ttk.Label(main_frame, text='Choose acount', style='field.TLabel')
    acounts_label.pack(pady=10)
    acounts = ttk.Button(main_frame, width=15, textvariable=selected_labels, command=lambda: multi_choice_acount(selected_labels))
    acounts.pack(pady=5)
    error_acount = ttk.Label(main_frame, text='', font=font_error, background=bg_back, foreground=error)
    error_acount.pack()
    spacer1 = ttk.Frame(main_frame, height=30)
    spacer1.pack()
    # date choice - currently just UI 
    date_label = ttk.Label(main_frame, text='Choose time period', style='field.TLabel')
    date_label.pack(pady=10)
    date = ttk.Button(main_frame, textvariable=selected_date, command=lambda: choose_time(selected_date), width=15)
    date.pack()
    spacer2 = ttk.Frame(main_frame, height=30)
    spacer2.pack()
    # file name input field
    name_label = ttk.Label(main_frame, text='Name the file', style='field.TLabel')
    name_label.pack(pady=10)
    name = ttk.Entry(main_frame, font=font_entry)
    name.pack()
    error_name = ttk.Label(main_frame, text='', font=font_error, background=bg_back, foreground=error)
    error_name.pack()
    spacer3 = ttk.Frame(main_frame, height=30)
    spacer3.pack()
    # activation button - save to txt file
    button = ttk.Button(main_frame, command=lambda: export_data(file_type, name, error_acount, error_name), text=button_choice, width=15)
    button.pack(pady=11)

# ------------------------- create menu -------------------------
###
# create and display menu for changing windows
###
# create main menu (whole top bar where all options reside)
def create_menu():
    menu = tk.Menu(window)
    # set the menu
    window.config(menu=menu)

    # create submenu (seperate options that will have choices after clicked)
    file_menu = tk.Menu(menu, tearoff=0)
    # name it and add to the main menu
    menu.add_cascade(label='Window', menu=file_menu)
    # add seperate choices
    file_menu.add_command(label='New', command=create_entry)
    file_menu.add_command(label='Overview', command=create_overview)
    file_menu.add_command(label='History', command=create_history)
    file_menu.add_command(label='Chart', command=create_chart)

    # repeat with second submenu
    export_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label='Export', menu=export_menu)
    export_menu.add_command(label='To CSV', command=lambda: create_export('csv'))
    export_menu.add_command(label='To xlsx', command=lambda: create_export('xlsx'))

    # repeat with third submenu
    # help_menu = tk.Menu(menu)
    # menu.add_cascade(label='Help', menu=help_menu)
    # help_menu.add_command(label='Files')
    # help_menu.add_command(label='New entry')
    # help_menu.add_command(label='Overview')
    # help_menu.add_command(label='History')
    # help_menu.add_command(label='Chart')
    # help_menu.add_command(label='Export')

# ------------------------- initiate the app -------------------------
# call starting window to have content
create_menu()
create_entry()
# run whole app
window.mainloop()