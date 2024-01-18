import time
import tkinter as tk
import tkinter.messagebox

class Calcutime():
    """ 
    Calculation datetime difference
    Input format must be xxxx|xx|xx >> year|month|date|
    """
    def __init__(self):
        self.day28 = [2]
        self.day30 = [4,6,9,11]
        self.day31 = [1,3,5,7,8,10,12]
        self.year_diff_date = 0
        self.s_total_date = 365
        self.e_total_date = 365

        
    def SplitStarT(self):
        var = str(date_s.get())
        if len(var) < 8:
            tkinter.messagebox.showinfo(message='Input format must be xxxx|xx|xx >> year|month|date|;eg:20220304')
            return False
        self.Syear = int(var[0:4])
        self.Smonth = int(var[4:6])
        self.Sdate = int(var[6:8])

    def SplitEndT(self):
        var = str(date_e.get())
        if len(var) < 8:
            tkinter.messagebox.showinfo(message='Input format must be xxxx|xx|xx >> year|month|date|;eg:20220304')
            return False
        self.Eyear = int(var[0:4])
        self.Emonth = int(var[4:6])
        self.Edate = int(var[6:8])


    def Yeardiff(self):
        """
        Per 4 years will 1 year had 366 days,
        """
        for i in range(self.Syear,self.Eyear):
            if i%4 == 0:
                self.year_diff_date +=366
            else:
                self.year_diff_date +=365


    def YearCount(self):
        self.SplitStarT()
        self.SplitEndT()
        if self.Syear%4 == 0:
            self.s_total_date = 366
        if self.Eyear%4 == 0:
            self.e_total_date = 366
        s_total_count = 0
        e_total_count = 0
        for i in range(0,self.Smonth+1):
            if i in self.day28 and self.s_total_date == 366:
                s_total_count +=29
            if i in self.day28 and self.s_total_date == 365:
                s_total_count +=28
            if i in self.day30:
                s_total_count +=30
            if i in self.day31:
                s_total_count +=31
        s_total_count = s_total_count + self.Sdate
        for i in range(0,self.Emonth+1):
            if i in self.day28 and self.e_total_date == 366:
                e_total_count +=29
            if i in self.day28 and self.e_total_date == 365:
                e_total_count +=28
            if i in self.day30:
                e_total_count +=30
            if i in self.day31:
                e_total_count +=31
        e_total_count = e_total_count + self.Edate
        self.Yeardiff()
        return s_total_count,e_total_count


    def FinalCal(self):
        StartDate, EndDate = self.YearCount()
        EndYeardate = EndDate + self.year_diff_date
        result = EndYeardate-StartDate
        tkinter.messagebox.showinfo(message='两段时间间隔天数为：'+str(result)+'天,\n'
                                    'The interval day is: '+str(result))




if __name__ == '__main__':

    """    
    date_s = 20190617
    date_e = 20190610
    """
    calt = Calcutime()
    window = tk.Tk()
    window.title('DATE COUNT')
    window.geometry('200x200')

    date_s = tk.StringVar()
    date_e = tk.StringVar()
    l = tk.Label(window,text='Please enter the start date',bg='white',font=('Arial',10))
    s = tk.Entry(window,textvariable=date_s,bg='white')
    k = tk.Label(window,text='Please enter the end date',bg='white',font=('Arial',10))
    e = tk.Entry(window,textvariable=date_e,bg='white')
    
    Start = tk.Button(window,text='enter',command=calt.FinalCal)
    quit = tk.Button(window, text="QUIT", command=window.destroy)

    l.pack()
    s.pack()
    k.pack()
    e.pack()
    Start.pack()
    quit.pack()
    window.mainloop()
    print(Start)