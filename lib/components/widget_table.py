import tkinter as tk
import matplotlib.pyplot as plt
def opentable():
    global total_rows
    global total_columns
    total_rows = int(yaxis.get())
    total_columns = int(xaxis.get())
    table = tk.Toplevel(root)

    def tcompile():
        masterlines = []
        for entries in my_entries:
            print(cell.get())
            masterlines.append(int(cell.get()))
        plt.plot(masterlines)
        plt.show()

    my_entries = []
    for i in range(total_rows):
        for j in range(total_columns):
            cell = tk.Entry(table, width=20, font=('Agency FB', 15))
            cell.grid(row=i, column=j)
            my_entries.append(cell)
    tblframe = tk.Frame(table, bd=4)
    tblframe.grid(row=i + 1, column=j)
    compbtn = tk.Button(tblframe, font=("Agency FB", 20), text="Compile",
                        command=tcompile)
    compbtn.grid(row=0, column=0)



def handle_focus(event):
    event.widget.delete(0, "end")
    event.widget.unbind("<FocusIn>")
    event.widget.config(relief = 'sunken')
    event.widget.config(fg="black")
    event.widget.bind("<FocusOut>", handle_focus_out)

def handle_focus_out(event):
    event.widget.unbind("<FocusOut>")
    event.widget.config(fg="grey")
    event.widget.bind("<FocusIn>", handle_focus)
    event.widget.config(relief = 'flat')
    event.widget.insert(0, columns[event.widget.grid_info()["column"]])
    event.widget.bind("<FocusOut>", handle_focus_out)


root = tk.Tk()
# change the size of the window to be bigger
root.geometry("500x500")
#
from lib.components.double_scrolled_frame import DoubleScrolledFrame
mainframe = tk.Frame(root,padx=30, pady=30)
mainframe.pack()
tablegrid = DoubleScrolledFrame(mainframe, bd=1, relief="solid", pady=0.6,
                                padx=0.6,height=150)
tablegrid.pack()
columns = ["Column Entry", "Row Entry", "More","Of","Tis is "]
rows = 16
for j, col in enumerate(columns):
    xlabel = tk.Label(tablegrid, text=col, border=2, relief="ridge",
                      borderwidth=2, bd=1, anchor="nw",
                      background="#1e2e8f", fg="white")
    xlabel.grid(row=0, column=j, sticky='WENS',padx=0.1)
    tablegrid.grid_columnconfigure(j, weight=1)
for i in range(rows):
    for j in range(len(columns)):
        bgcolor = "#e6e6e6" if i % 2 == 0 else "white"
        xaxis = tk.Entry(tablegrid, border=2, relief="flat",bg=bgcolor)
        xaxis.bind("<FocusIn>", handle_focus)
        xaxis.grid(row=i+1, column=j)
# wt = WidgetTable(graphinput, 3, 3)

root.mainloop()

