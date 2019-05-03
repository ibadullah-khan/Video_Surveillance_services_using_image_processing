from tkinter import *
from PIL import ImageTk, Image
import cv2


root = Tk()
# Create a frame
app = Frame(root, bg="white")
app.pack()
root.title("Testing App")
# Create a label in the frame
lmain = Label(app)
lmain.pack()

bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )

blackbutton = Button(bottomframe, text="Black", fg="black")
blackbutton.pack( side = BOTTOM)
# Capture from camera
cap = cv2.VideoCapture(0)

# function for video streaming
def video_stream():
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(1, video_stream) 

video_stream()
root.mainloop()