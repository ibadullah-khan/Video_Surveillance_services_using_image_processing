import PIL
from PIL import Image,ImageTk
import pytesseract
import requests
import json
import cv2
from tkinter import *
import time
import webbrowser
import json
from firebase import firebase
import numpy as np
import datetime
import base64
import threading
import googlemaps

mylocation = "Namak Bank"
#https://still-harbor-80129.herokuapp.com
addr = 'http://localhost:5000'
test_url = addr + '/api/test'
sema = threading.Semaphore(value=3)
threads = list()

global firebase
firebase = firebase.FirebaseApplication('https://toll-bbd9b.firebaseio.com/', None)

width, height = 1000, 600
cap = cv2.VideoCapture("TestVideo4.mp4")
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
root = Tk()
root.bind('<Escape>', lambda e: root.quit())
canvas = Canvas(root, height=height, width=width, bg='black',borderwidth = 0, highlightthickness = 0)
canvas.pack(side="top")

frame = Frame(canvas, bg='gray', bd=5, borderwidth = 5, highlightthickness = 0)
frame.place(relwidth=0.5, relheight=0.5)
frame.pack(side="left")

lmain = Label(frame,borderwidth = 0, highlightthickness = 0)
lmain.pack(side="left")

frame2 = Frame(canvas,bg='green', height=100, width=100)
frame2.pack(side="right")

canvas2 = Canvas(root, height=100, width=100, bg='black',borderwidth = 0, highlightthickness = 0)
canvas2.pack(side="bottom")

frame3 = Frame(canvas2,bg='green', height=100, width=100)
frame3.pack()
button = Button(frame3, text="Cam1")
button.pack()

def show_frame():
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = PIL.Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    t1 = threading.Thread(target=main_work, args=(frame,"15k-2231"))
    threads.append(t1)
    t1.start()
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)
    
def do_processing():
	pass

def callback(event):
    webbrowser.open_new(r"http://www.google.com")

def takeSnap():
    pass
def getOfficer():
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


def main_work(frame,username_info):
	sema.acquire()
	content_type = 'image/jpeg'
	headers = {'content-type': content_type}
	_, img_encoded = cv2.imencode('.jpg', frame)
	try:
		response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
		pass
	except Exception as e:
		print("Server did not respond !")
		raise
	else:
		#print (json.loads(response.text) + "\n")
		license_plate = json.loads(response.text)
		print ( license_plate["message"]+ " " + license_plate["color"])
		if (license_plate["message"] != "same frame detected"):
			if (license_plate["message"] != "no car detected"):
				if (license_plate["message"] == "no plate detected"):
					print("car passed without plate")
					t1 = threading.Thread(target=no_plate, args=(username_info,img_encoded,license_plate["color"]))
					t1.start()

				else:
					try:
						flag2 = 0
						plate = license_plate["message"]
						checkStolen = firebase.get("/RepCar",plate)
						getUsername = firebase.get("/License",plate)
						if checkStolen is None:
							if getUsername is not None:
								try:
									bal = firebase.get("/Users/"+getUsername,"Balance")
									pass
								except Exception as e:
									print("Connection to the database timeout! Check Internet Connection")
								else:
									balance = int(bal)
									if balance >= 100:
										balance = balance-100
										strbal = str(balance)
										try:
											some_values = firebase.put("/Users/"+getUsername+"","Balance",strbal)
											pass
										except Exception as e:
											print("Connection to the database timeout! Check Internet Connection")
										else:
											flag2=1
											pass
										finally:
											pass
										
									else:
										print(getUsername+" with "+plate+" has not enough money")
										t2 = threading.Thread(target=no_money, args=(username_info,img_encoded,plate))
										t2.start()
									pass
								finally:
									pass
								
							else:
								print("No record found")
						else:
							print(plate+" had been reported as lost/stolen")
							t4 = threading.Thread(target=check_stolen, args=(username_info,img_encoded,plate,checkStolen))
							t4.start()
						if flag2 == 1:
							try:
								result2 = firebase.get('/Transaction',getUsername)
								c = int(result2["count"])
								c = c + 1
								result2["count"] = str(c)
								x= datetime.datetime.now()
								obj= x.strftime("%d-%b-%Y %H:%M") +" " + location + " 100"
								cstr= str(c)
								result2[cstr] = obj
								new_object = {getUsername : result2}
								some_values = firebase.patch('/Transaction',new_object)
								pass
							except Exception as e:
								print("Connection to the database timeout! Check Internet Connection")
							else:
								pass
							finally:
								pass
						pass
					except Exception as e:
						print("Connection to the database timeout! Check Internet Connection")
					else:
						pass
					finally:
						pass
		pass
	finally:
		pass
	sema.release()


def no_plate(username_info, img_encoded, color):
	try:
		result3 = firebase.get("/CarCheck"+"/"+username_info+"","count")
		numeric = int(result3)
		numeric = numeric+1
		cstr = str(numeric)
		x= datetime.datetime.now()
		encoded_image = base64.standard_b64encode(img_encoded)
		coded = str(encoded_image)
		string_encoded_image = coded[2:]
		obj= x.strftime("%d-%b-%Y/%H:%M") +" "+color+" "+string_encoded_image
		some_values = firebase.put("/CarCheck"+"/"+username_info+"",cstr,obj)
		some_values = firebase.put("/CarCheck"+"/"+username_info+"","count",cstr)
		pass
	except Exception as e:
		print("Connection to the database timeout! Check Internet Connection")
	else:
		pass
	finally:
		pass


def no_money(username_info, img_encoded, plate):
	try:
		result3 = firebase.get("/CarCheck"+"/"+username_info+"","count")
		numeric = int(result3)
		numeric = numeric+1
		cstr = str(numeric)
		some_values = firebase.put("/CarCheck"+"/"+username_info+"","count",cstr)
		x= datetime.datetime.now()
		encoded_image = base64.standard_b64encode(img_encoded)
		coded = str(encoded_image)
		string_encoded_image = coded[2:]
		obj=plate+" "+x.strftime("%d-%b-%Y/%H:%M") +" No-TollMoney "+string_encoded_image
		some_values = firebase.put("/CarCheck"+"/"+username_info+"",cstr,obj)
		pass
	except Exception as e:
		print("Connection to the database timeout! Check Internet Connection")
	else:
		pass
	finally:
		pass
	

def check_stolen(username_info, img_encoded, plate, checkStolen):
	try:
		some_x= datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
		x = datetime.datetime.strptime(some_x, '%Y-%m-%d-%H-%M-%S')
		loc = checkStolen["Location"]

		api_key ='AIzaSyDeYiTPbzvFYbIA64sAqbXw3ZobvhsNurM'
		gmaps = googlemaps.Client(key=api_key)
		my_dist = gmaps.distance_matrix(loc,mylocation)['rows'][0]['elements'][0]['duration']['value']
		print(my_dist)
		

		date_object = datetime.datetime.strptime(checkStolen['Date'], '%Y-%m-%d-%H-%M-%S')
		date_object2 = x - date_object
		sec1 = date_object2.seconds + date_object2.days * 86400
		sec2 = my_dist

		print(sec1)

		if (sec1<sec2):
			print("don't send")
		else:
			result3 = firebase.get("/CarCheck"+"/"+username_info+"","count")
			numeric = int(result3)
			numeric = numeric+1
			cstr = str(numeric)
			some_values = firebase.put("/CarCheck"+"/"+username_info+"","count",cstr)
			encoded_image = base64.standard_b64encode(img_encoded)
			coded = str(encoded_image)
			string_encoded_image = coded[2:]
			obj=plate+" "+x.strftime("%d-%b-%Y/%H:%M")+" Crime-Car "+string_encoded_image
			some_values = firebase.put("/CarCheck"+"/"+username_info+"",cstr,obj)
	except Exception as e:
		print("Connection to the database timeout! Check Internet Connection")
	else:
		pass
	finally:
		pass
	


menu = Menu(root)
root.config(menu=menu)
root.focus_set()
root.title("HOMEPAGE")

subMenu = Menu(menu, tearoff=0)
menu.add_cascade(label="File",menu=subMenu)
subMenu.add_command(label="Take a Snapshot",command=takeSnap)
subMenu.add_command(label="Officer Information",command=getOfficer)
subMenu.add_separator()
subMenu.add_command(label="Exit",command=root.destroy)
subMenu.add_separator()

helpMenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help",menu=helpMenu)
helpMenu.add_command(label="Documentation",command=displayDoc)
helpMenu.add_separator()
helpMenu.add_command(label="License",command=displayLicense)
helpMenu.add_command(label="Version Info",command=version)
helpMenu.add_separator()
show_frame()
root.mainloop()