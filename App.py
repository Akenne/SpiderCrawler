
from tkinter import *
import SpiderCrawler


class Application:
    ## creating application
    def __init__(self):
    	app = Tk()
    	options = Frame(app)
    	itemoptions = Frame(app)
    	hoursoption = Frame(app)
    	SchemaUpdate = BooleanVar()
    	reset = BooleanVar()
    	genuine = BooleanVar()
    	buds = BooleanVar()
    	bills = BooleanVar()
    	unusual = BooleanVar()
    	maxs = BooleanVar()
    	bmoc = BooleanVar()
    	salvage = BooleanVar()
    	entryid = StringVar()


    	clicked = False

    	def start():
    		SpiderCrawler.start()

    	def callback(event):
    	    global clicked
    	    if (clicked == False):
    	        box.delete(0, END)
    	        box.config(fg = "black")
    	        clicked = True

    	b = Button(app, text="START", command=start)
    	b.pack()

    	box = Entry(options, fg = "gray")
    	box.bind("<Button-1>", callback)
    	box.insert(0, "Enter steamid")
    	box.pack(side = LEFT, anchor=N, padx =25, pady = 10)

    	labelText=StringVar()
    	labelText.set("Max Hours")
    	Label(itemoptions, textvariable=labelText).pack(side=TOP)

    	directory=StringVar(None)
    	Entry(itemoptions,textvariable=directory,width=5).pack(side=TOP, pady = (0,20))

    	Checkbutton(options, text = "Reload item schema", variable = SchemaUpdate).pack(side=TOP, anchor=W, fill=Y)
    	Checkbutton(options, text = "Start with fresh id", variable = reset).pack(side=TOP, anchor=W, fill=Y)
    	Checkbutton(itemoptions, text = "Genuines", variable = genuine).pack(side=TOP, anchor=W, fill=Y)
    	Checkbutton(itemoptions, text = "Earbuds", variable = buds).pack(side=TOP, anchor=W, fill=Y)
    	Checkbutton(itemoptions, text = "Bill's", variable = bills).pack(side=TOP, anchor=W, fill=Y)
    	Checkbutton(itemoptions, text = "Unusuals", variable = unusual).pack(side=TOP, anchor=W, fill=Y)
    	Checkbutton(itemoptions, text = "Max's items", variable = maxs).pack(side=TOP, anchor=W, fill=Y)
    	Checkbutton(itemoptions, text = "BMOCs", variable = bmoc).pack(side=TOP, anchor=W, fill=Y)
    	Checkbutton(itemoptions, text = "Salvaged crates", variable = salvage).pack(side=TOP, anchor=W, fill=Y)

    	options.pack(side=LEFT, anchor=N, padx=(0,300))
    	itemoptions.pack(side=LEFT, fill=BOTH, expand=YES, pady=(5,0))

    	app.mainloop()