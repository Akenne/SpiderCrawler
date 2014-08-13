import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import SpiderCrawler

# FOUND THIS ON THE INTERNET NOT MY CODE 

class McListBox(object):
    def __init__(self, frame):
        self.tree = None
        self._setup_widgets(frame)
        self._build_tree()
    def _setup_widgets(self, frame):
        self.container = ttk.Frame(frame)
        self.tree = ttk.Treeview(columns=header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=self.container)
        vsb.grid(column=1, row=0, sticky='ns', in_=self.container)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
    def _build_tree(self):
        for col in header:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))
        for item in clist:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(header[ix],width=None)<col_w:
                    self.tree.column(header[ix], width=col_w)
def sortby(tree, col, descending):
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
        int(not descending)))

header = ['Name', 'Hours', 'Joined', 'BPLink', 'SteamLink', 'Has']
clist = [
('Hyundai', 'brakes') ,
('Honda', 'light') ,
('Lexus', 'battery') ,
('Benz', 'wiper') ,
('Ford', 'tire') ,
('Chevy', 'air') ,
('Chrysler', 'piston') ,
('Toyota', 'brake pedal') ,
('BMW', 'seat')
]