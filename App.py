import threading
try:
    from tkinter import *
except ImportError:
    from Tkinter import *
import SpiderCrawler
import multilist
import webbrowser

class Application():
    def __init__(self):
        self.app = Tk()
        self.app.wm_iconbitmap('.\data\spider.ico')
        self.app.wm_title("Spider Crawler")
        #self.app.minsize(width=914, height=331)
        #self.app.maxsize(width=914, height=331)

        mainmainleft = Frame(self.app)
        bottom = Frame(self.app)

        mainleft = Frame(mainmainleft)
        itemoptions = Frame(bottom)
        self.graph = multilist.McListBox(bottom)

        startn = Frame(mainleft)
        options = Frame(mainleft)
        hourcredits = Frame(mainleft)

        checkoptions = Frame(options)
        boxoptions = Frame(options)

        hoursoption = Frame(hourcredits)
        credits = Frame(hourcredits)

        allbuttons = Frame(mainleft)

        fstart = Frame(startn)

        bp = Frame(allbuttons)
        buttons = Frame(allbuttons)

        self.SchemaUpdate = BooleanVar()
        self.reset = BooleanVar()
        self.genuine = BooleanVar()
        self.buds = BooleanVar()
        self.bills = BooleanVar()
        self.unusual = BooleanVar()
        self.maxs = BooleanVar()
        self.bmoc = BooleanVar()
        self.salvage = BooleanVar()
        self.traded = BooleanVar()
        self.entryid = StringVar()

        self.clicked = False

        for i in [self.reset, self.buds, self.unusual, self.maxs, self.salvage, self.traded]:
            i.set(True)

        self.b = Button(fstart, text="START", command=self.start)
        c = Button(buttons, text="Steam", command=self.steam).pack(side=LEFT, padx=(0,7))
        d = Button(buttons, text="GotoBP", command=self.backpack).pack(side=LEFT)
        self.b.pack(side=LEFT)

        buttons.pack()
        self.var = StringVar(self.app)
        self.var.set("http://backpack.tf/profiles/")

        option = OptionMenu(bp, self.var, "http://backpack.tf/profiles/", "www.tf2items.com/profiles/", "www.tf2b.com/tf2/")
        option.config(width = 18)
        option.pack()
        bp.pack(side = BOTTOM)    

        self.box = Entry(startn, textvariable=self.entryid, fg = "gray")
        self.box.bind("<Button-1>", self.callback)
        self.box.insert(0, "Enter steamid")
        self.box.pack(side = TOP, anchor=N, padx =(5,25), pady = 10)

        Label(credits, text="Created by Akenne", font=("Times New Roman", 8)).pack(anchor = E, pady = (0,25))

        credits.pack(side=TOP, anchor=E)

        Label(hoursoption, text="Max Hours:").pack(side=LEFT, padx = (0,10))

        self.hours=IntVar()
        self.hours.set(500)
        Entry(hoursoption,textvariable=self.hours,width=5).pack(side=LEFT)

        hoursoption.pack(padx= (0,45))

        Checkbutton(checkoptions, text = "Reload item schema", variable = self.SchemaUpdate).pack(side=TOP, anchor=W, pady =(0, 3))
        Checkbutton(checkoptions, text = "Start with fresh id", variable = self.reset).pack(side=TOP, anchor=W)
        checkoptions.pack(side = TOP)
        Label(boxoptions, text="Threads:").pack(side=LEFT, padx = (0,10))
        self.thread=IntVar()
        self.thread.set(25)
        Entry(boxoptions,textvariable=self.thread,width=5).pack(side=LEFT)
        boxoptions.pack(padx= (0,45))

        Checkbutton(itemoptions, text = "Only never traded items", variable = self.traded).pack(side=TOP, anchor=W)
        Checkbutton(itemoptions, text = "Genuines", variable = self.genuine).pack(side=TOP, anchor=W)
        Checkbutton(itemoptions, text = "Earbuds", variable = self.buds).pack(side=TOP, anchor=W)
        Checkbutton(itemoptions, text = "Bill's", variable = self.bills).pack(side=TOP, anchor=W)
        Checkbutton(itemoptions, text = "Unusuals", variable = self.unusual).pack(side=TOP, anchor=W)
        Checkbutton(itemoptions, text = "Max's items", variable = self.maxs).pack(side=TOP, anchor=W)
        Checkbutton(itemoptions, text = "BMOCs", variable = self.bmoc).pack(side=TOP, anchor=W)
        Checkbutton(itemoptions, text = "Salvaged crates", variable = self.salvage).pack(side=TOP, anchor=W)
        self.lbl = Label(fstart, text="0/0 found")
        self.lbl.pack(side = LEFT, anchor = W, padx = (20,30))

        fstart.pack(side=TOP)

        startn.pack(side=LEFT, anchor = W, padx = (10, 0))
        options.pack(side=LEFT, padx=(0,30), pady = (5,0))
        allbuttons.pack(side=LEFT, pady=(10,0), padx = (40,0))
        hourcredits.pack(side=LEFT, padx = (95,0), anchor = E)
        
        mainleft.pack(side = TOP, anchor = W)
        self.graph.container.pack(side = LEFT, anchor = W, pady = 10)
        itemoptions.pack(side=LEFT, anchor = E, padx=7)
        
        mainmainleft.pack(side = TOP, fill = X)
        bottom.pack(padx =10)
        self.app.mainloop()

    def updateGUI(self):
        fcount = str(SpiderCrawler.fcount)
        count = str(SpiderCrawler.count)
        msg = fcount + "/" + count + " found"
        self.lbl["text"] = msg

    def start(self):
        t1 = threading.Thread(target = self.threads)
        t1.daemon = True
        t1.start()
        SpiderCrawler.run = True
        self.b.configure(text = "STOP", command=self.stop)

    def stop(self):
        SpiderCrawler.run = False
        self.b.configure(text = "START", command=self.start)

    def threads(self):
        if self.entryid.get() == "Enter steamid":
            self.box.delete(0, END)
            self.box.config(fg = "black")
            self.clicked = True
        SpiderCrawler.start(self.SchemaUpdate.get(), self.reset.get(), self.entryid.get())
        SpiderCrawler.go(self.thread.get(), self, self.genuine.get(), self.buds.get(), self.bills.get(), self.unusual.get(), self.maxs.get(), self.bmoc.get(), self.salvage.get(), self.hours.get(), self.traded.get())

    def callback(self, event):
        if (self.clicked == False):
            self.box.delete(0, END)
            self.box.config(fg = "black")
            self.clicked = True

    def steam(self): 
        try:
            webbrowser.get("windows-default").open("www.steamcommunity.com/profiles/" + str(self.graph.tree.item(self.graph.tree.selection())["values"][0]))
        except:
            self.popup()

    def backpack(self): 
        try:
            webbrowser.get("windows-default").open(self.var.get() + str(self.graph.tree.item(self.graph.tree.selection())["values"][0]))
        except:
            self.popup()

    def popup(self):
        top = Toplevel()
        top.title("Error")
        msg = Label(top, text="You must select a found user first")
        msg.pack()
        button = Button(top, text="Dismiss", command=top.destroy)
        button.pack()