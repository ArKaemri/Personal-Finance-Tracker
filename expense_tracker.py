# ------------------------- dependencies -------------------------
import tkinter as tk
from tkinter import ttk
import datetime
import pandas
# ------------------------- app initialisation -------------------------
# app instance
window = tk.Tk(className='Expense tracker')

# size of tkinter window
w = 800
h = 800
# common variables
bg_common = '#626262'
fg = 'white'
bg_passive = '#7d7d7d'
bg_active = '#999999'
relief = 'solid'

# get width/height of the screen
screen_w = window.winfo_screenwidth()
screen_h = window.winfo_screenheight()

# get coordinates of windows top left corner, to place it in middle
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

# ------------------------- create menu -------------------------
# create main menu (whole top bar where all options reside)
menu = tk.Menu(window)
# set the menu
window.config(menu=menu)

# create submenu (seperate options that will have choices after clicked)
file_menu = tk.Menu(menu)
# name it and add to the main menu
menu.add_cascade(label='Window', menu=file_menu)
# add seperate choices
file_menu.add_command(label='New')
file_menu.add_command(label='Overview')
file_menu.add_command(label='History')
file_menu.add_command(label='Chart')

# repeat with second submenu
export_menu = tk.Menu(menu)
menu.add_cascade(label='Export', menu=export_menu)
export_menu.add_command(label='To CSV')
export_menu.add_command(label='To xlsx')

# repeat with third submenu
help_menu = tk.Menu(menu)
menu.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(label='Files')
help_menu.add_command(label='New entry')
help_menu.add_command(label='Overview')
help_menu.add_command(label='History')
help_menu.add_command(label='Chart')
help_menu.add_command(label='Export')

# ------------------------- main frame -------------------------
# create empty frame where widgets will appear
main_frame = tk.Frame(window, background=bg_common)
# position it to whole space
main_frame.pack(fill='both', expand='True')

# ------------------------- reload window -------------------------
# goes through all widgets of parent and erases them
def reset_window():
    for widget in main_frame.winfo_children():
        widget.destroy()

# ------------------------- load acounts (single) -------------------------
# global var to display chosen acount on button that opens choice menu
# define acount for visual (and later to write into file)
selected_label = tk.StringVar()
selected_label.set('Select Acount')
# create new window with selections
def load_acount_single(label_var):
    # function to select item from listbox
    def select_item(event):
        # get the widget
        listbox = event.widget
        # get the selection
        selected = listbox.curselection()
        # if selecting empty space or similar, don't react
        if not selected:
            return
        # retrieve selection values
        index = selected[0]
        selected_value = listbox.get(index)
        # set global selected acount label (change button text to see what's selected and write to txt)
        label_var.set(selected_value)
        # close the popup
        listbox.master.destroy()
        
    top_w = 400
    top_h = 400
    # create and position window
    toplevel = tk.Toplevel(main_frame)
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
            # add all values with same key as a list to that key {'key':[a, b, c]}
            acc_dict.setdefault(key, []).append(value)
    # create listbox
    # flatten all values into 1 list
    all_acounts = [acc for acounts in acc_dict.values() for acc in acounts]
    # convert to tuple and add as listbox variables
    acount_var = tk.Variable(value=tuple(all_acounts))
    # create listbox widget
    listbox = tk.Listbox(toplevel, listvariable=acount_var, selectmode=tk.SINGLE)
    listbox.pack()
    # select an item from list
    listbox.bind('<<ListboxSelect>>', select_item)
    # prevent from opening more windows
    toplevel.grab_set()
    
# ------------------------- save entry inputs -------------------------
def save_entry(amount, text):
    # get selected acount
    acount = selected_label.get()
    # get and lowercase text
    text = text.get().lower()
    # get the date of input
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    # get the direction (spent or gain money)
    # get amount in text form without spaces
    amount_text = amount.get().strip()
    # add gain/spent variable depending on symbol +/-/nothing
    if amount_text.startswith('-'):
        state = 'spent'
        amount_text = amount_text[1:].strip()
    elif amount_text.startswith('+'):
        state = 'gain'
        amount_text = amount_text[1:].strip()
    else:
        state = 'gain'
    # convert amount text to number (float)
    amount_val = float(amount_text)
    # write into file
    output = f'{date}|{acount}|{state}|{amount_val:.2f}|{text}'
    with open('finance_test.txt', 'a') as file:
        file.write('\n' + output)
    # reset window
    selected_label.set('Select Acount')
    reset_window()
    create_entry()
    
# ------------------------- add acount -------------------------
def add_new_acount():
    # create popup
    toplevel = tk.Toplevel(main_frame)
    top_w = 200
    top_h = 200
    top_sw = toplevel.winfo_screenwidth()
    top_sh = toplevel.winfo_screenheight()
    top_x = (top_sw / 2) - (top_w / 2)
    top_y = (top_sh / 2) - (top_h / 2)
    toplevel.geometry('%dx%d+%d+%d' % (top_w, top_h, top_x, top_y))
    # add entry
    new_label = tk.Label(toplevel, text='Input new acount')
    new_label.pack()
    new_entry = tk.Entry(toplevel)
    new_entry.pack(pady=20)
    # entry function
    def new_acount():
        # get variable from entry
        acount = new_entry.get()
        # write to file
        with open('acounts_test.txt', 'a') as file:
            file.write('\n' + acount + '-live')
        # close popup
        toplevel.destroy()
    # add confirm button
    new_button = tk.Button(toplevel, text='Confirm', command=new_acount)
    new_button.pack()
    toplevel.grab_set()

# ------------------------- entry UI -------------------------
# add entry window
def create_entry():
    # delete widgets on the screen
    reset_window()
    # label of the window
    header = tk.Label(main_frame, text='New Entry', font=('System', 28), background=bg_common, foreground=fg)
    header.pack(pady=20)
    # spacer 
    spacer1 = tk.Frame(main_frame, height=80, background=bg_common)
    spacer1.pack()
    # acount choice, currently just UI element
    acounts_label = tk.Label(main_frame, text='Choose acount', background=bg_common, foreground=fg, font=('System', 18))
    acounts_label.pack(pady=5)
    acounts = tk.Button(main_frame, textvariable=selected_label, command=lambda: load_acount_single(selected_label), background=bg_common, foreground=fg)
    acounts.pack()
    add_acount = tk.Button(main_frame, text='+', command=add_new_acount, background=bg_passive, foreground=fg, activebackground=bg_active, activeforeground=fg)
    add_acount.pack()
    spacer2 = tk.Frame(main_frame, height=80, background=bg_common)
    spacer2.pack()
    # amount input field
    amount_label = tk.Label(main_frame, text='Input amount', background=bg_common, foreground=fg, font=('System', 18))
    amount_label.pack(pady=5)
    amount = tk.Entry(main_frame, border=2, relief=relief, background=bg_passive, foreground=fg, font=('System', 18))
    amount.pack()
    spacer3 = tk.Frame(main_frame, height=80, background=bg_common)
    spacer3.pack()
    # source/desination input field
    purpose_label = tk.Label(main_frame, text='Gain source / spent destination', background=bg_common, foreground=fg, font=('System', 18))
    purpose_label.pack(pady=5)
    text = tk.Entry(main_frame, border=2, relief=relief, background=bg_passive, foreground=fg, font=('System', 18))
    text.pack()
    spacer4 = tk.Frame(main_frame, height=80, background=bg_common)
    spacer4.pack()
    # activation button - save to txt file
    button = tk.Button(main_frame, command=lambda: save_entry(amount, text), text='Save', background=bg_passive, foreground=fg, activebackground=bg_active, activeforeground=fg, font=('System', 18))
    button.pack(pady=20)
    
# ------------------------- multi-choice acount select -------------------------
selected_labels = tk.StringVar()
selected_labels.set('Select Acounts')
from tkinter.messagebox import showinfo
def multi_choice_acount(label_var):
    # create popup
    toplevel = tk.Toplevel(main_frame)
    top_w = 400
    top_h = 400
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
            return
        selected_acounts = [listbox.get(i) for i in selected]
        selected_list = ', '.join(selected_acounts)
        selected_label = selected_list
        # shorten visual representation if too long
        label_var.set(selected_list if len(selected_acounts) <= 3 else ', '.join(selected_acounts[:2]) + '...')
        # close window 
        listbox.master.destroy()
        print(selected_label)
    # display selection
    acc_dict = {}
    with open('acounts_test.txt', 'r') as file:
        for line in file:
            line = line.strip()
            value, key = line.split('-')
            acc_dict.setdefault(key, []).append(value)
    all_acounts = [acc for acounts in acc_dict.values() for acc in acounts]
    acount_var = tk.Variable(value=tuple(all_acounts))
    listbox = tk.Listbox(toplevel, listvariable=acount_var, selectmode=tk.MULTIPLE)
    listbox.pack()
    button = tk.Button(toplevel, text='Confirm', command=save_selection)
    button.pack()
    toplevel.grab_set()
# ------------------------- display pandas table -------------------------
def display_table():
    return

# ------------------------- overview UI -------------------------
def create_overview():
    reset_window()
    selected_labels.set('Select Acounts')
    selected_label.set('Select Acount')
    # label of the window
    header = tk.Label(main_frame, text='Finance Overview', background=bg_common, foreground=fg, font=('System', 28))
    header.pack(pady=20)
    spacer1 = tk.Frame(main_frame, height=180, background=bg_common)
    spacer1.pack()
    # account choice
    acounts_label = tk.Label(main_frame, text='Choose acounts', background=bg_common, foreground=fg, font=('System', 18))
    acounts_label.pack(pady=5)
    acounts = tk.Button(main_frame, textvariable=selected_labels, command=lambda: multi_choice_acount(selected_labels), background=bg_common, foreground=fg)
    acounts.pack()
    spacer2 = tk.Frame(main_frame, height=300, background=bg_common)
    spacer2.pack()
    # button to activate
    button = tk.Button(main_frame, text='Show', command=display_table, background=bg_passive, foreground=fg, activebackground=bg_active, activeforeground=fg, font=('System', 18))
    button.pack(pady=20)
    
# ------------------------- history UI -------------------------
def create_history():
    reset_window()
    # label of the window
    header = tk.Label(main_frame, text='Finance History', foreground=fg, background=bg_common, font=('System', 28))
    header.pack(pady=20)
    spacer1 = tk.Frame(main_frame, height=100, background=bg_common)
    spacer1.pack()
    # account choice
    acounts_label = tk.Label(main_frame, text='Choose acount', background=bg_common, foreground=fg, font=('System', 18))
    acounts_label.pack(pady=5)
    acounts = ttk.Combobox(main_frame, values=['temp1', 'temp2'], font=('System', 18), state='readonly')
    acounts.pack()
    acounts.current(0)
    spacer2 = tk.Frame(main_frame, height=100, background=bg_common)
    spacer2.pack()
    # date choice - currently just UI 
    date_label = tk.Label(main_frame, text='Choose time period', background=bg_common, foreground=fg, font=('System', 18))
    date_label.pack(pady=5)
    date = ttk.Combobox(main_frame, values=['1 month', '3 months'], font=('System', 18), state='readonly')
    date.pack()
    date.current(0)
    spacer3 = tk.Frame(main_frame, height=200, background=bg_common)
    spacer3.pack()
    # button to activate
    button = tk.Button(main_frame, text='Plot', background=bg_passive, foreground=fg, activebackground=bg_active, activeforeground=fg, font=('System', 18))
    button.pack(pady=20)
    
# ------------------------- chart UI -------------------------
def create_chart():
    reset_window()
    # label of the window
    header = tk.Label(main_frame, text='Earning/Spending Chart', background=bg_common, foreground=fg, font=('System', 28))
    header.pack(pady=20)
    spacer1 = tk.Frame(main_frame, height=180, background=bg_common)
    spacer1.pack()
    # account choice
    acounts_label = tk.Label(main_frame, text='Choose acount', background=bg_common, foreground=fg, font=('System', 18))
    acounts_label.pack(pady=5)
    acounts = ttk.Combobox(main_frame, values=['temp1', 'temp2'], font=('System', 18), state='readonly')
    acounts.pack()
    acounts.current(0)
    spacer2 = tk.Frame(main_frame, height=300, background=bg_common)
    spacer2.pack()
    # button to activate
    button = tk.Button(main_frame, text='Plot', background=bg_passive, foreground=fg, activebackground=bg_active, activeforeground=fg, font=('System', 18))
    button.pack(pady=20)

# ------------------------- export UI -------------------------
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
    header = tk.Label(main_frame, text=text_choice, background=bg_common, foreground=fg, font=('System', 28))
    header.pack(pady=50)
    # acount choice, currently just UI element
    acounts_label = tk.Label(main_frame, text='Choose acount', background=bg_common, foreground=fg, font=('System', 18))
    acounts_label.pack(pady=5)
    acounts = ttk.Combobox(main_frame, values=['temp1', 'temp2'], font=('System', 18), state='readonly')
    acounts.pack()
    acounts.current(0)
    spacer1 = tk.Frame(main_frame, height=50, background=bg_common)
    spacer1.pack()
    # date choice - currently just UI 
    date_label = tk.Label(main_frame, text='Choose time period', background=bg_common, foreground=fg, font=('System', 18))
    date_label.pack(pady=5)
    date = ttk.Combobox(main_frame, values=['1 month', '3 months'], font=('System', 18), state='readonly')
    date.pack()
    date.current(0)
    spacer2 = tk.Frame(main_frame, height=50, background=bg_common)
    spacer2.pack()
    # file name input field
    name_label = tk.Label(main_frame, text='Name the file', background=bg_common, foreground=fg, font=('System', 18))
    name_label.pack(pady=5)
    name = tk.Entry(main_frame, border=2, relief=relief, background=bg_passive, foreground=fg, font=('System', 18))
    name.pack()
    spacer3 = tk.Frame(main_frame, height=50, background=bg_common)
    spacer3.pack()
    # file destination input field
    destination_label = tk.Label(main_frame, text='Where to save file', background=bg_common, foreground=fg, font=('System', 18))
    destination_label.pack(pady=5)
    destination = tk.Entry(main_frame, border=2, relief=relief, background=bg_passive, foreground=fg, font=('System', 18))
    destination.pack()
    spacer4 = tk.Frame(main_frame, height=50, background=bg_common)
    spacer4.pack()
    # activation button - save to txt file
    button = tk.Button(main_frame, text=button_choice, background=bg_passive, foreground=fg, activebackground=bg_active, activeforeground=fg, font=('System', 18))
    button.pack(pady=20)

# ------------------------- initiate the app -------------------------
# call starting window to have content
create_overview()
# run whole app
window.mainloop()