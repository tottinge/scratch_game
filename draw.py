from tkinter import *

root = Tk()
root.title("visualize")
root.geometry("320x550")

my_canvas = Canvas(root, width=300, height=500, bg="grey")
my_canvas.pack(pady=20)

#my_canvas.create_line(x1, y1, x2, y2, fill="blue")
my_canvas.create_line(0,0, 200,400, fill="blue")
my_canvas.create_rectangle(0,0, 100,200, fill="green")


root.mainloop()
