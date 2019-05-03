from tkinter import *
import webbrowser

def callback(event):
    webbrowser.open_new(r"http://www.google.com")

def getOfficer():
    with open('officer.txt', 'r') as file:
        data = file.readlines()
    toplevel4 = Toplevel()
    toplevel4.geometry("350x200")
    toplevel4.title('Officer Information')
    toplevel4.focus_set()

    label = Label(toplevel4,text="Officer logged In",font=('Verdana', 20, 'bold'))
    label.pack()
    user = Label(toplevel4, text=data, fg="blue", cursor="hand2")
    user.pack()
    pass
def displayDoc():
    toplevel1 = Toplevel()
    toplevel1.geometry("350x200")
    toplevel1.title('Documentation')
    toplevel1.focus_set()

    label = Label(toplevel1,text="Documentation",font=('Verdana', 20, 'bold'))
    label.pack()
    link = Label(toplevel1, text="Documentation Link", fg="blue", cursor="hand2")
    link.bind("<Button-1>", callback)
    link.pack()
    pass

def displayLicense():
    toplevel2 = Toplevel()
    toplevel2.title('Version Information')
    toplevel2.focus_set()

    text2 = Text(toplevel2, height=20, width=50)
    scroll = Scrollbar(toplevel2, command=text2.yview)
    text2.configure(yscrollcommand=scroll.set)
    text2.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
    text2.tag_configure('big', font=('Verdana', 20, 'bold'))
    text2.tag_configure('color',font=('Times New Roman', 12))
    text2.tag_bind('follow', '<1>', lambda e, t=text2: t.insert(END, "Not now, maybe later!"))
    text2.insert(END,'\nLICENSE INFORMATION\n', 'big')
    quote = """
    THIS AGREEMENT BINDS YOU (“YOU”) TO THE 
    TERMS AND CONDITIONS SET FORTH HEREIN IN 
    CONNECTION WITH YOUR USE OF TOLL SYSTEM 
    (“WE”, “OUR”, “US”, OR “COMPANY”) SOFTWARE,
    SERVICES OR OTHER OFFERINGS ON OUR APP 
    (COLLECTIVELY, OUR “PRODUCTS”). BY USING 
    ANY OF THE COMPANY PRODUCTS, YOU AGREE TO 
    ACCEPT THE TERMS AND CONDITIONS OF THIS 
    AGREEMENT.IF YOU DO NOT ACCEPT THESE TERMS,
    YOU MUST NOT USE ALL OR ANY PORTION OF THE
    COMPANY PRODUCTS.
    """
    text2.insert(END, quote, 'color')
    text2.pack(side=LEFT)
    scroll.pack(side=RIGHT, fill=Y)
    pass


def version():
    toplevel = Toplevel()
    toplevel.title('Version Information')
    toplevel.focus_set()

    text2 = Text(toplevel, height=20, width=50)
    scroll = Scrollbar(toplevel, command=text2.yview)
    text2.configure(yscrollcommand=scroll.set)
    text2.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
    text2.tag_configure('big', font=('Verdana', 20, 'bold'))
    text2.tag_configure('color',font=('Times New Roman', 12))
    text2.tag_bind('follow', '<1>', lambda e, t=text2: t.insert(END, "Not now, maybe later!"))
    text2.insert(END,'\nVERSION INFORMATION\n', 'big')
    quote = """
    Version : 0.0.1
    Type : Python 3.6 
    Product Name : Toll System,
    Size : 100 MB,
    Copyright : AUMI.Inc,
    Date Modified: 02/May/2017
    Language: English (United States)
    """
    text2.insert(END, quote, 'color')
    text2.pack(side=LEFT)
    scroll.pack(side=RIGHT, fill=Y)
    pass



root = Tk()
menu = Menu(root)
root.config(menu=menu)
root.focus_set()
root.title("HOMEPAGE")
root.geometry("700x500")

subMenu = Menu(menu, tearoff=0)
menu.add_cascade(label="File",menu=subMenu)
#subMenu.add_command(label="Take a Snapshot",command=takeSnap)
subMenu.add_command(label="Officer Information",command=getOfficer)
subMenu.add_separator()
subMenu.add_command(label="Exit",command=root.quit)
subMenu.add_separator()

helpMenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help",menu=helpMenu)
helpMenu.add_command(label="Documentation",command=displayDoc)
helpMenu.add_separator()
helpMenu.add_command(label="License",command=displayLicense)
helpMenu.add_command(label="Version Info",command=version)
helpMenu.add_separator()

screen2 = Frame(root, width=1000, height=600)
screen2.pack()
left_container = Frame(screen2, bg="black",width=450, height=450, borderwidth=2)
right_container = Frame(screen2, bg="black",width=200, height=450, borderwidth=2)
left_container.pack(side=LEFT)
right_container.pack(side=RIGHT)
revenue_view = Frame(right_container,height=150,width=200, borderwidth=5)
car_count = Frame(left_container,height=150,width=200,borderwidth=5)
last_detect= Frame(right_container,height=150,width=200,borderwidth=5)
last_criminal = Frame(left_container,height=150,width=200,borderwidth=5)
revenue_view.pack()
car_count.pack()
last_detect.pack()
last_criminal.pack()



count_label = Label(car_count,text="Default",font = ("calibri", 14))
count_label.place(x=95, y=75, anchor="center")
label1 = Label(car_count,text="NUMBER OF CARS",font = ("calibri", 16))
label1.place(x=95, y=35, anchor="center")

last_detect_label = Label(last_detect,text="Default",font = ("calibri", 14))
last_detect_label.place(x=95, y=75, anchor="center")
label2 = Label(last_detect,text="LAST DETECTED",font = ("calibri", 16))
label2.place(x=95, y=35, anchor="center")

revenue_view_label = Label(revenue_view,text="Default",font = ("calibri", 14))
revenue_view_label.place(x=95, y=75, anchor="center")
label3 = Label(revenue_view,text="REVENUE GENERATED",font = ("calibri", 16))
label3.place(x=95, y=35, anchor="center")

criminal = Label(last_criminal,text="Default",font = ("calibri", 14))
criminal.place(x=95, y=75, anchor="center")
label4 = Label(last_criminal,text="SUSPECTED",font = ("calibri", 16))
label4.place(x=95, y=35, anchor="center")

def continuous():
    f = open("DemoFile.txt", "rt")
    last = f.readline()
    rev = f.readline()
    count = f.readline()
    crime = f.readline()
    last=last.replace('\n','')
    rev=rev.replace('\n','')
    count=count.replace('\n','')
    crime=crime.replace('\n','')
    last_detect_label.configure(text=last, bg=last_detect["bg"])
    revenue_view_label.configure(text=rev, bg=revenue_view["bg"])
    count_label.configure(text=count, bg=car_count["bg"])
    criminal.configure(text=crime, bg=last_criminal["bg"],fg="red")
    count_label.after(10000, continuous)



status = Label(root, text="App Status: Stable", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

continuous()


root.mainloop()
