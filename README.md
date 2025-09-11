# Project introduction
This is minimal and simplistic finance tracking app, not equal to big apps with loads of functionality and cloud storage, it is just alternative for physical money spending/earning notepad, just with couple extra functions that works offline and keeps data locally and digitally. It is bundled in single executable that doesn't need installing or setting up, should work out of the box, on both, Linux and Windows.
# Quick info
- App uses 2 .txt files that are created automatically, when relocating app, relocate .txt aswell 
- Design is static, making it smaller/bigger may not look pretty
- App functionality: input new data, see table of all data, see history of change, spending/earning charts, export to csv/excel
- Input reason (last field in entry tab) is static, reasons 'bought groceries' and 'groceries' or even 'Bought groceries' are treated as different reasons
- Navigate through functionality by top bar (menu)
- Works offline
# Use manual
## Windows
Go to releases, download .exe file, put it into new folder (or any folder, but will create 2 new files, so 3 files in total), once clicked, it will open the GUI app and 2 .txt files will be created in same location. For start you should press '+' button on opened tab and input name of an account, after that press 'select account' and input all the data, this will put the info into files. After this the app is ready to use. (to use app by choosing from start menu, you need to pin it to start, just finding the name and clicking enter will cause error and won't start the app) 
## Linux
Same steps for linux, the only difference that app won't be found in start menu at all.
# Development manual
## Windows
Clone the repo into new location, then create virtual environment (libraries installed with pip and there is no computer vision packages so preferably use venv) and install the libraries from requirements.txt:
- Open terminal and navigate to the folder
- py -m venv .venv
- .venv\Scripts\activate
- pip install -r requirements.txt
- Launch app from running in code editor or running 'py finance_tracker.py' in terminal
## Linux
Same steps as for Windows, but different commands in the terminal:
- Open terminal in the folder
- sudo apt install python3-tk
- python3 -m venv .venv
- source .venv/bin/activate
- pip install -r requirements.txt
- Launch from running in code editor or type 'python3 finance_tracker.py'
P.S. - Linux (atleast Mint) don't have python packages that launch tkinter by default, so you need to install them manually, it will be installed on main system, not virtual environment.
# Structure introduction
## Files
- accounts.txt - keeps the list of all accounts
- finances.txt - keep records of spendings/earnings
## Entry 
Used to input new accounts or data records into .txt files:
- 'select account' let's choose from already created accounts
- '+' inputs new account
- 'input ammount' field - inputs money amount (- for spending, nothing for earning)
- 'gain source / spend destination' field - inputs the reason for spending/earning, where the money went/came from
- 'save' button - saves the input into the finances.txt
## Overview
- 'choose accounts' - choose 1 or multiple accounts
- 'choose time period' - choose how much data to show (based on date of inputs)
- 'show' button - opens table with finances.txt data, just in more presentable format than .txt file
## History
- 'choose account' and 'choose time period' - works same as in overview
- 'plot' button - opens a graph that shows how total amount of money changed by date in selected accounts
## Chart
- 'choose account' and 'choose time period' - works same as previous examples, but you can only choose 1 account
- 'plot' button - shows 2 pie charts, 1-st shows how much money earnt from each reason (input from entry tab last field), 2-nd shows spendings
## Export
Exports .txt file data in .csv or excel format.
### CSV
- 'choose account' and 'choose time period' - same as previous (multiple accounts)
- 'name the file' - name of saved file
- 'save to csv' - opens file manager to choose where to save the file
### Xlsx
- same principle as csv, just exports excel file