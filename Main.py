from tkinter import *
from tkinter.messagebox import showerror
from tkinter.ttk import Combobox, Progressbar
import datetime
import threading
from tkinter.messagebox import askokcancel

class DataField(Frame):
    def __init__(self , master  ,width ="normal" , *args , **kwargs):
        Frame.__init__(self , master, *args , **kwargs)
        self.width = width

        self.build()

    def build(self):

        self.titleKwargs = {"font":("Consolas" , 15) , "bg":"#aaa" ,"width":17 if self.width=="normal" else 35 , "height":2}
        self.valueKwargs = {"font":("Consolas" , 15) , "bg":"#f0f" ,"width":12 if self.width=="normal" else 25 , "height":2}

        self.gridKwargs = {"pady": 5 , "padx":2 }

        # ===========================================

        self.confirmedTitle = Label(self , text = "Confirmed Cases" , **self.titleKwargs)
        self.confirmedTitle.grid(row = 1 , column = 0 , **self.gridKwargs)

        self.confirmedValue = Label(self  ,**self.valueKwargs)
        self.confirmedValue.grid(row = 1 , column = 1 ,**self.gridKwargs)

        # ===========================================

        self.activeTitle = Label(self, text="Active Cases", **self.titleKwargs)
        self.activeTitle.grid(row=2, column=0 ,**self.gridKwargs)

        self.activeValue = Label(self,text="" ,**self.valueKwargs)
        self.activeValue.grid(row=2, column=1 ,**self.gridKwargs)

        # ===========================================

        self.deathTitle = Label(self, text="No. of Deaths", **self.titleKwargs)
        self.deathTitle.grid(row=3, column=0,**self.gridKwargs)

        self.deathValue = Label(self,  **self.valueKwargs)
        self.deathValue.grid(row=3, column=1,**self.gridKwargs)

        # ===========================================

        self.recoveredTitle = Label(self, text="Recovered Cases", **self.titleKwargs)
        self.recoveredTitle.grid(row=4, column=0,**self.gridKwargs)

        self.recoveredValue = Label(self, **self.valueKwargs)
        self.recoveredValue.grid(row=4, column=1,**self.gridKwargs)

    def config(self , data):
        self.confirmedValue["text"] = data["confirmed"]
        self.deathValue["text"] = data["deaths"]
        self.recoveredValue["text"] = data["recovered"]
        self.activeValue["text"] = data["active"]

class CountryField(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.master = master



        self.build()

    def build(self):
        self.titleKwargs = {"font": ("Consolas", 15), "bg": "#aaa", "width": 13, "height": 2}
        self.valueKwargs = {"font": ("Consolas", 15), "bg": "#f0f", "width": 12, "height": 2}

        self.gridKwargs = {"pady": 5, "padx": 2}

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        self.idTitle = Label(self , text= "Country Id" , **self.titleKwargs)
        self.idTitle.grid(row = 1 , column = 0 ,**self.gridKwargs)

        self.idValue = Label(self  , **self.valueKwargs)
        self.idValue.grid(row = 1 , column = 1 ,**self.gridKwargs)

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        self.countryTitle = Label(self  ,text="Country", **self.titleKwargs)
        self.countryTitle.grid(row = 2 , column = 0 ,**self.gridKwargs)

        self.countryValue = Label(self  , **self.valueKwargs)
        self.countryValue.grid(row = 2 , column = 1 ,**self.gridKwargs)

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        self.latitudeTitle = Label(self, text="Latitude", **self.titleKwargs)
        self.latitudeTitle.grid(row=3, column=0, **self.gridKwargs)

        self.latitudeValue = Label(self,  **self.valueKwargs)
        self.latitudeValue.grid(row=3, column=1, **self.gridKwargs)

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        self.longitudeTitle = Label(self, text="Longitude", **self.titleKwargs)
        self.longitudeTitle.grid(row=4, column=0, **self.gridKwargs)

        self.longitudeValue = Label(self, **self.valueKwargs)
        self.longitudeValue.grid(row=4, column=1, **self.gridKwargs)

    def config(self ,data):
        self.idValue["text"] = data['id']
        self.countryValue["text"] = data['country']
        self.latitudeValue["text"] = data['latitude']
        self.longitudeValue["text"] = data['longitude']

class thread(threading.Thread):
    MODE_LOAD_WORLD_DATA = 1
    MODE_LOAD_COUNTRIES_LIST = 3
    MODE_LOAD_ALL_DATA = 4

    def __init__(self, mode, obj):
        threading.Thread.__init__(self)
        self.obj = obj

        self.mode = mode

    def run(self):
        if (self.mode == self.MODE_LOAD_WORLD_DATA):
            self.preTime = self.obj.LastUpdatedLabel["text"]
            self.obj.LastUpdatedLabel["text"] = ""
            try:
                self.obj.ThreadRunning = True
                data = {"active": self.obj.C.get_total_active_cases()
                    , "confirmed": self.obj.C.get_total_confirmed_cases()
                    , "deaths": self.obj.C.get_total_deaths(),
                        "recovered": self.obj.C.get_total_recovered()}

            except:
                if (not self.obj.covidInstalled):   # for Module Not Found Error
                    self.obj.progress.stop()
                    self.obj.progress.pack_forget()
                    self.installCovid()
                else:                                # for Connection Error
                    self.obj.BodyFrame['text'] = "Connection Error !"
                    showerror("Connection Error", "Make Sure You Have Internet Connection !", icon="warning")
                    self.obj.progress.stop()
                    self.obj.progress.pack_forget()

                self.obj.df.pack()


                self.obj.ThreadRunning = False
                return

            self.obj.BodyFrame['text'] = "World Data"
            self.obj.df.config(data)
            self.obj.progress.stop()
            self.obj.progress.pack_forget()
            # self.obj.progress.destroy()
            self.obj.df.pack()
            self.obj.WorldData = data
            self.obj.LastUpdatedLabel["text"] = self.preTime
            self.obj.ThreadRunning = False

        elif (self.mode == self.MODE_LOAD_COUNTRIES_LIST):
            self.obj.ThreadRunning = True

            self.obj.Countries = [x["name"] for x in self.obj.C.list_countries()]
            self.obj.CountryCombobox["values"] = self.obj.Countries
            self.obj.progress.stop()
            self.obj.progress.pack_forget()
            self.obj.ThreadRunning = False

        elif (self.mode == self.MODE_LOAD_ALL_DATA):
            self.preTime = self.obj.LastUpdatedLabel["text"]
            self.obj.LastUpdatedLabel["text"] = ""
            try:
                self.obj.ThreadRunning = True
                alldata = self.obj.C.get_data()
            except:
                if(not self.obj.covidInstalled):    # for Module Not Found Error
                    self.obj.progress.stop()
                    self.obj.progress.pack_forget()
                    self.installCovid()
                else:                                # for Connection Error
                    self.obj.BodyFrame['text'] = "Connection Error !"
                    showerror("Connection Error", "Make Sure You Have Internet Connection !", icon="warning")
                self.obj.progress.stop()
                self.obj.progress.pack_forget()
                self.obj.cf.pack(side="left", padx=7)
                self.obj.breaker.pack(side="left", padx=3)
                self.obj.df.pack(side="left", padx=7)

                self.obj.LastUpdatedLabel["text"] = self.preTime

                self.obj.ThreadRunning = False
                return

            self.obj.AllData = alldata
            # self.obj.progress.destroy()
            self.obj.progress.stop()
            self.obj.progress.pack_forget()

            self.obj.CountryCombobox["values"] = [x['country'] for x in alldata]

            countryName = self.obj.CountryCombobox.get()
            if (self.obj.CountryCombobox.get() not in self.obj.CountryCombobox["values"]):
                countryName = "India"

            countryData = None
            for x in alldata:
                if (x['country'] == countryName):
                    countryData = x
                    break
            self.obj.BodyFrame['text'] = "Country Wise Data (%s)" % (countryName)
            self.obj.cf.config(countryData)
            self.obj.df.config(countryData)
            self.obj.cf.pack(side="left", padx=7)
            self.obj.breaker.pack(side="left", padx=3)
            self.obj.df.pack(side="left", padx=7)
            self.obj.LastUpdatedLabel["text"] = "Last Update : %s"%self.obj.formatTime(countryData["last_update"])
            self.obj.ThreadRunning = False

    def installCovid(self):
        self.obj.BodyFrame['text'] = "Module Not Installed! "
        ask = askokcancel("Module Not Istalled" , "Do You Want to Install the Module ?")

        if(ask == True):
            import os
            os.system("title Installing Module &echo Make Sure You Are Connected to Internet.& pip install Covid")
            from covid import Covid
            C=Covid()
            self.obj.C = C
            self.obj.covidInstalled =True
            self.obj.ShowData(2)
        else:
            pass



class App(Frame):
    def __init__(self, master,*args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        try:
            from covid import Covid
            self.C = Covid()
            self.covidInstalled = True
        except ModuleNotFoundError:
            self.covidInstalled =False

        self.Countries = None
        self.WorldData = None
        self.AllData = None

        self.ThreadRunning = False

        self.TopFrame = LabelFrame(self, text="Select World or Country", font="Consolas 10", fg="blue")
        self.TopFrame.pack(fill="x", pady=20, padx=5)
        self.BuildTop(self.TopFrame)

        self.BodyFrame = LabelFrame(self, text="Data", font="Consolas 10", fg="blue")
        self.BodyFrame.pack(pady=5, fill="both", padx=5)
        self.progressFrame = Frame(self.BodyFrame)
        self.progressFrame.pack(side = "top" ,fill = "x")
        self.progress = Progressbar(self.progressFrame , orient="horizontal", mode="indeterminate")
        self.LastUpdatedLabel = Label(self ,font = "Consolas 10 bold" ,bg="#ffd")
        self.LastUpdatedLabel.pack(side="right")


        self.ShowData(2)

    def BuildTop(self, master):

        self.RadioVar = IntVar(master)
        self.RadioVar.set(2)

        self.options = {"font": ("Consolas", 15), "cursor": "hand2"}

        # 22222222222222222222222222

        self.WorldRadioButton = Radiobutton(master, text="World Data", variable=self.RadioVar)
        self.WorldRadioButton.config(value=1, command=lambda: self.RadioButtonSelected(1), **self.options)

        self.CountryRadioButton = Radiobutton(master, text="Country Data", variable=self.RadioVar)
        self.CountryRadioButton.config(value=2, command=lambda: self.RadioButtonSelected(2), **self.options)

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@2

        self.WorldRadioButton.pack(side="left", padx=20)
        self.CountryRadioButton.pack(side="left")

        # $$$$$$$$$$$$$$$$$$$$$$$$$$$

        self.previousRadioSelected = 2

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!1

        self.CountryCombobox = Combobox(master, state="normal", **self.options)
        self.CountryCombobox.pack(side="left", padx=5)
        self.CountryCombobox.bind("<<ComboboxSelected>>", lambda evt: self.OnComboBoxItemSelected())

        popup = self.CountryCombobox.tk.eval("ttk::combobox::PopdownWindow %s" % self.CountryCombobox)
        self.CountryCombobox.tk.call('%s.f.l' % popup, 'configure', '-font',
                                     ("Consolas 13"))

        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        breaker = Label(master, text="|", font="Consolas 25", fg="#bbb")
        breaker.pack(side="left")

        # *******************************

        self.RefreshBtn = Button(master, text="Refresh", font="Consolas 11", bd=1, cursor="hand2")
        self.RefreshBtn.config(command=self.refresh)
        self.RefreshBtn.pack(side='left')

    def RadioButtonSelected(self, flag):
        if (self.ThreadRunning):
            print("Busy...")
            self.RadioVar.set(1 if flag ==2 else 2)
            return

        if (flag == 1 and self.previousRadioSelected != 1):
            #print("World Selected")
            self.CountryCombobox.config(state="disable")
            self.ShowData(1)
            self.previousRadioSelected = 1
        elif (flag == 2 and self.previousRadioSelected != 2):
            #print("Country Selected")
            self.CountryCombobox.config(state="enable")
            self.ShowData(2)
            self.previousRadioSelected = 2

    def ShowData(self, flag):

        if (flag == 1):
            try:
                self.df.destroy()
                self.cf.destroy()
                self.breaker.destroy()
            except:
                pass
            self.df = DataField(self.BodyFrame, width="large")
            # Update Values Here
            # loading data
            if (self.WorldData == None):
                self.BodyFrame['text'] = "Loading Data ..."
                self.progress.pack(fill="x")
                self.progress.start(5)

                Th = thread(mode=thread.MODE_LOAD_WORLD_DATA, obj=self)
                Th.start()
            else:
                self.BodyFrame['text'] = "World Data"
                self.df.pack()
                self.df.config(self.WorldData)

            # data = C.get_status_by_country_id(27)
            # self.df.config(data)
            # self.progress.destroy()
            # self.df.pack()

        elif (flag == 2):
            try:
                self.df.destroy()
            except:
                pass

            self.cf = CountryField(self.BodyFrame)
            # Update Values Here
            # self.cf.pack(side="left" ,padx =7)

            self.breaker = Label(self.BodyFrame, bg="#000", height=16)
            # self.breaker.pack(side="left" ,padx =3)

            self.df = DataField(self.BodyFrame, width="normal")
            # Also Update Values Here
            # self.df.pack(side="left" ,padx = 7)

            if (self.AllData == None):
                self.BodyFrame['text'] = "Loading Data ..."
                self.progress.pack(fill="x")
                self.progress.start(5)
                Thr = thread(mode=thread.MODE_LOAD_ALL_DATA, obj=self)
                Thr.start()

                self.CountryCombobox.set("India")
            else:
                self.CountryCombobox["values"] = [x['country'] for x in self.AllData]
                countryData = None
                countryName = self.CountryCombobox.get()
                if (countryName not in self.CountryCombobox["values"]):
                    countryName = "India"
                    self.CountryCombobox.set("India")

                for x in self.AllData:
                    if (x['country'] == countryName):
                        countryData = x
                        break

                self.BodyFrame['text'] = "Country Wise Data (%s)" % countryName
                self.cf.config(countryData)
                self.df.config(countryData)

                self.cf.pack(side="left", padx=7)
                self.breaker.pack(side="left", padx=3)
                self.df.pack(side="left", padx=7)

    def OnComboBoxItemSelected(self):
        cur = self.CountryCombobox.get()
        data = None
        for z in self.AllData:
            if (z['country'] == cur):
                data = z
                break

        self.BodyFrame["text"] = "Country Wise Data (%s)" % cur
        self.df.config(data)
        self.cf.config(data)
        self.LastUpdatedLabel["text"] = "Last Update : %s"%self.formatTime(data["last_update"])

    def refresh(self):
        print("Refreshing ...")

        if (self.RadioVar.get() == 1):
            #print("World")
            self.BodyFrame['text'] = "Refreshing Data ..."
            self.progress.pack(fill="x")
            self.progress.start(5)

            Th = thread(mode=thread.MODE_LOAD_WORLD_DATA, obj=self)
            Th.start()

        elif (self.RadioVar.get() == 2):
            self.BodyFrame['text'] = "Refreshing Data ..."
            self.progress.pack(fill="x")
            self.progress.start(5)

            Thr = thread(mode=thread.MODE_LOAD_ALL_DATA, obj=self)
            Thr.start()

    def formatTime(self , timeStamp):

        timeStamp = int(int(timeStamp)/1000)
        date = datetime.datetime.fromtimestamp((timeStamp))
        if(date.day == datetime.datetime.today().day):
            time = "Today %02d:%02d "%(date.hour,date.minute)
        else:
            time = "%02d:%02d (%s/%s/%s) "%(date.hour ,date.minute ,date.day ,date.month ,date.year)
        return time


if __name__ == '__main__':

    root = Tk()
    root.title("Program to View Covid-19 Cases [rishitosh]")
    root.focus_force()
    root.minsize(700, 420)
    app = App(root)
    app.pack()
    #r.protocol("WM_DELETE_WINDOW", lambda *x:r.destroy())
    root.mainloop()
