# Project
App to input and store money amount spent or earned to specific acount and destination/source (for example: 0.02 cents in piggy bank 'found on the street'; 120 euros in bank acount 'birthday gift; -20.59 euros from wallet 'lunch). The input will automatically be saved into text file (after pressing button, choosing acount and inputing amount and text - date, gain/spent based on if there is '-' before amount and lowercasing text will be saved into txt), data from file will be used in other windows to show historical change, whole amount or percentale spending/gain based on source/destination.

# Limitations
- only used on Windows (probably doesn't work on Linux/Mac)
- PC app (doesn't work on phone)
- not optimised (first version)
- code repeats

# Parts
## entry: (input new data to txt)
- dropdown account field
- input amount field
- input text field (where got/spent)
- button to input
- Result -> save data into .txt

## overview: (show pandas table of inputs)
- dropdown account field (1, multiple or all) - currently static
- button to show (show overall amount)
- Result -> show table with data from .txt stored data in app

## history: (matplotlib graph)
- dropdown account field (1, multiple or all) - currently static
- time field (all time, this month, past 3/6 months) - currently static
- button to plot (plots matplotlib with current amount)
- Result -> plots graph with acounts balance change by time

## chart: (pie chart of all spendings and earnings, 2 seperate)
- dropdown accoutn field (choose only 1 acount)
- button to plot
- Result -> plots 2 pie charts of 1 chosen acount, one shows how much percent spent on each destination, other shows how much gain percentaly from different sources

## export: (save to excel or csv)
- save file name field 
- save file place field (same directory if empty)
- dropdown account field (1, multiple or all) - currently static
- time field (all time, this month, past 3/6 months) - currently static
- button to save
- Result -> export acounts data in specific time period into excel or csv 

# Future improvement
- app should work on linux/windows/mac
- make docker image
- rewrite project using classes and decrease code repeats
- add color palete change (bright/dark + choose colors to not clash with colorblindness)
- try to make src/dst less rigid (for example 'birthday gift' and 'birthday' should be counted as one, considering both are in 'gain' category)