import threading
from tkinter import *
import SpiderCrawler


class Application():
    def __init__(self):
        self.app = Tk()
        startn = Frame(self.app)
        options = Frame(self.app)
        itemoptions = Frame(self.app)
        hoursoption = Frame(self.app)
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

        self.lbl = Label(itemoptions, text="0/0")
        self.lbl.pack(side = TOP)

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

        startn.pack(side=LEFT, anchor = N)

        labelText=StringVar()
        labelText.set("Max Hours")
        Label(itemoptions, textvariable=labelText).pack(side=TOP)

        hours=IntVar()
        hours.set(250)
        Entry(itemoptions,textvariable=hours,width=5).pack(side=TOP, pady = (0,20))

        Checkbutton(options, text = "Reload item schema", variable = SchemaUpdate).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(options, text = "Start with fresh id", variable = reset).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(options, text = "Only never traded", variable = traded).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "Genuines", variable = genuine).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "Earbuds", variable = buds).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "Bill's", variable = bills).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "Unusuals", variable = unusual).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "Max's items", variable = maxs).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "BMOCs", variable = bmoc).pack(side=TOP, anchor=W, fill=Y)
        Checkbutton(itemoptions, text = "Salvaged crates", variable = salvage).pack(side=TOP, anchor=W, fill=Y)

        options.pack(side=LEFT, anchor=N, padx=(0,300))
        itemoptions.pack(side=LEFT, fill=BOTH, expand=YES, pady=(5,0))

        self.app.mainloop()

    def updateGUI(self):
        msg = str(SpiderCrawler.fcount) + "/" + str(SpiderCrawler.count)
        self.lbl["text"] = msg
        self.lbl.after(1000, self.updateGUI)
