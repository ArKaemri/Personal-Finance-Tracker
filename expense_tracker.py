# ------------------------- dependencies -------------------------
import tkinter as tk
from tkinter import ttk

# ------------------------- app initialisation -------------------------
# app instance
window = tk.Tk(className='expense tracker')

# size of tkinter window
w = 800
h = 800
# common colors
bg_common = '#626262'
fg = 'white'
bg_passive = '#7d7d7d'
bg_active = "#999999"

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
        
# ------------------------- entry UI -------------------------
# add entry window
def create_entry():
    # delete widgets on the screen
    reset_window()
    # label of the window
    header = tk.Label(main_frame, text='New Entry', font=('System', 26))
    header.pack(pady=20)
    # acount choice, currently just UI element
    acounts = ttk.Combobox(main_frame, values=['temp1', 'temp2'], font=('System', 18))
    acounts.pack(pady=50)
    acounts.current(0) # default option, 1-st from the list
    # amount input field
    amount = tk.Entry(main_frame, selectbackground='white', selectforeground='black', font=('System', 18))
    amount.pack(pady=50)
    # source/desination input field
    text = tk.Entry(main_frame, selectbackground='white', selectforeground='black', font=('System', 18))
    text.pack(pady=50)
    # activation button - save to txt file
    button = tk.Button(main_frame, text='Save', activebackground='white', activeforeground='black', font=('System', 18))
    button.pack(pady=20)
    
# ------------------------- overview UI -------------------------
def create_overview():
    reset_window()
    # label of the window
    header = tk.Label(main_frame, text='Finance Overview', font=('System', 26))
    header.pack(pady=20)
    # account choice
    acounts = ttk.Combobox(main_frame, values=['temp1', 'temp2'], font=('System', 18))
    acounts.pack(pady=80)
    acounts.current(0)
    # spacer to position button
    spacer = tk.Frame(main_frame, height=200)
    spacer.pack()
    # button to activate
    button = tk.Button(main_frame, text='Show', activebackground='white', activeforeground='black', font=('System', 18))
    button.pack(pady=20)
    
# ------------------------- history UI -------------------------
def create_history():
    reset_window()
    # label of the window
    header = tk.Label(main_frame, text='Finance History', font=('System', 26))
    header.pack(pady=20)
    # account choice
    acounts = ttk.Combobox(main_frame, values=['temp1', 'temp2'], font=('System', 18))
    acounts.pack(pady=60)
    acounts.current(0)
    # date choice - currently just UI 
    date = ttk.Combobox(main_frame, values=['1 month', '3 months'], font=('System', 18))
    date.pack(pady=60)
    date.current(0)
    # spacer to position button
    spacer = tk.Frame(main_frame, height=100)
    spacer.pack()
    # button to activate
    button = tk.Button(main_frame, text='Plot', activebackground='white', activeforeground='black', font=('System', 18))
    button.pack(pady=20)
    
# ------------------------- chart UI -------------------------
def create_chart():
    reset_window()
    # label of the window
    header = tk.Label(main_frame, text='Earning/Spending Chart', font=('System', 26))
    header.pack(pady=20)
    # account choice
    acounts = ttk.Combobox(main_frame, values=['temp1', 'temp2'], font=('System', 18))
    acounts.pack(pady=80)
    acounts.current(0)
    # spacer to position button
    spacer = tk.Frame(main_frame, height=200)
    spacer.pack()
    # button to activate
    button = tk.Button(main_frame, text='Plot', activebackground='white', activeforeground='black', font=('System', 18))
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
    header = tk.Label(main_frame, text=text_choice, font=('System', 26))
    header.pack(pady=30)
    # file name input field
    name = tk.Entry(main_frame, selectbackground='white', selectforeground='black', font=('System', 18))
    name.pack(pady=30)
    # file destination input field
    destination = tk.Entry(main_frame, selectbackground='white', selectforeground='black', font=('System', 18))
    destination.pack(pady=30)
    # acount choice, currently just UI element
    acounts = ttk.Combobox(main_frame, values=['temp1', 'temp2'], font=('System', 18))
    acounts.pack(pady=30)
    acounts.current(0)
    # date choice - currently just UI 
    date = ttk.Combobox(main_frame, values=['1 month', '3 months'], font=('System', 18))
    date.pack(pady=30)
    date.current(0)
    # activation button - save to txt file
    button = tk.Button(main_frame, text=button_choice, activebackground='white', activeforeground='black', font=('System', 18))
    button.pack(pady=20)

# ------------------------- initiate the app -------------------------
# call starting window to have content
create_entry()
# run whole app
window.mainloop()