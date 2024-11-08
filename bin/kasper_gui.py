import tkinter
from tkinter import PhotoImage

display = tkinter.Tk()
display.title("Kasper")
photo = PhotoImage(file="icon.png")
display.iconphoto(False, photo)

# making 2 versions IOS AND DESKTOP
display.mainloop()
