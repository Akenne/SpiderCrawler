try:
    import tkinter.ttk as ttk
except:
    import Tkinter.ttk as ttk
import SpiderCrawler

class McListBox(object):
    def __init__(self, frame):
        self.tree = None
        self.header = ['Id', 'Hours', 'Has']
        self._setup_widgets(frame)
        self._build_tree()
    def _setup_widgets(self, frame):
        self.container = ttk.Frame(frame)
        self.tree = ttk.Treeview(columns=self.header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=self.container)
        vsb.grid(column=1, row=0, sticky='ns', in_=self.container)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
    def _build_tree(self):
        count = 0
        hey = [187, 63, 420]
        for col in self.header:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: sortby(self.tree, c, 0))
            self.tree.column(col,
                width=hey[count])
            count+=1      

def sortby(tree, col, descending):
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    if (data[0][0]).isdigit():
        data = [(int(a), b) \
            for a, b in data]
        data = sorted(data, key=lambda tup: tup[0], reverse=descending)
    else:
        data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
        int(not descending)))