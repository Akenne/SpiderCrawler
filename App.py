import threading
from tkinter import *
import SpiderCrawler
import multilist
import webbrowser

class Application():
    def __init__(self):
        self.app = Tk()
        self.app.wm_title("Spider Crawler")
        self.app.minsize(width=880, height=348)
        self.app.maxsize(width=880, height=348)

        mainmainleft = Frame(self.app)
        bottom = Frame(self.app)

        mainleft = Frame(mainmainleft)
        itemoptions = Frame(bottom)
        self.graph = multilist.McListBox(bottom)

        startn = Frame(mainleft)
        options = Frame(mainleft)
        hoursoption = Frame(mainleft)
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

        for i in [self.reset, self.buds, self.unusual, self.maxs, self.salvage]:
            i.set(True)

        self.b = Button(fstart, text="START", command=self.start)
        c = Button(buttons, text="Steam", command=self.steam).pack(side=LEFT, padx=(0,7))
        d = Button(buttons, text="GotoBP", command=self.backpack).pack(side=LEFT)
        self.b.pack(side=LEFT)

        buttons.pack()
        self.var = StringVar(self.app)
        self.var.set("http://bptf/id/profiles")

        option = OptionMenu(bp, self.var, "http://backpack.tf/profiles/", "http://tf2items.com/profiles/", "http://tf2b.com/tf2/")
        option.pack()
        bp.pack(side = BOTTOM)    

        self.box = Entry(startn, textvariable=self.entryid, fg = "gray")
        self.box.bind("<Button-1>", self.callback)
        self.box.insert(0, "Enter steamid")
        self.box.pack(side = TOP, anchor=N, padx =25, pady = 10)

        labelText=StringVar()
        labelText.set("Max Hours")
        Label(hoursoption, textvariable=labelText).pack(side=TOP)

        self.hours=IntVar()
        self.hours.set(250)
        Entry(hoursoption,textvariable=self.hours,width=5).pack(side=TOP, pady = (0,20))

        Checkbutton(options, text = "Reload item schema", variable = self.SchemaUpdate).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(options, text = "Start with fresh id", variable = self.reset).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "Only never traded items", variable = self.traded).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "Genuines", variable = self.genuine).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "Earbuds", variable = self.buds).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "Bill's", variable = self.bills).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "Unusuals", variable = self.unusual).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "Max's items", variable = self.maxs).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "BMOCs", variable = self.bmoc).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "Salvaged crates", variable = self.salvage).pack(side=TOP, anchor=W, fill=Y)
        self.lbl = Label(fstart, text="0/0 found")
        self.lbl.pack(side = LEFT, anchor = W, padx = (20,0))

        fstart.pack(side=TOP)

        startn.pack(side=LEFT)
        options.pack(side=LEFT, padx=(0,30), pady = (5,0))
        allbuttons.pack(side=LEFT, pady=(10,0))
        hoursoption.pack(side=LEFT, padx = (25,0), pady = (5,0))
        
        mainleft.pack(side = TOP, anchor = N)
        self.graph.container.pack(side = LEFT, anchor = W, pady = 20)
        itemoptions.pack(side=LEFT, pady=(0,5), anchor = S)
        
        bottom.pack(side=BOTTOM)
        mainmainleft.pack(side = LEFT, padx=(10,0), anchor = N)
        self.app.mainloop()

    def updateGUI(self):
        msg = str(SpiderCrawler.fcount) + "/" + str(SpiderCrawler.count) + " found"
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
        while SpiderCrawler.run:
            item = SpiderCrawler.go(self.genuine.get(), self.buds.get(), self.bills.get(), self.unusual.get(), 
                self.maxs.get(), self.bmoc.get(), self.salvage.get(), self.hours.get(), self.traded.get())
            self.graph.tree.insert('', 'end', values=item) 
            self.updateGUI()  

    def callback(self, event):
        if (self.clicked == False):
            self.box.delete(0, END)
            self.box.config(fg = "black")
            self.clicked = True

    def steam(self): 
        try:
            webbrowser.open("steamcommunity.com/profiles/" + str(self.graph.tree.item(self.graph.tree.selection())["values"][0]))
        except:
            self.popup()

    def backpack(self): 
        webbrowser.open(self.var.get() + str(self.graph.tree.item(self.graph.tree.selection())["values"][0]))

    def popup(self):
        top = Toplevel()
        top.title("Error")
        msg = Label(top, text="You must select a found user first")
        msg.pack()
        button = Button(top, text="Dismiss", command=top.destroy)
        button.pack()