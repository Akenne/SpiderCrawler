import threading
try:
    from tkinter import *
except ImportError:
    from Tkinter import *
import SpiderCrawler
import multilist
import webbrowser
import json

class Application(Frame):
    def __init__(self,master=None):
        root = Tk()
        Frame.__init__(self,master)
        root.wm_iconbitmap('.\data\spider.ico')
        root.wm_title("Spider Crawler")

        topframe = Frame(root)
        midframe = Frame(root)
        botframe = Frame(root)

        for i in range(5):
            topframe.columnconfigure(i, weight=1)
            botframe.columnconfigure(i, weight=1)

        self.graph = multilist.McListBox(midframe)
        self.graph.container.pack()
        
        self.SchemaUpdate = BooleanVar()
        self.reset = BooleanVar()
        self.genuine = BooleanVar()
        self.buds = BooleanVar()
        self.bills = BooleanVar()
        self.unusual = BooleanVar()
        self.stranges = BooleanVar()
        self.maxs = BooleanVar()
        self.bmoc = BooleanVar()
        self.salvage = BooleanVar()
        self.traded = BooleanVar()
        self.f2p = BooleanVar()
        self.untradable = BooleanVar()

        self.entryid = StringVar()
        self.apikey = StringVar()
        self.bpurl = StringVar()

        self.hours=IntVar()
        self.recenthours=IntVar()
        self.thread=IntVar()

        self.clicked = False
        self.hours.set(500)
        self.recenthours.set(500)
        self.thread.set(25)
        self.bpurl.set("http://backpack.tf/profiles/")

        with open('config.json', 'r') as f:
            config = json.load(f)
            self.SchemaUpdate.set(config['SchemaUpdate']) 
            self.reset.set(config['reset']) 
            self.genuine.set(config['genuine'])
            self.buds.set(config['buds'])
            self.bills.set(config['bills'])
            self.unusual.set(config['unusual'])
            self.stranges.set(config['stranges']) 
            self.maxs.set(config['maxs'])
            self.bmoc.set(config['bmoc'])
            self.salvage.set(config['salvage']) 
            self.traded.set(config['traded']) 
            self.f2p.set(config['f2p'])
            self.untradable.set(config['untradable'])
            self.apikey.set(config['apikey'])
            self.hours.set(config['hours'])
            self.recenthours.set(config['recenthours'])
            self.thread.set(config['thread'])
        #except:
        #    for i in [self.reset, self.buds, self.unusual, self.maxs, self.salvage, self.traded]:
        #        i.set(True)

        self.box = Entry(topframe, textvariable=self.entryid, fg = "gray")
        self.box.bind("<Button-1>", self.callback)
        self.box.insert(0, "Enter steamid")
        self.box.grid(row=0, column=0, columnspan =3, pady = 5, padx = (5,0))

        self.b = Button(topframe, text="START", command=self.start)
        self.b.grid(row=1, column=0, padx = (5,2), pady = (0,5))
        self.cl = Button(topframe, text="CLEAR", command=self.clear).grid(row=1, column=1, padx = (0,2), pady = (0,5))
        self.he = Button(topframe, text="HELP", command=self.clear).grid(row=1, column=2, pady = (0,5))

        Checkbutton(topframe, text = "Reload item schema", variable = self.SchemaUpdate).grid(row=0, column=4, sticky = W, padx = 5)
        Checkbutton(topframe, text = "Start with fresh id", variable = self.reset).grid(row=1, column=4, sticky = W, padx = 5)

        c = Button(topframe, text="Steam", command=self.steam).grid(row=0, column=5, padx = 5, pady = (5,0))
        d = Button(topframe, text="GotoBP", command=self.backpack).grid(row=0, column=6, pady = (5,0))
        option = OptionMenu(topframe, self.bpurl, "http://backpack.tf/profiles/", "www.tf2items.com/profiles/", "www.tf2b.com/tf2/")
        option.config(width = 22)
        option.grid(row=0, column=7, padx = 5, pady = (5,0))
        
        Label(topframe, text="Threads:").grid(row=1, column=5, pady = 5)
        Entry(topframe,textvariable=self.thread,width=5).grid(row=1, column=6)

        self.lbl = Label(topframe, text="0/0 found")
        self.lbl.grid(row=1, column=7, padx = (45,0)) 

        Label(botframe, text="Created by Akenne", font=("Times New Roman", 8)).grid(row=3, column=0, sticky = W)


        Label(botframe, text="Max Hours:").grid(row=0, column=4, sticky = W)
        Entry(botframe,textvariable=self.hours,width=5).grid(row=1, column=4, sticky = W)

        Label(botframe, text="Max recent Hours:").grid(row=2, column=4, sticky = W)
        Entry(botframe,textvariable=self.recenthours,width=5).grid(row=3, column=4, sticky = W, pady = (0,5))

        Checkbutton(botframe, text = "Hide traded", variable = self.traded).grid(row=0, column=3, sticky = W)
        Checkbutton(botframe, text = "Hide f2p", variable = self.f2p).grid(row=1, column=3, sticky = W)
        Checkbutton(botframe, text = "Hide untradable", variable = self.untradable).grid(row=2, column=3, sticky = W)

        Checkbutton(botframe, text = "Earbuds", variable = self.buds).grid(row=0, column=0, sticky = W)
        Checkbutton(botframe, text = "Bill's", variable = self.bills).grid(row=1, column=0, sticky = W)
        Checkbutton(botframe, text = "Max's items", variable = self.maxs).grid(row=2, column=0, sticky = W)

        Checkbutton(botframe, text = "Genuines", variable = self.genuine).grid(row=0, column=2, sticky = W)
        Checkbutton(botframe, text = "Unusuals", variable = self.unusual).grid(row=1, column=2, sticky = W)
        Checkbutton(botframe, text = "Stranges", variable = self.stranges).grid(row=2, column=2, sticky = W)

        Checkbutton(botframe, text = "BMOCs", variable = self.bmoc).grid(row=0, column=1, sticky = W)
        Checkbutton(botframe, text = "Salvaged crates", variable = self.salvage).grid(row=1, column=1, sticky = W)

        self.api()

        topframe.grid(row =0, column = 0, sticky=N+E+W)
        midframe.grid(row =1, column = 0, sticky=E+W)
        botframe.grid(row =2, column = 0, sticky=S+E+W)

        def handler():
            self.config = {'SchemaUpdate': self.SchemaUpdate.get(), 'reset': self.reset.get(), 'genuine': self.genuine.get(), 'buds': self.buds.get(), 'bills': self.bills.get(), 'unusual': self.unusual.get()
            , 'stranges': self.stranges.get(), 'maxs': self.maxs.get(), 'bmoc': self.bmoc.get(), 'salvage': self.salvage.get(), 'traded': self.traded.get(), 'f2p': self.f2p.get(), 'untradable': self.untradable.get()
            , 'apikey': self.apikey.get(), 'hours': self.hours.get(), 'recenthours': self.recenthours.get(), 'thread':self.thread.get()}     
            with open('config.json', 'w') as f:
                json.dump(self.config, f)
            root.quit()

        root.protocol("WM_DELETE_WINDOW", handler)

        root.mainloop()

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
        SpiderCrawler.API = self.apikey.get()
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
            webbrowser.get("windows-default").open(self.bpurl.get() + str(self.graph.tree.item(self.graph.tree.selection())["values"][0]))
        except:
            self.popup()

    def clear(self):
        for i in self.graph.tree.get_children():
            self.graph.tree.delete(i)

    def popup(self):
        top = Toplevel()
        top.title("Error")
        msg = Label(top, text="You must select a found user first")
        msg.pack()
        button = Button(top, text="Dismiss", command=top.destroy)
        button.pack()

    def api(self):
        top = Toplevel()
        top.title("Enter Steam API key")
        entry = Entry(top, textvariable=self.apikey,width=36)
        entry.pack(padx = 15, pady = 5)
        button = Button(top, text="Save", command=top.destroy)
        button.pack()