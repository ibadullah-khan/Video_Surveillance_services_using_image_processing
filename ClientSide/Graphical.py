# import tkinter as tk

# root = tk.Tk()

# button = tk.Button(root, text="Button")
# button.pack()

# frame = tk.Frame(root, bg='#80c1ff', bd=5)
# frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

# root.mainloop()
import tkinter as tk
import threading
import imageio
from PIL import Image, ImageTk

video_name = "TestVideo2.mp4" #This is your video file path
video = imageio.get_reader(video_name)

def stream(label):

    frame = 0
    for image in video.iter_data():
        frame += 1                                    #counter to save new frame number
        image_frame = Image.fromarray(image)                #if you need the frame you can save each frame to hd
        frame_image = ImageTk.PhotoImage(image_frame)
        label.config(image=frame_image)
        label.image = frame_image

if __name__ == "__main__":

	HEIGHT = 500
	WIDTH = 800
	root = tk.Tk()
	canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg='black')
	canvas.pack()
	frame = tk.Frame(root, bg='#80c1ff', bd=5)
	frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.5, anchor='n')
	my_label = tk.Label(frame)
	my_label.pack()
	thread = threading.Thread(target=stream, args=(my_label,))
	thread.daemon = 1
	thread.start()
	root.mainloop()