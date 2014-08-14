import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import SpiderCrawler

class McListBox(object):
    def __init__(self, frame):
        self.tree = None
        self._setup_widgets(frame)
        self._build_tree()
        self.tree.bind("<1>", self.OnClick)
    def _setup_widgets(self, frame):
        self.container = ttk.Frame(frame)
        self.tree = ttk.Treeview(columns=header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=self.container)
        vsb.grid(column=1, row=0, sticky='ns', in_=self.container)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
    def _build_tree(self):
        count = 0
        hey = [187, 63, 420]
        for col in header:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: sortby(self.tree, c, 0))
            self.tree.column(col,
                width=hey[count])
            count+=1
        #for item in clist:
        #    self.tree.insert('', 'end', values=item)
    def OnClick(self, event):
        allrow=self.tree.item(self.tree.selection())
        print (allrow["values"][0])
        

def sortby(tree, col, descending):
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
        int(not descending)))

header = ['Id', 'Hours', 'Has']
''''
clist = [
('76561197986697804', '250', 'Unusual drill sergeant, max hessssssssssssssssssaddse item') ,
('Honda', 'light') ,
('Lexus', 'battery') ,
('Benz', 'wiper') ,
('Ford', 'tire') ,
('Chevy', 'air') ,
('Chrysler', 'piston') ,
('Toyota', 'brake pedal') ,
('BMW', 'seat')
]
'''