from tkinter import *
import requests
import json
import cv2
from firebase import firebase
import numpy as np
import datetime
import base64
import threading
import time
import googlemaps
import webbrowser
from PIL import Image, ImageTk

mylocation = "Clifton"
#https://still-harbor-80129.herokuapp.com
addr = 'http://192.168.1.105:5000'
test_url = addr + '/api/test'

total_count= 0
charges = 100

def main_work(frame,username_info):
	global total_count
	global charges

	content_type = 'image/jpeg'
	headers = {'content-type': content_type}
	_, img_encoded = cv2.imencode('.jpg', frame)
	try:
		response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
		pass
	except Exception as e:
		print("Server did not respond !")
	else:
		#print (json.loads(response.text) + "\n")
		try:
			license_plate = json.loads(response.text)
			pass
		except Exception as e:
			print("No response from server! Corrupted image problem possible")
		else:
			if len(license_plate["message"]) <= 5:
				pass
			else:
				# if(license_plate["message"] == "8KA606"):
				# 	license_plate["message"] = "BKA606"
				print (license_plate["message"])
				if (license_plate["message"] != "same frame detected"):
					if (license_plate["message"] != "no car detected"):
						if (license_plate["message"] == "no plate detected"):
							print("car passed without plate")
							t1 = threading.Thread(target=no_plate, args=(username_info,img_encoded,license_plate["color"]))
							t1.start()
							with open('Demofile.txt', 'r') as file:
							    data = file.readlines()
							total_count=total_count+1
							data[2] = str(total_count)+'\n'
							data[0] = 'no plate\n'

							with open('Demofile.txt', 'w') as file:
							    file.writelines( data )

						else:
							try:
								plate = license_plate["message"]
								with open('Demofile.txt', 'r') as file:
								    data = file.readlines()
								total_count=total_count+1
								data[2] = str(total_count)+'\n'
								data[0] = plate+'\n'

								with open('Demofile.txt', 'w') as file:
								    file.writelines( data )
								flag2 = 0
								checkStolen = firebase.get("/RepCar",plate)
								getUsername = firebase.get("/License",plate)
								if checkStolen is None:
									if getUsername is not None:
										try:
											bal = firebase.get("/Users/"+getUsername,"Balance")
											pass
										except Exception as e:
											print("Unable to get balance, Connection to the database timeout! Check Internet Connection")
										else:
											balance = int(bal)
											if balance >= charges:
												balance = balance-charges
												strbal = str(balance)
												try:
													some_values = firebase.put("/Users/"+getUsername+"","Balance",strbal)
													pass
												except Exception as e:
													print("unable to put balance, Connection to the database timeout! Check Internet Connection")
												else:
													flag2=1
													pass
												finally:
													pass
												
											else:
												print(getUsername+" with "+plate+" has not enough money")
												t2 = threading.Thread(target=no_money, args=(username_info,img_encoded,plate,getUsername))
												t2.start()
											pass
										
									else:
										print("No record found")
										some_x= datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
										x = datetime.datetime.strptime(some_x, '%Y-%m-%d-%H-%M-%S')
										loc = checkStolen["Location"]

										api_key ='AIzaSyDeYiTPbzvFYbIA64sAqbXw3ZobvhsNurM'
										gmaps = googlemaps.Client(key=api_key)
										my_dist = gmaps.distance_matrix(loc,mylocation)['rows'][0]['elements'][0]['duration']['value']
										

										date_object = datetime.datetime.strptime(checkStolen['Date'], '%Y-%m-%d-%H-%M-%S')
										date_object2 = x - date_object
										sec1 = date_object2.seconds + date_object2.days * 86400
										sec2 = my_dist

										if (sec1<sec2):
											print("don't send")
										else:
											result3 = firebase.get("/CarCheck"+"/"+username_info+"","count")
											numeric = int(result3)
											numeric = numeric+1
											cstr = str(numeric)
											
											encoded_image = base64.standard_b64encode(img_encoded)
											coded = str(encoded_image)
											string_encoded_image = coded[2:]
											obj=plate+" "+x.strftime("%d-%b-%Y/%H:%M")+" Crime-Car "+string_encoded_image
											some_values = firebase.put("/CarCheck"+"/"+username_info+"",cstr,obj)
											some_values = firebase.put("/CarCheck"+"/"+username_info+"","count",cstr)
											with open('Demofile.txt', 'r') as file:
											    data = file.readlines()
											data[3] = plate+'\n'

											with open('Demofile.txt', 'w') as file:
											    file.writelines( data )
								else:
									print(plate+" had been reported as lost/stolen")
									t4 = threading.Thread(target=check_stolen, args=(username_info,img_encoded,plate,checkStolen))
									t4.start()
								if flag2 == 1:
									try:
										thread = threading.Thread(target=make_transaction, args=(getUsername,mylocation))
										thread.start()
										pass
									except Exception as e:
										print("Unable to make transaction, Connection to the database timeout! Check Internet Connection")
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
			pass
		finally:
			pass
		
	finally:
		pass


def make_transaction(getUsername, location):
	result2 = firebase.get('/Transaction',getUsername)
	c = int(result2["count"])
	c = c + 1
	result2["count"] = str(c)
	x= datetime.datetime.now()
	obj= x.strftime("%d-%b-%Y %H:%M") +" " + location + " "+ str(charges)
	cstr= str(c)
	result2[cstr] = obj
	new_object = {getUsername : result2}
	some_values = firebase.patch('/Transaction',new_object)

	result3 = firebase.get('/Money',None)
	money = int(result3)
	money = money + charges
	strMoney = str(money)
	some_values = firebase.put('/','Money/',strMoney)
	with open('Demofile.txt', 'r') as file:
	    data = file.readlines()
	data[1] = strMoney+'\n'

	with open('Demofile.txt', 'w') as file:
	    file.writelines( data )
	pass

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


def no_money(username_info, img_encoded, plate,getUsername):
	try:
		result3 = firebase.get("/CarCheck"+"/"+username_info+"","count")
		numeric = int(result3)
		numeric = numeric+1
		cstr = str(numeric)
		
		x= datetime.datetime.now()
		encoded_image = base64.standard_b64encode(img_encoded)
		coded = str(encoded_image)
		string_encoded_image = coded[2:]
		obj=plate+" "+x.strftime("%d-%b-%Y/%H:%M") +" No-TollMoney "+string_encoded_image
		some_values = firebase.put("/CarCheck"+"/"+username_info+"",cstr,obj)
		some_values = firebase.put("/CarCheck"+"/"+username_info+"","count",cstr)
		some_values = firebase.put("/Users/"+getUsername+"","warning","1")
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
		

		date_object = datetime.datetime.strptime(checkStolen['Date'], '%Y-%m-%d-%H-%M-%S')
		date_object2 = x - date_object
		sec1 = date_object2.seconds + date_object2.days * 86400
		sec2 = my_dist

		if (sec1<sec2):
			print("don't send")
		else:
			result3 = firebase.get("/CarCheck"+"/"+username_info+"","count")
			numeric = int(result3)
			numeric = numeric+1
			cstr = str(numeric)
			
			encoded_image = base64.standard_b64encode(img_encoded)
			coded = str(encoded_image)
			string_encoded_image = coded[2:]
			obj=plate+" "+x.strftime("%d-%b-%Y/%H:%M")+" Crime-Car "+string_encoded_image
			some_values = firebase.put("/CarCheck"+"/"+username_info+"",cstr,obj)
			some_values = firebase.put("/CarCheck"+"/"+username_info+"","count",cstr)
			with open('Demofile.txt', 'r') as file:
			    data = file.readlines()
			data[3] = plate+'\n'

			with open('Demofile.txt', 'w') as file:
			    file.writelines( data )
	except Exception as e:
		print("Connection to the database timeout! Check Internet Connection")
	else:
		pass
	finally:
		pass
	


def login_user():

	username_info = username.get()
	password_info = password.get()

	auth = False
	while True:
		flag = 0
		user_pass = username_info+"/Password"
		try:
			result5 = firebase.get("/Users",user_pass)
		except Exception as e:
			Label(screen1, text = "Connection Error").pack()
		

		if result5 == password_info:
			auth = True;
			with open('officer.txt', 'w') as file:
			    file.writelines( username_info )

		print (auth)
		if auth == True:
			status.config(text = "Authentication success!", fg = "green")
			screen.withdraw()
			try:
				cap = cv2.VideoCapture("final-4.mp4")
			except Exception as e:
				raise Exception("Video Not Found")
			
			while True:
				try:
					ret, frame = cap.read()
					if (cap.isOpened() and ret == True):
						#cv2.putText(frame, "Press \"q\" to exit." , (450, 450), cv2.FONT_ITALIC, 0.5, (0,255,0),2)
						#img_res = requests.get("http://192.168.0.103:8080/shot.jpg")
						#img_arr = np.array(bytearray(img_res.content), dtype = np.uint8)
						#img = cv2.imdecode(img_arr,-1)
						cv2.imshow('frame', frame)
						main_work(frame,username_info)

					else:
						lab.config(text="Camera Error!")
					if cv2.waitKey(1) & 0xFF == ord('q'):
						break
					pass
				except Exception as e:
					raise Exception("Video Not Found or Corrupted")
				else:
					pass
			cap.release()
			cv2.destroyAllWindows()
			screen.deiconify()
			break
		else:
			status.config(text = "Authentication failed!", fg = "red")
			break
 
  # username_entry.delete(0, END)
  # password_entry.delete(0, END)
 
  # Label(screen1, text = "Registration Sucess", fg = "green" ,font = ("calibri", 11)).pack()
 
def login():

	global firebase
	firebase = firebase.FirebaseApplication('https://toll-bbd9b.firebaseio.com/', None)

	global screen
	screen = Tk()
	screen.title("Login")
	screen.geometry("600x450")
	photo = ImageTk.PhotoImage(Image.open('icon.png').resize((150, 150)))

	global screen1
	screen1 = Frame(screen)
	screen1.pack()
	global username
	global password
	global username_entry
	global password_entry
	username = StringVar()
	password = StringVar()

	photolabel = Label(screen1,image=photo)
	photolabel.pack()
	Label(screen1, text = "Please enter details below", pady=30).pack()
	Label(screen1, text = "").pack()
	Label(screen1, text = "Username * ").pack()
	username_entry = Entry(screen1, textvariable = username)
	username_entry.pack()
	Label(screen1, text = "Password * ").pack()
	password_entry = Entry(screen1, textvariable = password, show = "*")
	password_entry.pack()
	Label(screen1, text = "").pack()
	global status
	status = Label(screen1, text = " ")
	status.pack()
	global lab
	lab = Label(screen1, text = "")
	lab.pack()
	Button(screen1,text = "Login", width = 10, height = 1, command = login_user).pack()
	screen1.mainloop()


login()
