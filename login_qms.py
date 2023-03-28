#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import json
import configparser

try:
    import tkinter
except:
    import Tkinter as tkinter

import os
import sys
import logging
import subprocess
sys.path.append(os.path.abspath(os.path.curdir))
# The scansn.py was run by another process, so import te_lib will trigger rebuild.
# Don't import any te_lib here.
#from te_lib.communicate.adb_lib import AdbLib
#from te_lib import GLOBAL_PARA

_LOG = logging.getLogger(__name__)

def record_user_pd(user,pd,station_id):
    content = {}
    content['user'] = user
    content['password'] = pd

    # Check Factory by building name
    if 'F2-' in station_id or 'P3-' in station_id:
        print('QCMC')
        os.system('net use \\\\10.18.6.48 /user:bekins bekind2')
        record_path = '\\\\10.18.6.48\\acer_m\\QA_station\\'
    else:
        print('QMB')
        os.system('net use \\\\10.97.1.48 /user:bekins bekind2SEL')
        record_path = '\\\\10.97.1.48\\SEL_Monitor\\QA_station\\'
    if not os.path.exists(record_path):
        os.makedirs(record_path)
    record_file = record_path + '%s.ini'%station_id
    try:
        os.remove(record_path)
    except:
        pass

    # Create a ini file for SF program get userID/PD
    config = configparser.ConfigParser()
    config.add_section('LoginInfo')
    config.set('LoginInfo', 'username', user)
    config.set('LoginInfo', 'password', pd)
    with open(record_file,'w')as f:
        config.write(f)
    return content


def ScanForm(plantform):
    # separate test plantform and get the station id
    if plantform == 'clifford':
        with open(os.path.expanduser('~')+'\\.clifford_station.txt','r')as f:
            text = f.readlines()
            for item in text:
                if 'STATION_ID' in item:
                    station_id = item.split('=')[1].strip()
                    print(station_id)

    if plantform == 'mars':
        with open(os.path.expanduser('~')+'\\mars.json','r')as f:
            text = json.load(f)
            station_id = text['mars_config']['identity']['station_id'].strip()
            print(station_id)
    
    def login(event):
        get_user_id = var_code_user.get().replace(' ','').upper()
        get_password = var_code_pd.get().replace(' ','')
        print(get_user_id)
        print(get_password)
        if get_user_id != '' and get_password != '':
            if len(get_user_id) > 8:
                note('ID length exceeds 8 characters','red')
            else:
                note('OK!','green')
                record_user_pd(get_user_id,get_password,station_id)
                master.destroy()
                master == None
                return
        

    def clearall():
        ety_scn_user.delete(0, tkinter.END)
        ety_scn_pd.delete(0, tkinter.END)

    def note(message, bgcolor):
        lab_msg.config(text='Message:%s' % message, bg=bgcolor)
        
    def quit():
        print('quit')
        master.quit()
        master.destroy()
        master == None
        
    master = tkinter.Tk()
    master.wm_attributes('-topmost', 1)
    master.title('QA station Get SN')
    master.focus()
    var_code_user = tkinter.StringVar()
    var_code_pd = tkinter.StringVar()

    lab_scnp = tkinter.Label(master, text="Username", font="Arial 16")
    lab_scnf = tkinter.Label(master, text="Password", font="Arial 16")
    lab_msg = tkinter.Label(master, text="XXXX", font="Arial 16")

    ety_scn_user = tkinter.Entry(master,font="Times 21",textvariable=var_code_user)
    ety_scn_pd = tkinter.Entry(master,font="Times 21",textvariable=var_code_pd)
    txt_lst = tkinter.Text(master,font="Times 21", width=20, height=10 )
    btn_clr = tkinter.Button(master, font="Arial 16",text='Clear All', command=clearall)
    btn_quit = tkinter.Button(master, font="Arial 16",text='Quit', command=quit)

    lab_scnp.grid(row=0, column=0, sticky=tkinter.E)
    lab_scnf.grid(row=1, column=0, sticky=tkinter.E)
    ety_scn_user.grid(row=0, column=1, sticky=tkinter.W)
    ety_scn_pd.grid(row=1, column=1, sticky=tkinter.W)
    btn_quit.grid(row=0, column=2, sticky=tkinter.E)
    btn_clr.grid(row=2, column=2, sticky=tkinter.E)
    lab_msg.grid(columnspan=2)

    ety_scn_user.bind('<Return>', login)
    ety_scn_pd.bind('<Return>', login)
    master.protocol('WM_DELETE_WINDOW', quit)

    ety_scn_user.focus()
    master.mainloop()

if __name__ == "__main__":
    ScanForm(sys.argv[1])

