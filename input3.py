from tkinter import *
import win32gui
from PIL import ImageGrab
 
def CaptureScreen():
    HWND = win32gui.GetFocus()
    rect=win32gui.GetWindowRect(HWND)
    x = rect[0]
    x1=x+cv.winfo_width()
    y = rect[1]
    y1=y+cv.winfo_height()
    im=ImageGrab.grab((x,y,x1,y1))
    im.save("second.jpeg",'jpeg')
 
root = Tk()
cv = Canvas(root, width=300, height=150)
cv.pack()
cv.create_rectangle(10,10,50,50)
cv.update()
b = Button(root, text='截图', command=CaptureScreen)
b.pack()
root.mainloop()