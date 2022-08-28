import os
from math import log
from tkinter import *
import pandas as pd
import psutil
from psutil import NoSuchProcess, AccessDenied
import re

def get_log_files(desktop):
    """
    Function to get all log files from csv file and turns it to pandas table
    """
    newCsvFile = ""
    path = desktop+r'\Procmon'
    with os.scandir(path) as files:
        for entry in files:
            if ".txt" in entry.name and not entry.name == "Eula.txt":
                newCsvFile = entry.name.replace('.txt', '')
    df = pd.read_csv(desktop+'/Procmon/'+newCsvFile+'.CSV')
    return df


def get_offset_and_length(log_detail):
    off_fl = False
    offset_length = re.findall('[0-9]*,[0-9]+|[0-9]+', log_detail)
    temp_offset = temp_length = int
    for i in offset_length:
        if re.search('^[0-9]', i) is not None:
            if off_fl is False:
                temp_offset = i.replace(",", "")
                off_fl = True
            elif off_fl is True:
                temp_length = i.replace(",", "")
            offset_length = [temp_offset, temp_length]
    return offset_length


def check_entropy(open_log,offset,length):
    """
    Function to check for entropy of a given file
    :param length:
    :param offset:
    :param open_log:
    :return -log_entropy || 0
    """
    # variable to hold entropy value for a given file (open_log)
    log_entropy = 0
    # list to hold all probabilities of all the characters in text
    char_list = []
    probabilities = []
    # variable to hold the length of file
    file_length = len(open_log.read())
    # opening file from the offset
    open_log.seek(int(offset))
    # referencing the reading method to file_text
    file_text = open_log.read(int(length))
    # if file has something in it then check it
    if file_length > 0:
        # iterating through all characters in file_text
        for char in file_text:
            if char not in char_list:
                # appending every character's probability
                probabilities.append(file_text.count(char) / file_length)
                char_list.append(char)
        # iterating through probabilities
        for probability in probabilities:
            # summing the entropy of the file
            log_entropy += probability * log(probability, 2)
        # returning the entropy value
        return -log_entropy
    # return's 0 if the file has nothing in it
    return 0


def check_log_files(unchecked_logs):
    checked_logs = pd.DataFrame()
    # looping through logs in processLogFiles
    for log in unchecked_logs.itertuples():
        try:
            # getting the specific unicode to encode log file (usually cp1255)
            log_unicode = open(log[5]).encoding
            # opening the log file for analysis and referencing it to open_log
            with open(log[5], 'r', encoding=log_unicode) as open_log:
                temp_log_offset = str(get_offset_and_length(log[7])[0])
                temp_log_length = str(get_offset_and_length(log[7])[1])
                checked_logs = checked_logs.append(
                    {'Process Name': log[2], 'PID': log[3], 'Path': log[5], 'Detail': log[7],
                     'Entropy': check_entropy(open_log,temp_log_offset,temp_log_length)}, ignore_index=True)
                open_log.close()
        except UnicodeDecodeError:
            with open(log[5], 'rb') as open_log:
                temp_log_offset = str(get_offset_and_length(log[7])[0])
                temp_log_length = str(get_offset_and_length(log[7])[1])
                checked_logs = checked_logs.append(
                    {'Process Name': log[2], 'PID': log[3], 'Path': log[5], 'Detail': log[7],
                     'Entropy': check_entropy(open_log,temp_log_offset,temp_log_length)}, ignore_index=True)
                open_log.close()
        except TypeError:
            print('got a empty path\n')
        except PermissionError:
            continue
        except FileNotFoundError:
            if log[5][-3:] == "tmp":
                continue
    checked_logs['PID'] = checked_logs['PID'].astype(int)
    return checked_logs


def getSuspiciousPIDs(checked_df):
    entropy_avg = checked_df["Entropy"].mean()
    filtered_df = checked_df.loc[checked_df["Entropy"] >= 5.5]
    filtered_df = filtered_df.sort_values('Entropy', ascending=False)
    temp_df = pd.DataFrame(filtered_df)
    return temp_df


def popupMessage(PIDs):
    PIDs_str = PIDs['PID'].to_list()
    PIDs_str = list(dict.fromkeys(PIDs_str))
    # create root window
    root = Tk()
    # root window title and dimension
    root.title("Process Security threat")
    # Set geometry(widthxheight)
    root.geometry('350x200')
    i = 1
    for pid in PIDs_str:
        Label(root, text=pid).grid(column=1, row=i)
        i = i + 1
    # button is clicked
    def clicked():
        eliminateProcess(PIDs_str)
        root.destroy()
    # button widget with red color text
    btn = Button(root, text="Terminate Processes", fg="red", command=clicked)
    # set Button grid
    btn.grid(column=2, row=10)
    # Execute Tkinter
    root.mainloop()


def eliminateProcess(PIDs):
    for pid in PIDs:
        try:
            temp = psutil.Process(int(pid))
            temp.terminate()
            print("Process terminated; PID: "+str(pid))
        except ProcessLookupError:
            print("The process was not found")
        except NoSuchProcess:
            print("The process doesn't exists")
        except AccessDenied:
            print("Can't access this process")


def suspend_PIDs(PIDs):
    PIDs_str = PIDs['PID'].to_list()
    PIDs_str = list(dict.fromkeys(PIDs_str))
    for pid in PIDs_str:
        try:
            temp = psutil.Process(int(pid))
            temp.suspend()
            print("Process suspended; PID: "+str(pid))
        except ProcessLookupError:
            print("The process was not found")
        except NoSuchProcess:
            print("The process doesn't exists")
        except AccessDenied:
            print("Can't access this process")


if __name__ == "__main__":
    desktop = os.path.normpath(os.path.expanduser("~/Desktop"))
    df = get_log_files(desktop)
    checked_df = check_log_files(df)
    suspicious_PIDs_df = getSuspiciousPIDs(checked_df)
    suspend_PIDs(suspicious_PIDs_df)
    popupMessage(suspicious_PIDs_df)
    newCsvFile = ""
    path = desktop+r'/Procmon'
    with os.scandir(path) as files:
        for entry in files:
            if ".txt" in entry.name and not entry.name == "Eula.txt":
                newCsvFile = entry.name.replace('.txt', '')
    try:
        os.remove(desktop+r'/Procmon/' + newCsvFile + '.CSV')
        os.remove(desktop+r'/Procmon/' + newCsvFile + '.txt')
    except PermissionError:
        print('Could not delete temp csv and txt files')
    except FileNotFoundError:
        print('Could not find temp csv and txt files')
