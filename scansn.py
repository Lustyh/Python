#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import json

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

def get_snlist():
    # with open(GLOBAL_PARA.get_sn_list_path(), "r") as f:
    with open('./sn_list.json', "r") as f:
        duts = json.loads(f.read())
        f.seek(0)
    return duts

def ScanForm(args):
    num = int(args[1])
    def Scansn(event):
        # WIP9A19105DD000X5 = 17 digits
        # 9A26105DD0118G   = 14 digits
        get_scanned_sn = var_code_p.get().replace(' ', '').upper()
        var_code_p.set("")
        if get_scanned_sn[:4] == 'BWIP':
            get_scanned_sn = get_scanned_sn[1:]
        if get_scanned_sn == "":
            note('SN不能为空 SN is None', 'red')
        if ('WIP' in get_scanned_sn and len(get_scanned_sn) == 17):
            if get_scanned_sn in txt_lst.get(1.0, tkinter.END):
                note('SN重复 SN duplicate', 'red')
            else:
                txt_lst.insert(tkinter.END, "%s\n" % get_scanned_sn)
                note('OK!', 'green')
            if len(txt_lst.get(1.0,tkinter.END).split('\n'))  == 3:
                get_SNList('pass')
                master.destroy()
                master == None
                return
        if 'SKIP' in get_scanned_sn and len(get_scanned_sn) < 6:
            txt_lst.insert(tkinter.END,"%s\n"%get_scanned_sn)
            if len(txt_lst.get(1.0,tkinter.END).split('\n'))  == 3:
                get_SNList('pass')
                master.destroy()
                master == None
                return
        get_scanned_sn = var_code_f.get().replace(' ', '').upper()
        var_code_f.set("")
        if get_scanned_sn[:4] == 'BWIP':
            get_scanned_sn = get_scanned_sn[1:]
        if get_scanned_sn == "":
            note('SN不能为空 SN is None', 'red')
        if ('WIP' in get_scanned_sn and len(get_scanned_sn) == 17):
            if get_scanned_sn in txt_lst.get(1.0, tkinter.END):
                note('SN重复 SN duplicate', 'red')
            else:
                txt_lst.insert(tkinter.END, "%s\n" % get_scanned_sn)
                note('OK!', 'green')
            if len(txt_lst.get(1.0,tkinter.END).split('\n'))  == 3:
                get_SNList('fail')
                master.destroy()
                master == None
                return
        if 'SKIP' in get_scanned_sn and len(get_scanned_sn) < 6:
            txt_lst.insert(tkinter.END,"%s\n"%get_scanned_sn)
            if len(txt_lst.get(1.0,tkinter.END).split('\n'))  == 3:
                get_SNList('fail')
                master.destroy()
                master == None
                return
        # print(len(txt_lst.get(1.0,tkinter.END).split('\n')))
        # if 'START' in get_scanned_sn and len(get_scanned_sn) < 6:
        #     if len(txt_lst.get(1.0,tkinter.END).split('\n')) != num + 2:
        #         note('请输入所有位置上的SN please scan SN','red')
        #     else:
        #         get_SNList()
        #         master.destroy()
        #         master == None

    def get_SNList(result):
        snlist = txt_lst.get(1.0, tkinter.END).split('\n')
        tjson={}
        if result == 'pass':
            for x in range(0,num):
                tjson['DUT_pass'] = snlist[x]
                #with open(GLOBAL_PARA.get_sn_list_path(), "w") as f:
                with open('./sn_list.json', "w") as f:
                    f.write(json.dumps(tjson, indent=num))
                _LOG.info('snlist=%s', snlist)
                return snlist
        elif result == 'fail':
            for x in range(0,num):
                tjson['DUT_fail'] = snlist[x]
                #with open(GLOBAL_PARA.get_sn_list_path(), "w") as f:
                with open('./sn_list.json', "w") as f:
                    f.write(json.dumps(tjson, indent=num))
                _LOG.info('snlist=%s', snlist)
                return snlist

    def clearall():
        ''' clear all text '''
        # con = txt_lst.get(1.0, tkinter.END).split('\n')
        ety_scn.delete(0, tkinter.END)
        ety_scn_f.delete(0, tkinter.END)

    def note(message, bgcolor):
        lab_msg.config(text='Message:%s' % message, bg=bgcolor)

    def online(arg):
        # while not master == None:
        #     time.sleep(1)
        #     ret, out, err = None#AdbLib.adb_devices()
        #     lab_adb.config(text=out)
        while not master == None:
            time.sleep(1)
            p = subprocess.Popen(
            "adb devices",
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            )
            out, err = p.communicate()
            p.poll()
            lab_adb.config(text=out)
        
    def quit():
      print('quit')
      try:
        os.remove('./sn_list.json')
        pass
      except:
        pass
      master.quit()
      master.destroy()
      master == None
        
    master = tkinter.Tk()
    master.wm_attributes('-topmost', 1)
    master.title('QA station Get SN')
    master.focus()
    var_code_p = tkinter.StringVar()
    var_code_f = tkinter.StringVar()

    lab_scnp = tkinter.Label(master, text="ScanPASS", font="Arial 16")
    lab_scnf = tkinter.Label(master, text="ScanFAIL", font="Arial 16")
    lab_lst = tkinter.Label(master, text="List", font="Arial 16")
    lab_adb = tkinter.Label(master, text="XXXX", font="Arial 16", width=20)
    lab_msg = tkinter.Label(master, text="XXXX", font="Arial 16")

    ety_scn = tkinter.Entry(master,font="Times 21",textvariable=var_code_p)
    ety_scn_f = tkinter.Entry(master,font="Times 21",textvariable=var_code_f)
    txt_lst = tkinter.Text(master,font="Times 21", width=20, height=10 )
    btn_clr = tkinter.Button(master, font="Arial 16",text='Clear All', command=clearall)
    btn_quit = tkinter.Button(master, font="Arial 16",text='Quit', command=quit)

    lab_scnp.grid(row=0, column=0, sticky=tkinter.E)
    lab_scnf.grid(row=1, column=0, sticky=tkinter.E)
    # lab_lst.grid(row=2, column=0, sticky=tkinter.E)
    # lab_adb.grid(row=1, column=2, sticky=tkinter.W)
    lab_msg.grid(row=3, column=0, sticky=tkinter.W)
    ety_scn.grid(row=0, column=1, sticky=tkinter.W)
    ety_scn_f.grid(row=1, column=1, sticky=tkinter.W)
    # txt_lst.grid(row=2, column=1, sticky=tkinter.E)
    btn_quit.grid(row=0, column=2, sticky=tkinter.E)
    btn_clr.grid(row=2, column=2, sticky=tkinter.E)
    lab_msg.grid(columnspan=2)

    ety_scn.bind('<Key-Return>', Scansn)
    ety_scn_f.bind('<Key-Return>', Scansn)
    master.protocol('WM_DELETE_WINDOW', quit)

    ety_scn.focus()
    ety_scn_f.focus()
    #thread.start_new_thread(online,("",))
    master.mainloop()

if __name__ == "__main__":
    ScanForm(sys.argv)
    result = get_snlist()
    print(result)
    for v,k in result.items():
        if 'WIP' in k:
            print(1)

