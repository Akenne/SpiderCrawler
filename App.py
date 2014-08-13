import threading
from tkinter import *
import SpiderCrawler
import multilist


class Application():
    def __init__(self):
        self.app = Tk()

        itemoptions = Frame(self.app)
        mainmainleft = Frame(self.app)

        mainleft = Frame(mainmainleft)
        graph = multilist.McListBox(mainmainleft)

        startn = Frame(mainleft)
        options = Frame(mainleft)
        hoursoption = Frame(mainleft)

        SchemaUpdate = BooleanVar()
        reset = BooleanVar()
        genuine = BooleanVar()
        buds = BooleanVar()
        bills = BooleanVar()
        unusual = BooleanVar()
        maxs = BooleanVar()
        bmoc = BooleanVar()
        salvage = BooleanVar()
        traded = BooleanVar()
        entryid = StringVar()

        self.clicked = False

        for i in [reset, buds, unusual, maxs, salvage]:
            i.set(True)

        self.lbl = Label(mainleft, text="0/0 found")
        

        def start():
            t1 = threading.Thread(target = SpiderCrawler.start, args = (SchemaUpdate.get(), reset.get(), 
                entryid.get(), genuine.get(), buds.get(), bills.get(), unusual.get(), maxs.get(), bmoc.get(), salvage.get(), hours.get(), traded.get()))
            t1.daemon = True
            t1.start()
            SpiderCrawler.run = True
            b.configure(text = "STOP", command=stop)
            self.updateGUI()

        def stop():
            SpiderCrawler.run = False
            b.configure(text = "START", command=start)

        def callback(event):
            if (self.clicked == False):
                box.delete(0, END)
                box.config(fg = "black")
                self.clicked = True

        b = Button(startn, text="START", command=start)
        

        box = Entry(startn, textvariable=entryid, fg = "gray")
        box.bind("<Button-1>", callback)
        box.insert(0, "Enter steamid")
        box.pack(anchor=N, padx =25, pady = 10)
        b.pack(side = BOTTOM)

        labelText=StringVar()
        labelText.set("Max Hours")
        Label(hoursoption, textvariable=labelText).pack(side=TOP)

        hours=IntVar()
        hours.set(250)
        Entry(hoursoption,textvariable=hours,width=5).pack(side=TOP, pady = (0,20))

        Checkbutton(options, text = "Reload item schema", variable = SchemaUpdate).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(options, text = "Start with fresh id", variable = reset).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "Only never traded items", variable = traded).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "Genuines", variable = genuine).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "Earbuds", variable = buds).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "Bill's", variable = bills).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "Unusuals", variable = unusual).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "Max's items", variable = maxs).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "BMOCs", variable = bmoc).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "Salvaged crates", variable = salvage).pack(side=TOP, anchor=W, fill=Y)

        startn.pack(side=LEFT)
        options.pack(side=LEFT, padx=(0,150), pady = (5,0))
        self.lbl.pack(side = LEFT, anchor = N, pady = (15,0))
        hoursoption.pack(side=LEFT, padx = (25,0), pady = (5,0))
        
        mainleft.pack(side = TOP, anchor = N)
        graph.container.pack(anchor = W, pady = 20)
        
        mainmainleft.pack(side = LEFT, anchor = N)
        itemoptions.pack(side=LEFT, pady=(5,0), anchor = N)

        self.app.mainloop()

    def updateGUI(self):
        msg = str(SpiderCrawler.fcount) + "/" + str(SpiderCrawler.count) + " found"
        self.lbl["text"] = msg
        self.lbl.after(1000, self.updateGUI)
