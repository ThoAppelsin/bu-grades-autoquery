from bs4 import BeautifulSoup
import requests
import getpass
import regex
import math
import shutil
import sys
import os
import datetime
import pickle
import time
import winsound
from itertools import zip_longest

# Retrieve terminal dimensions
termcols, termrows = shutil.get_terminal_size()


def PlayNote(note, octave, duration):
    key = 3 + 12 * (4 + octave) + note
    fre = int(2 ** ((key - 49) / 12) * 440)

    winsound.Beep(fre, duration)


def Alarm1():
    ran = [1, 5, 3, 5, 4, 2, 0, 1]
    repeat = 2

    ran *= 4
    ran += [ran[0]]

    for i in ran:
        PlayNote(i, 1, 300)


def QueryForChange(url, alert=True):
    waitsecs = 3
    dotwaitsecs = 0.5

    initialcontent = requests.get(url).text
    initialtime = datetime.datetime.now()
    initialtstr = initialtime.strftime('%d %b %Y %H:%M:%S')

    latestcontent = None
    elapsedtime = None
    elapsedtstr = None
    timeinfostr = None

    def QueryLatest():
        nonlocal latestcontent
        nonlocal elapsedtime
        nonlocal elapsedtime
        nonlocal elapsedtstr
        nonlocal timeinfostr

        latestcontent = requests.get(url).text
        elapsedtime = datetime.datetime.now() - initialtime
        elapsedtstr = str(elapsedtime).split('.')[0]

        timeinfostr = 'Elapsed:\t' + elapsedtstr

        return latestcontent == initialcontent

    print('Querying:\t' + url)
    print('Started:\t' + initialtstr)

    while QueryLatest():
        sys.stdout.write('\r' + ' ' * (termcols - 1))
        sys.stdout.write('\r' + timeinfostr + ' ')
        sys.stdout.flush()

        for _ in range(int(waitsecs / dotwaitsecs)):
            time.sleep(dotwaitsecs)
            sys.stdout.write('.')
            sys.stdout.flush()

        time.sleep(waitsecs % dotwaitsecs)

    sys.stdout.write('\n')
    print('The page has changed!')

    if alert:
        Alarm1()


###
# Definitions of the offering functions
###


def printlist(offerlist, columncount):
    rowcount = math.ceil(len(offerlist) / columncount)
    columnwid = (termcols - 1) // columncount

    columns = []
    for i in range(columncount):
        start = i * rowcount
        end = start + rowcount
        column = [offer for offer in offerlist[start:end]]

        longestnrwid = len(str(end))
        longestofferwid = max(len(offer) for offer in column)

        for idx, offer in enumerate(column):
            offernr = repr(start + idx + 1).rjust(longestnrwid)
            column[idx] = (offernr + ') ' + offer).ljust(columnwid)[:columnwid]

        columns.append(column)

    rowtuples = zip_longest(*columns, fillvalue='')

    print('\n'.join(''.join(rowtuple) for rowtuple in rowtuples))


def offerthelist(question, offerlist, columncount=1, default=False):
    printlist(offerlist, columncount)

    if default:
        question += ' (default: ' + str(default) + ')'

    while True:
        print(question)
        inp = input()

        if inp:
            if inp.isdigit():
                choice = int(inp)
            else:
                continue
        else:
            choice = default

        if 1 <= choice <= len(offerlist):
            break

    return choice - 1


def offeryesno(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}

    if default is None:
        prompt = " [y/n]"
    elif default in valid:
        prompt = " [Y/n]" if valid[default] else " [y/N]"
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        print(question + prompt, end=' ', flush=True)
        choice = input().lower()

        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').")

################                     ################
################ Program Starts Here ################
################                     ################

print('Please welcome your Semester Grades!')

uname = 'user_name'
upass = 'user_pass'

credentials = {}

# Feel free to hardcode your credentials below
# to skip the prompt appearing on each run
# credentials[uname] = FAT_CEO
# credentials[upass] = PA$$WORD

if not credentials:
    print('We need your login credentials to continue')
    credentials[uname] = input('Student ID: ')

    if offeryesno('Want to see your password as you type?'):
        credentials[upass] = input('Password: ')
    else:
        credentials[upass] = getpass.getpass()

s = requests.Session()
info = s.get('https://registration.boun.edu.tr/scripts/stuinflogin.asp', data=credentials)
grades = s.get('http://registration.boun.edu.tr/scripts/stuinfgs.asp?donem=2016/2017-2')
grades_soup = BeautifulSoup(grades.text, 'html.parser')

grades_table = grades_soup.find_all('table')[1]
grades_rows = grades_table.find_all('tr', 'recmenu')

# print(grades_table.get_text(strip=True))

def extract_grade(row):
    cells = row.find_all('td')
    return tuple(cells[n].get_text(strip=True) for n in (0, 3))

grades = [extract_grade(row) for row in grades_rows]
for grade in grades:
    if grade[1]:
        print(grade[0], ': ', grade[1], sep='')

if not grades:
    print('You have no courses assigned for this semester!')
elif all(not grade[1] for grade in grades):
    print('None of your courses have been graded!')

# QueryForChange(url)
